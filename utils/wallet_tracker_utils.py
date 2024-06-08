import json
import time
import threading
import requests

import numpy as np
import pandas as pd
from moralis import sol_api

from .miss_utils import (
    create_directory_if_not_exists,
    create_file_if_not_exists,
    read_input,
    write_output,
)
from .constants import DELAY, LAST_K_TXS


def start_get_wallet_portfolio_threads(wallets: list, api_key: str) -> None:
    threads = []
    for i, wallet in enumerate(wallets):
        thread = start_get_wallet_portfolio_thread(i, wallet, api_key)

        threads.append(thread)

    backoff_times = {thread.name: [0, 1] for thread in threads}
    while True:
        for i, thread in enumerate(threads):
            if thread.is_alive():
                continue
            else:
                if backoff_times[thread.name][0] < 5:
                    print(f"{thread.name} has died, restarting...")

                    new_thread = start_get_wallet_portfolio_thread(
                        i, wallets[i], api_key, backoff_times[thread.name][1]
                    )

                    backoff_times[thread.name][0] += 1
                    backoff_times[thread.name][1] *= 2

                    threads[i] = new_thread

        time.sleep(DELAY)


def start_get_wallet_portfolio_thread(
    idx: int,
    wallet: list[str],
    api_key: str,
    delay: int = 0,
) -> threading.Thread:
    time.sleep(delay)

    thread = threading.Thread(
        target=start_get_wallet_portfolio,
        kwargs={
            "wallet": wallet,
            "api_key": api_key,
            "log": True,
        },
        name=f"Thread {idx+1} - Portfolio - Wallet - {wallet[1]} - {wallet[0]}",
        daemon=True,
    )

    thread.start()

    return thread


def start_get_wallet_portfolio(wallet: list[str], api_key: str, log: bool) -> None:
    while True:
        get_wallet_portfolio(wallet, api_key, log)

        time.sleep(DELAY)


def get_wallet_portfolio(wallet: str, api_key: str, log: bool = False) -> dict:
    current_timestamp = str(int(time.time()))

    params = {"network": "mainnet", "address": wallet[0]}

    portfolio = sol_api.account.get_portfolio(
        api_key=api_key,
        params=params,
    )

    if portfolio:
        result = {
            "address": wallet[0],
            "timestamp": current_timestamp,
        } | format_wallet_portfolio(portfolio)
    else:
        result = {"address": wallet[0], "timestamp": current_timestamp} | {
            "tokens": [],
            "nfts": [],
            "native_balance": "",
        }

    if log:
        save_to_dir = f"data/wallets/{wallet[1]}_{wallet[0]}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path_portfolio = save_to_dir + "portfolio.txt"

        create_file_if_not_exists(save_to_file_path_portfolio)

        write_output(result, save_to_file_path_portfolio)

    return result


def format_wallet_portfolio(portfolio: dict) -> dict:
    tokens = []
    for x in portfolio["tokens"]:
        tokens.append(
            {
                "name": x["name"],
                "symbol": x["symbol"],
                "amount": x["amount"],
                "address": x["associatedTokenAddress"],
                "type": "token",
            }
        )

    nfts = []
    for x in portfolio["nfts"]:
        nfts.append(
            {
                "name": x["name"],
                "symbol": x["symbol"],
                "amount": x["amount"],
                "address": x["associatedTokenAddress"],
                "type": "nft",
            }
        )

    native_balance = portfolio["nativeBalance"]["solana"]

    result = {
        "tokens": tokens,
        "nfts": nfts,
        "native_balance": native_balance,
    }

    return result


def start_get_token_transfers_threads(wallets: list, api_key: str) -> None:
    threads = []
    for i, wallet in enumerate(wallets):
        thread = start_get_token_transfers_thread(i, wallet, api_key)

        threads.append(thread)

    backoff_times = {thread.name: [0, 1] for thread in threads}
    while True:
        for i, thread in enumerate(threads):
            if thread.is_alive():
                continue
            else:
                if backoff_times[thread.name][0] < 5:
                    print(f"{thread.name} has died, restarting...")

                    new_thread = start_get_token_transfers_thread(
                        i, wallets[i], api_key, backoff_times[thread.name][1]
                    )

                    backoff_times[thread.name][0] += 1
                    backoff_times[thread.name][1] *= 2

                    threads[i] = new_thread

        time.sleep(DELAY)


def start_get_token_transfers_thread(
    idx: int,
    wallet: list[str],
    api_key: str,
    delay: int = 0,
) -> threading.Thread:
    time.sleep(delay)

    thread = threading.Thread(
        target=start_get_token_transfers,
        kwargs={
            "wallet": wallet,
            "api_key": api_key,
            "num_tx": LAST_K_TXS,
            "log": True,
        },
        name=f"Thread {idx+1} - Token Transfers - Wallet - {wallet[1]} - {wallet[0]}",
        daemon=True,
    )

    thread.start()

    return thread


def start_get_token_transfers(
    wallet: list[str], api_key: str, num_tx: int, log: bool
) -> None:
    while True:
        get_token_transfers(wallet, api_key, num_tx, log)

        time.sleep(DELAY)


def get_token_transfers(
    wallet: list[str], api_key: str, num_tx: int = 25, log: bool = False
):
    url = "https://api.shyft.to/sol/v1/wallet/transaction_history"
    headers = {"x-api-key": api_key}
    params = {"network": "mainnet-beta", "wallet": wallet[0], "tx_num": num_tx}

    response = requests.get(url, headers=headers, params=params)

    result = []
    if response.status_code == 200:
        for x in response.json()["result"]:
            if x["type"] == "TOKEN_TRANSFER" and x["status"].lower() != "fail":
                timestamp = x["timestamp"]

                for y in x["actions"]:
                    if y["type"] == "TOKEN_TRANSFER":
                        temp = {
                            "timestamp": timestamp,
                            "sender": y["info"]["sender"],
                            "receiver": y["info"]["receiver"],
                            "amount": y["info"]["amount"],
                            "token_address": y["info"]["token_address"],
                        }

                        result.append(temp)

    if log:
        save_to_dir = f"data/wallets/{wallet[1]}_{wallet[0]}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path_portfolio = save_to_dir + "token_txs.txt"

        create_file_if_not_exists(save_to_file_path_portfolio)

        write_output(result, save_to_file_path_portfolio)

    return result


def start_get_buys_sells_threads(wallets: list) -> None:
    threads = []
    for i, wallet in enumerate(wallets):
        thread = start_get_buys_sells_thread(i, wallet)

        threads.append(thread)

    backoff_times = {thread.name: [0, 1] for thread in threads}
    while True:
        for i, thread in enumerate(threads):
            if thread.is_alive():
                continue
            else:
                if backoff_times[thread.name][0] < 5:
                    print(f"{thread.name} has died, restarting...")

                    new_thread = start_get_buys_sells_thread(
                        i, wallets[i], backoff_times[thread.name][1]
                    )

                    backoff_times[thread.name][0] += 1
                    backoff_times[thread.name][1] *= 2

                    threads[i] = new_thread

        time.sleep(DELAY)


def start_get_buys_sells_thread(
    idx: int,
    wallet: list[str],
    delay: int = 0,
) -> threading.Thread:
    time.sleep(delay)

    thread = threading.Thread(
        target=start_get_buys_sells,
        kwargs={
            "wallet": wallet,
            "log": True,
        },
        name=f"Thread {idx+1} - Buys and Sells - Wallet - {wallet[1]} - {wallet[0]}",
        daemon=True,
    )

    thread.start()

    return thread


def start_get_buys_sells(wallet: list[str], log: bool) -> None:
    while True:
        get_buys_sells(wallet, log)

        time.sleep(DELAY)


def get_buys_sells(wallet: list[str], log: bool = False) -> dict:
    portfolio_history = read_input(
        f"data/wallets/{wallet[1]}_{wallet[0]}/portfolio.txt"
    )

    if len(portfolio_history) > 2:
        timestamp = json.loads(portfolio_history[-1])["timestamp"]

        portfolio_t_k_1 = json.loads(portfolio_history[-2])["tokens"]
        portfolio_t_k = json.loads(portfolio_history[-1])["tokens"]

        portfolio_t_k_1 = pd.DataFrame(portfolio_t_k_1)
        portfolio_t_k = pd.DataFrame(portfolio_t_k)

        temp = portfolio_t_k.merge(portfolio_t_k_1, on="address", how="outer")

        temp.fillna(0, inplace=True)

        temp["change"] = temp["amount_x"].astype("float") - temp["amount_y"].astype(
            "float"
        )

        temp["action"] = temp["change"].apply(buy_sell_same)

        result = temp[["address"]]

        result.loc[:, "name"] = np.where(
            temp["name_x"] != 0, temp["name_x"], temp["name_y"]
        )

        result.loc[:, "symbol"] = np.where(
            temp["symbol_x"] != 0, temp["symbol_x"], temp["symbol_y"]
        )

        result.loc[:, "quantity"] = temp["change"].abs()

        result.loc[:, "action"] = temp["action"]

        result["timestamp"] = timestamp

        result = result.to_dict("records")
    else:
        result = []

    if log:
        save_to_dir = f"data/wallets/{wallet[1]}_{wallet[0]}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path_portfolio = save_to_dir + "buys_sells.txt"

        create_file_if_not_exists(save_to_file_path_portfolio)

        write_output(result, save_to_file_path_portfolio)

    return result


def buy_sell_same(x) -> str:
    if x > 0:
        return "buy"
    elif x < 0:
        return "sell"
    else:
        return ""


def setup_wallet_tracker(wallets: list) -> None:
    for wallet in wallets:
        save_to_dir = f"data/wallets/{wallet[1]}_{wallet[0]}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path_token_txs = save_to_dir + "token_txs.txt"

        create_file_if_not_exists(save_to_file_path_token_txs)

        save_to_file_path_portfolio = save_to_dir + "portfolio.txt"

        create_file_if_not_exists(save_to_file_path_portfolio)

        save_to_file_path_buy_sells = save_to_dir + "buys_sells.txt"

        create_file_if_not_exists(save_to_file_path_buy_sells)
