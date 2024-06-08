# Solana Token and Wallet Tracker

## Table of Contents

- [Solana Token and Wallet Tracker](#solana-token-and-wallet-tracker)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
      - [Using Conda](#using-conda)
  - [Installation](#installation)
    - [Step 1: Install Python 3.10](#step-1-install-python-310)
    - [Step 2: Clone the Repository](#step-2-clone-the-repository)
    - [Step 3: Install Dependencies](#step-3-install-dependencies)
    - [Step 4: Environment Variables](#step-4-environment-variables)
    - [Step 5: Moralis](#step-5-moralis)
    - [Step 5: Shyft](#step-5-shyft)
    - [Step 6: Constant Params](#step-6-constant-params)
  - [Running Scripts](#running-scripts)
    - [Running Token Tracker](#running-token-tracker)
    - [Running Wallet Tracker](#running-wallet-tracker)

## Introduction

Solana Token and Wallet Tracker

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Anaconda or Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

#### Using Conda

1. Open your terminal (or Anaconda Prompt if you are on Windows).
2. Create a new Conda environment with Python 3.10:
   ```sh
   conda create --name myenv python=3.10
   ```
3. Activate the environment:
   ```sh
   conda activate myenv
   ```

## Installation

### Step 1: Install Python 3.10

You need Python 3.10 to run this project. You can install it via Anaconda or Miniconda.

### Step 2: Clone the Repository

Clone this repository to your local machine using:

```sh
git clone git@github.com:SaudxInu/solana_token_and_wallet_tracker.git
```

```sh
cd solana_token_and_wallet_tracker
```

### Step 3: Install Dependencies

```sh
conda create --name solana_token_wallet_tracker python=3.10
```

```sh
conda activate solana_token_wallet_tracker
```

```sh
pip install -r requirements.txt
```

### Step 4: Environment Variables

You need to create a environment variable file named .env which will contain all your secrets and api keys.

Create a new file named .env in the root directory of the project. Add one environment variable per line. For example:

```.env
API_KEY=XXXX
```

### Step 5: Moralis

Please create an account on [Moralis](https://moralis.io/), copy your api key and add it to .env file. For example,

```.env
MORALIS_API_KEY=<your_moralis_api_key>
```

### Step 5: Shyft

Please create an account on [Shyft](https://shyft.to/), copy your api key and add it to .env file. For example,

```.env
SHYFT_API_KEY=<your_shyft_api_key>
```

### Step 6: Constant Params

Tp avoid rate limits, concurrent rate limits, compute budget of RPC and storage budget of machines on which the scripts will be running we have set some constant params for the scripts.

Please check out,

```txt
utils/constants.py
```

It contains the following to variables,

```txt
DELAY = 60
LAST_K_TXS = 25
```

You can change these params according to your own Moralis and Shyft accounts RPC limits.

## Running Scripts

Please note that we are not doing any input validation so it is your responsibilty to pass correct inputs.

### Running Token Tracker

You need to create a file named token_addresses.txt which will contain the input data. Each line in this file should represent a token address.

Create a new file named token_addresses.txt in the root directory of the project. Add the token addresses, one per line. For example:

```txt
4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R
7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr
9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E
2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk
3S8qX1MsMqRbiwKg2cQyx7nis1oHMgaCuc9c4VfvVdPN
F9CpWoyeBJfoRB8f2pBe2ZNPbPsEE76mWZWme3StsvHK
HaP8r3ksG76PhQLTqR8FYBeNiQpejcFbQmiHbg787Ut1
DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
8FU95xFJhUUkyyCLU13HSzDLs7oC4QZdXQHL6SCeab36
EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm
```

To start the token tracker script please run the following command,

```sh
python token_tracker.py
```

### Running Wallet Tracker

You need to create a file named wallets.txt which will contain the input data. Each line in this file should represent a wallet address and name.

Create a new file named wallets.txt in the root directory of the project. Add the wallets, one per line. For example:

```txt
2Em76UkVmchjPd4F56RU7WVsFUtaryzzZHsHja8PWxBd,A
6o5v1HC7WhBnLfRHp8mQTtCP2khdXXjhuyGyYEoy2Suy,B
2W1VbazcNPxyMYAVebPac1zk1cvPXkujnPEby9JnC64Z,C
```

To start the wallet tracker script please run the following command,

```sh
python wallet_tracker.py
```
