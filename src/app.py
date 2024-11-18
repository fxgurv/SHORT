import os
import json
import schedule
import subprocess
import threading
from uuid import uuid4
from termcolor import colored
from classes.YouTube import YouTube
from prettytable import PrettyTable
from flask import Flask, jsonify, request
from cache import get_accounts, add_account, remove_account
from utils import rem_temp_files
from config import ROOT_DIR, get_verbose
from status import info, warning, success, error, question
from constants import SHORTS_MENU, CRON_MENU

app = Flask(__name__)

@app.route('/')
def home():
    with open('Index.html', 'r') as f:
        return f.read()

@app.route('/api/accounts')
def get_youtube_accounts():
    accounts = get_accounts("youtube")
    return jsonify(accounts)

@app.route('/api/account', methods=['POST'])
def add_youtube_account():
    data = request.json
    new_account = {
        "id": str(uuid4()),
        "nickname": data['nickname'],
        "firefox_profile": data['firefox_profile'],
        "niche": data['niche'],
        "language": data['language'],
        "videos": []
    }
    add_account("youtube", new_account)
    return jsonify({"status": "success", "account": new_account})

@app.route('/api/account/<id>', methods=['DELETE'])
def remove_youtube_account(id):
    remove_account("youtube", id)
    return jsonify({"status": "success"})

@app.route('/api/generate/<id>')
def generate_video(id):
    accounts = get_accounts("youtube")
    account = next((acc for acc in accounts if acc["id"] == id), None)
    if account:
        youtube = YouTube(
            account["id"],
            account["nickname"],
            account["firefox_profile"],
            account["niche"],
            account["language"]
        )
        youtube.generate_video()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Account not found"})

@app.route('/api/cron/<id>', methods=['POST'])
def setup_cron(id):
    data = request.json
    schedule_type = data['schedule_type']
    accounts = get_accounts("youtube")
    account = next((acc for acc in accounts if acc["id"] == id), None)
    if account:
        cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
        command = f"python {cron_script_path} youtube {account['id']}"
        
        def job():
            subprocess.run(command)
            
        if schedule_type == "daily":
            schedule.every(1).day.do(job)
        elif schedule_type == "twice":
            schedule.every().day.at("10:00").do(job)
            schedule.every().day.at("16:00").do(job)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Account not found"})

def main():
    info("Starting YouTube automation")
    cached_accounts = get_accounts("youtube")

    if len(cached_accounts) == 0:
        warning("No accounts found. Create one? (y/n)")
        user_input = question("y/n: ")

        if user_input.lower() == "y":
            generated_uuid = str(uuid4())
            nickname = question("Enter account nickname: ")
            fp_profile = question("Enter Firefox profile path: ")
            niche = question("Enter account niche: ")
            language = question("Enter account language: ")

            add_account("youtube", {
                "id": generated_uuid,
                "nickname": nickname,
                "firefox_profile": fp_profile,
                "niche": niche,
                "language": language,
                "videos": []
            })
            success(f"Added new account: {nickname}")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "UUID", "Nickname", "Niche"]

        for account in cached_accounts:
            table.add_row([
                cached_accounts.index(account) + 1, 
                colored(account["id"], "cyan"),
                colored(account["nickname"], "blue"),
                colored(account["niche"], "green")
            ])

        print(table)
        user_input = question("Select account: ")
        selected_account = cached_accounts[int(user_input) - 1]

        youtube = YouTube(
            selected_account["id"],
            selected_account["nickname"],
            selected_account["firefox_profile"],
            selected_account["niche"],
            selected_account["language"]
        )

        while True:
            rem_temp_files()
            print("\n=== YouTube Menu ===")
            for idx, option in enumerate(SHORTS_MENU):
                print(colored(f"{idx + 1}. {option}", "cyan"))

            choice = int(question("Select option: "))

            if choice == 1:
                youtube.generate_video()
                if question("Upload to YouTube? (y/n): ").lower() == "y":
                    youtube.upload_video()
            elif choice == 2:
                videos = youtube.get_videos()
                if videos:
                    videos_table = PrettyTable()
                    videos_table.field_names = ["ID", "Date", "Title"]
                    for video in videos:
                        videos_table.add_row([
                            videos.index(video) + 1,
                            colored(video["date"], "blue"),
                            colored(video["title"][:60] + "...", "green")
                        ])
                    print(videos_table)
                else:
                    warning("No videos found")
            elif choice == 3:
                setup_cron_job(youtube, selected_account)
            elif choice == 4:
                break

def setup_cron_job(youtube, account):
    print("\n=== Schedule Options ===")
    for idx, option in enumerate(CRON_MENU):
        print(colored(f"{idx + 1}. {option}", "cyan"))

    choice = int(question("Select option: "))
    cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
    command = f"python {cron_script_path} youtube {account['id']}"

    def job():
        subprocess.run(command)

    if choice == 1:
        schedule.every(1).day.do(job)
        success("Set daily upload schedule")
    elif choice == 2:
        schedule.every().day.at("10:00").do(job)
        schedule.every().day.at("16:00").do(job)
        success("Set twice daily upload schedule")

if __name__ == "__main__":
    info("Starting YouTube automation system")
    server = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 7860})
    server.daemon = True
    server.start()
    info("WebUI started at http://localhost:7860")

    while True:
        main()
