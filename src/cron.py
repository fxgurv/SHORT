import os
import sys
from status import *
from cache import get_accounts
from config import get_verbose
from classes.YouTube import YouTube

def main():
    account_id = str(sys.argv[1])  # Now first argument is account_id directly
    verbose = get_verbose()
    accounts = get_accounts("youtube")

    if not account_id:
        error("Account UUID cannot be empty.")
        sys.exit(1)

    for acc in accounts:
        if acc["id"] == account_id:
            if verbose:
                info("Initializing YouTube...")
            youtube = YouTube(
                acc["id"],
                acc["name"],
                acc["profile_path"],
                acc["niche"],
                acc["language"]
            )
            youtube.generate_video()
            youtube.upload_video()
            if verbose:
                success("Uploaded Short.")
            break

if __name__ == "__main__":
    main()
