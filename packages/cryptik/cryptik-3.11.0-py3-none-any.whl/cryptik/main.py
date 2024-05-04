# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2024 dradux.com
#
# LOGGING: designed to run at INFO loglevel.

import json
import logging
import os
import sys
from decimal import Decimal
from urllib.request import urlopen

import arrow
import click
import tomllib

import importlib.metadata as md

local_config = None

_log_level = "INFO"  # [CRITICAL|ERROR|WARNING|INFO|DEBUG] (suggest INFO)

logging.basicConfig(
    format="%(message)s",
    level=logging.getLevelName(_log_level),
    stream=sys.stdout,
)


class Ticker(object):
    """
    Ticker info returned by exchanges.
    """

    price = 0.00  # decimal(2)
    high = 0.00  # decimal(2)
    low = 0.00  # decimal(2)
    bid = 0.00  # decimal(2)
    ask = 0.00  # decimal(2)
    volume = 0.00  # decimal(2)
    rundts = 0  # long

    def __init__(self, price="", high="", low="", bid="", ask="", volume="", rundts=""):
        self.price = (
            Decimal(price.replace("$", "")).quantize(Decimal("0.00"))
            if isinstance(price, str)
            else price
        )
        self.high = (
            Decimal(high.replace("$", "")).quantize(Decimal("0.00"))
            if isinstance(high, str)
            else high
        )
        self.low = (
            Decimal(low.replace("$", "")).quantize(Decimal("0.00"))
            if isinstance(low, str)
            else low
        )
        self.bid = (
            Decimal(bid.replace("$", "")).quantize(Decimal("0.00"))
            if isinstance(bid, str)
            else bid
        )
        self.ask = (
            Decimal(ask.replace("$", "")).quantize(Decimal("0.00"))
            if isinstance(ask, str)
            else ask
        )
        self.volume = (
            Decimal(volume).quantize(Decimal("0.00"))
            if isinstance(volume, str)
            else volume
        )
        self.rundts = arrow.get(int(rundts)) if isinstance(rundts, str) else rundts

    def __str__(self):
        rundts = (
            self.rundts.to("local").format(local_config["default"]["date_format"])
            if self.rundts
            else f"{arrow.utcnow().to('local').format(local_config['default']['date_format'])}*"
        )
        if local_config["default"]["response_data_format"] == "compact":
            return (
                f"{local_config['default']['currency_indicator']}{self.price} @{rundts}"
            )
        elif local_config["default"]["response_data_format"] == "minimal":
            return f"{local_config['default']['currency_indicator']}{self.price}"
        elif local_config["default"]["response_data_format"] == "full":
            return f"{local_config['default']['currency_indicator']}{self.price} @{self.rundts.to('local').format(local_config['default']['date_format'])}\n  low: {self.currencyIndicator}{self.low}  high: {self.currencyIndicator}{self.high}\n  bid: {self.currencyIndicator}{self.bid}  ask: {self.currencyIndicator}{self.ask}\n  vol: {self.volume}"
        else:
            logging.error(
                f"Unknown response data format: [{local_config['default']['response_data_format']}]"
            )
            return ""


def get_version():
    """
    Get Version string.
    """

    _name = md.metadata("cryptik")["Name"]
    _version = md.metadata("cryptik")["Version"]
    return f"{_name} {_version}"


def show_version():
    """
    Show version.
    NOTICE: we load the pyproject.toml here (rather than a config) so its not loaded on normal app usage as it is not needed then.
    """

    logging.critical(f"{get_version()}")

    sys.exit()


def list_all_exchanges():
    """
    List all exchanges.
    """

    for exchg in local_config["exchanges"]:
        logging.critical(f"- {exchg['label']} ({exchg['id']}) - {exchg['type']}")
    sys.exit()


def lookup_exchange(exchange, crypto_currency):
    """
    Lookup exchange by exchange (id) and crypto-currency (type).
    """

    # filter on exchange
    exchg_set = filter(lambda x: exchange in x["id"], local_config["exchanges"])
    # filter on type
    el = list(filter(lambda x: crypto_currency in x["type"], exchg_set))
    if len(el) == 1:
        return el[0]
    elif len(el) < 1:
        logging.error(f"Exchange not found, verify [{exchange}] is configured.")
        sys.exit(21)
    else:
        logging.error(
            f"Lookup exchange returned [{len(el)}] exchanges matching the exchange [{exchange}] and crypto-currency [{crypto_currency}] specified and cannot continue."
        )
        sys.exit(22)


def process(
    exchange, response_moniker_format, response_data_format, crypto_currency, quiet
):
    exchg = lookup_exchange(exchange, crypto_currency)
    logging.debug(f"- EXCHANGE={exchg}; crypto-currency={crypto_currency}")
    er = get_exchange_data(exchg["url"])
    logging.debug(f"- processing exchange response: {er}")
    ticker = None
    if exchange == "BITSTAMP":
        ticker = Ticker(
            price=er["last"],
            high=er["high"],
            low=er["low"],
            bid=er["bid"],
            ask=er["ask"],
            volume=er["volume"],
            rundts=er["timestamp"],
        )
    elif exchange == "KRAKEN":
        ticker = Ticker(
            price=er["result"][exchg["pair_id"]]["c"][0],
            high=er["result"][exchg["pair_id"]]["h"][0],
            low=er["result"][exchg["pair_id"]]["l"][0],
            bid=er["result"][exchg["pair_id"]]["b"][0],
            ask=er["result"][exchg["pair_id"]]["a"][0],
            volume=er["result"][exchg["pair_id"]]["v"][0],
            rundts=None,
        )
    else:
        # should not reach here as lookup_exchange will handle missing exchanges.
        logging.error(f"Unknown exchange [{exchange}], cannot continue.")
        sys.exit(99)

    if ticker:
        if quiet:
            ret = ticker.price
        else:
            ret = (
                f"{get_formatted_moniker(response_moniker_format, exchg)} {str(ticker)}"
            )
        return ret
    else:
        logging.error("Issue with Ticker model, cannot continue.")
        sys.exit(98)


def get_exchange_data(url):
    """
    Get data from exchange.
    """

    logging.debug(f"- getting exchange data from={url}")
    response = urlopen(url)  # nosec
    r = response.read().decode()
    if response.getcode() == 200:
        return json.loads(r)
    else:
        logging.error(
            f"Problem retrieving data:\n- code: {r.status_code}\n- text: {r.text}"
        )
        return None


def get_formatted_moniker(fmt, dataSource):
    """
    Get the response moniker in given format
    """

    if fmt == "standard":
        return f"{dataSource['id']}"
    if fmt == "minimal":
        return f"{dataSource['label']}"
    if fmt == "label":
        return f"{dataSource['label']}:{dataSource['type']}"


@click.command()
@click.option("--version", default=False, is_flag=True, help="show version and exit")
@click.option(
    "--exchange",
    "-e",
    default="",
    help="exchange to check for price (note: use --list-exchanges to see a full list)",
)
@click.option(
    "--crypto-currency",
    "-t",
    default="BTC",
    help="crypto currency type (BTC, LTC, etc.)",
)
@click.option(
    "--response-moniker-format",
    "-m",
    default="",
    help="response moniker (exchange label) format (e.g. one of [standard|label|minimal|none])",
)
@click.option(
    "--response-data-format",
    "-d",
    default="",
    help="response data format (e.g. one of [minimal|compact|full])",
)
@click.option(
    "--verbose", "-v", default=False, is_flag=True, help="show additional information"
)
@click.option(
    "--quiet",
    "-q",
    default=False,
    is_flag=True,
    help="quiet (minimal) response - only returns the price (no moniker/formatting, as a decimal)",
)
@click.option(
    "--list-exchanges",
    "-l",
    default=False,
    is_flag=True,
    help="list configured exchanges",
)
@click.option(
    "--config-file",
    "-c",
    default=os.path.expanduser("~/.config/cryptik/config.toml"),
    help="config file location (default '~/.config/cryptik/config.toml')",
)
def app(
    version,
    exchange,
    crypto_currency,
    response_moniker_format,
    response_data_format,
    verbose,
    quiet,
    list_exchanges,
    config_file,
):
    global local_config
    logging.setLevel(logging.DEBUG) if verbose else None
    logging.debug(
        f"- exchange: {exchange}\n- reponse moniker format: {response_moniker_format}\n- reponse data format: {response_data_format}\n- config file: {config_file}"
    )

    if version:
        show_version()

    with open(config_file, "rb") as f:
        local_config = tomllib.load(f)

    if list_exchanges:
        list_all_exchanges()

    exchange = exchange if exchange else local_config["default"]["exchange"]
    response_moniker_format = (
        response_moniker_format
        if response_moniker_format
        else local_config["default"]["response_moniker_format"]
    )
    response_data_format = (
        response_data_format
        if response_data_format
        else local_config["default"]["response_data_format"]
    )
    print(
        process(
            exchange,
            response_moniker_format,
            response_data_format,
            crypto_currency,
            quiet,
        )
    )
