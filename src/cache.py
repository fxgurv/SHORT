import os
import json
from typing import List
from config import ROOT_DIR

def get_cache_path() -> str:
    return os.path.join(ROOT_DIR, '.mp')

def get_youtube_cache_path() -> str:
    return os.path.join(get_cache_path(), 'youtube.json')

def get_accounts() -> List[dict]:
    cache_path = get_youtube_cache_path()

    if not os.path.exists(cache_path):
        # Create the cache file
        with open(cache_path, 'w') as file:
            json.dump({
                "accounts": []
            }, file, indent=4)

    with open(cache_path, 'r') as file:
        parsed = json.load(file)

        if parsed is None:
            return []
        
        if 'accounts' not in parsed:
            return []

        # Get accounts dictionary
        return parsed['accounts']

def add_account(account: dict) -> None:
    # Get the current accounts
    accounts = get_accounts()

    # Add the new account
    accounts.append(account)

    # Write the new accounts to the cache
    with open(get_youtube_cache_path(), 'w') as file:
        json.dump({
            "accounts": accounts
        }, file, indent=4)

def remove_account(account_id: str) -> None:
    # Get the current accounts
    accounts = get_accounts()

    # Remove the account
    accounts = [account for account in accounts if account['id'] != account_id]

    # Write the new accounts to the cache
    with open(get_youtube_cache_path(), 'w') as file:
        json.dump({
            "accounts": accounts
        }, file, indent=4)
