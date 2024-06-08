import os
import time
import threading

from dotenv import load_dotenv

from utils.wallet_tracker_utils import (
    setup_wallet_tracker,
    start_get_wallet_portfolio_threads,
    start_get_token_transfers_threads,
    start_get_buys_sells_threads,
)
from utils.miss_utils import read_input, create_directory_if_not_exists
from utils.constants import DELAY


load_dotenv()


def main():
    create_directory_if_not_exists("data/")
    create_directory_if_not_exists("data/wallets/")

    WALLETS = [x.split(",") for x in read_input("wallets.txt")]

    MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
    SHYFT_API_KEY = os.getenv("SHYFT_API_KEY")

    setup_wallet_tracker(WALLETS)

    thread_portfolio = threading.Thread(
        target=start_get_wallet_portfolio_threads,
        kwargs={
            "wallets": WALLETS,
            "api_key": MORALIS_API_KEY,
        },
        name=f"Thread - Portfolio",
        daemon=True,
    )

    thread_portfolio.start()

    thread_token_transfers = threading.Thread(
        target=start_get_token_transfers_threads,
        kwargs={
            "wallets": WALLETS,
            "api_key": SHYFT_API_KEY,
        },
        name=f"Thread - Token Transfers",
        daemon=True,
    )

    thread_token_transfers.start()

    thread_buys_sells = threading.Thread(
        target=start_get_buys_sells_threads,
        kwargs={
            "wallets": WALLETS,
        },
        name=f"Thread - Buys and Sells",
        daemon=True,
    )

    thread_buys_sells.start()

    while True:
        if thread_portfolio.is_alive():
            continue
        else:
            thread_portfolio = threading.Thread(
                target=start_get_wallet_portfolio_threads,
                kwargs={
                    "wallets": WALLETS,
                    "api_key": MORALIS_API_KEY,
                },
                name=f"Thread - Portfolio",
                daemon=True,
            )

        if thread_token_transfers.is_alive():
            continue
        else:
            thread_token_transfers = threading.Thread(
                target=start_get_token_transfers_threads,
                kwargs={
                    "wallets": WALLETS,
                    "api_key": SHYFT_API_KEY,
                },
                name=f"Thread - Token Transfers",
                daemon=True,
            )

        if thread_buys_sells.is_alive():
            continue
        else:
            thread_buys_sells = threading.Thread(
                target=start_get_buys_sells_threads,
                kwargs={
                    "wallets": WALLETS,
                },
                name=f"Thread - Buys and Sells",
                daemon=True,
            )

        time.sleep(DELAY)


if __name__ == "__main__":
    main()
