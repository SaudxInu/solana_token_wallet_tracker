import os

from dotenv import load_dotenv

from utils.token_tracker_utils import (
    setup_token_tracker,
    get_token_metadata,
    start_get_token_price_threads,
)
from utils.miss_utils import read_input, create_directory_if_not_exists


load_dotenv()


def main():
    create_directory_if_not_exists("data/")
    create_directory_if_not_exists("data/tokens/")

    TOKEN_ADDRESSES = read_input("token_addresses.txt")
    MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
    TOKEN_METADATAS = [
        get_token_metadata(token_address, MORALIS_API_KEY)
        for token_address in TOKEN_ADDRESSES
    ]

    setup_token_tracker(TOKEN_METADATAS)

    start_get_token_price_threads(TOKEN_METADATAS, MORALIS_API_KEY)


if __name__ == "__main__":
    main()
