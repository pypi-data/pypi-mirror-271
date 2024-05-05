import json
import os
from pathlib import Path
from typing import Any

from krakenpull import CurrencyPair


def get_root_dir():
    return Path(os.getenv("ROOT_DIRECTORY", Path(__file__).parents[1]))


def load_json(path: Path) -> Any:
    with open(get_root_dir() / path, "r") as f:
        return json.load(f)


def get_unique_tickers(tickers: list[CurrencyPair]) -> list[CurrencyPair]:
    uniq_list = []
    for ticker in tickers:
        if ticker not in uniq_list:
            uniq_list.append(ticker)

    return uniq_list
