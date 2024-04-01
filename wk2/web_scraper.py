#!/usr/bin/env python3
import requests
import os
from bs4 import BeautifulSoup
import subprocess

def save_file(content):
    save = temp = "results"
    i = 0
    while os.path.exists(temp) and os.path.isdir(temp):
        i += 1
        temp = save + str(i)
    save = temp
    os.makedirs(save)
    os.chdir(save)
    with open('result.html', 'w') as result_file:
        result_file.write(response.text)
    print(f"Success! Results saved to {save}/results.html")

def print_content(content):
    print("Pretty print content? (leave blank for no)")
    selected_format = input()
    if selected_format != "":
        soup = BeautifulSoup(content, 'html.parser')
        lines = soup.get_text()
        print(lines)
    else:
        print(content)

website = input("Enter the website that you would like to scrape: ")

if not website.startswith("https://"):
    website = "https://" + website

print("Now visiting", website)

try:
    response = requests.get(website)
    if response.status_code == 200:
        print("Visit successful! Scrape subdomains with GoBuster? [Y] for yes, default response is no.")
        scrape = input()
        if scrape == "Y":
            print("Running GoBuster, this could take a while...")
            command = [
                'gobuster',
                'dns',
                '-qd', website,
                '-w', 'subdomains-top1mil-20000.txt'
            ]
            subprocess.run(command, check=True)
        print("Enter SAVE to save content to files. Enter PRINT to echo them directly.")
        user_input = input()
    if user_input == "SAVE":
        save_file(response.text)
        exit()
    elif user_input == "PRINT":
        print_content(response.text)
        exit()
    else:
        print("Error: invalid option. Exiting...")
        exit()
except requests.exceptions.RequestException as e:
    print(f"Error making the request: {e}")
    print("Did you enter a valid URL?")