import time
import requests
import threading

from moralis import sol_api

from .miss_utils import (
    create_directory_if_not_exists,
    create_file_if_not_exists,
    write_output,
)
from .constants import DELAY


def start_get_token_price_threads(token_metadatas: list[dict], api_key: str) -> None:
    threads = []
    for i, token_metadata in enumerate(token_metadatas):
        thread = start_get_token_price_thread(i, token_metadata, api_key)

        threads.append(thread)

    backoff_times = {thread.name: [0, 1] for thread in threads}
    while True:
        for i, thread in enumerate(threads):
            if thread.is_alive():
                continue
            else:
                if backoff_times[thread.name][0] < 5:
                    print(f"{thread.name} has died, restarting...")

                    new_thread = start_get_token_price_thread(
                        i, token_metadatas[i], api_key, backoff_times[thread.name][1]
                    )

                    backoff_times[thread.name][0] += 1
                    backoff_times[thread.name][1] *= 2

                    threads[i] = new_thread

        time.sleep(DELAY)


def start_get_token_price_thread(
    idx: int,
    token_metadata: dict,
    api_key: str,
    delay: int = 0,
) -> threading.Thread:
    time.sleep(delay)

    thread = threading.Thread(
        target=start_get_token_price,
        kwargs={
            "address": token_metadata["address"],
            "api_key": api_key,
            "token_metadata": token_metadata,
            "log": True,
        },
        name=f"Thread {idx+1} - Token - {token_metadata['name']} - {token_metadata['symbol']}",
        daemon=True,
    )

    thread.start()

    return thread


def start_get_token_price(
    address: str, api_key: str, token_metadata: dict, log: bool
) -> None:
    while True:
        get_token_price(address, api_key, token_metadata, log)

        time.sleep(DELAY)


def get_token_price(
    address: str, api_key: str, token_metadata: dict | None = None, log: bool = False
) -> dict:
    current_timestamp = str(int(time.time()))

    params = {
        "address": address,
        "network": "mainnet",
    }

    token_price = sol_api.token.get_token_price(
        api_key=api_key,
        params=params,
    )

    if token_metadata is None:
        token_metadata = get_token_metadata(address, api_key)

    if token_price:
        result = token_metadata | {
            "price_usd": token_price["usdPrice"],
            "exchange_name": token_price["exchangeName"],
            "timestamp": current_timestamp,
        }
    else:
        result = token_metadata | {
            "price_usd": "",
            "exchange_name": "",
            "timestamp": current_timestamp,
        }

    if log:
        if token_metadata["symbol"]:
            save_to_dir = f"data/tokens/{token_metadata['symbol']}/"
        else:
            save_to_dir = f"data/tokens/{token_metadata['address']}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path = save_to_dir + "prices.txt"

        create_file_if_not_exists(save_to_file_path)

        write_output(result, save_to_file_path)

    return result


def get_token_metadata(address: str, api_key: str) -> dict:
    url = f"https://solana-gateway.moralis.io/token/mainnet/{address}/metadata"

    headers = {"Accept": "application/json", "X-API-Key": api_key}

    response = requests.request("GET", url, headers=headers)

    result = {
        "address": address,
    }
    if response.status_code == 200:
        token_metadata = response.json()

        result["name"] = token_metadata["name"]
        result["symbol"] = token_metadata["symbol"]
    else:
        result["name"] = ""
        result["symbol"] = ""

    return result


def setup_token_tracker(token_metadatas: dict) -> None:
    for token_metadata in token_metadatas:
        if token_metadata["symbol"]:
            save_to_dir = f"data/tokens/{token_metadata['symbol']}/"
        else:
            save_to_dir = f"data/tokens/{token_metadata['address']}/"

        create_directory_if_not_exists(save_to_dir)

        save_to_file_path = save_to_dir + "prices.txt"

        create_file_if_not_exists(save_to_file_path)
