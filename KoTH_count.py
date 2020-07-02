#!/bin/python3
import requests
import sys
import time
from multiprocessing.pool import Pool
from tqdm import tqdm

def req_koth_data(match_number):

    session = requests.Session()
    data = session.get(base + str(match_number)).text
    if '"gameType":"private"' not in data:
        if f'"username":"{user}"' in data:
            return match_number
        else:
            return ""


if __name__ == '__main__':
    if len(sys.argv) == 2:
        base = "https://tryhackme.com/games/koth/data/"
        print("""
           =================================================
            King of the hill matches counter for TryHackMe.
            Created by: Mr.Holmes

             P.S. This doesn't count Private games.
           =================================================
            """)
        user = sys.argv[1]
        print("Fetching last game played on TryHackMe...")
        last_game = requests.get(
            "https://tryhackme.com/games/koth/recent/games").text.split(",")[1].split(":")[1]
        print("Done.")
        print("""Checking all games.... (It's not that slow.)
If you feel it's too slow, then you can edit the code to increase number of processes. ;)\n""")
        temp_list = []
        for i in range(23, int(last_game)):
            temp_list.append(i)

        pool = Pool(processes=50)
        start = time.time()
        pool_outputs = list(
            tqdm(pool.imap(req_koth_data, temp_list), total=(len(temp_list) - 23)))
        end = time.time()
        # Filtering None returns
        final_result = []
        for i in pool_outputs:
            if i in temp_list:
                final_result.append(i)

        print(f"Number of matches {user} have played: ")
        for i in final_result:
            print(i, end=", ")
        print(f"\nTotal public matches played: {len(final_result)}")
        print(f"\nTime taken: {end-start} seconds.")
    else:
        print('''
            Uh Uh cannot detect any username.
            Usage:
            python3 KoTH_count.py <USERNAME>
            OR
            ./KoTH_count.py <USERNAME>
            ''')
