from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import termcolor
import argparse
from os import system
import time
from alive_progress import alive_bar


def get_TLDS():
    with open("emailTLDS.txt", "r") as file:
        tlds = file.readlines()
        file.close()
    return tlds

SAVE = False

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="Specify the target url you want to scan!")
    parser.add_argument("-sf", "--save-file", dest="file_name", help="Specify file name if you want to save it. defualt is None.", default=None)
    parser.add_argument("-c", "--count", dest="count", help="Specify the number of URLs you want to scan. defualt is 100.", default=100)
    parser.add_argument("-v", "--verbose", dest="verbose", help="Specify if you want to see output. defualt is False.", default=False, action="store_true")
    parser.add_argument("-ce", "--check-email", dest="check", help="Specify if you want to check for invalid emails. defualt is False.", default=False, action="store_true")
    opt = parser.parse_args()
    return opt.url, opt.file_name, opt.count, opt.verbose, opt.check


url, file_name, COUNT, verbose, check = get_args()
url, file_name, COUNT, check = str(url), str(file_name), int(COUNT), bool(check)

if url == "None":
    user_url = str(input("[?] Enter Target URL To Scan >>  "))

else:
    user_url = url

if file_name != "None":
    SAVE = True

urls = deque([user_url])
scraped_urls = set()
emails = set()

count = 0
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

print(termcolor.colored("[!] Running...", "green"))
try:
    tlds = get_TLDS()
    with alive_bar() as bar:
        while len(urls):
            count += 1
            if count == COUNT:
                break
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)

            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            try:
                response = requests.get(url)
                if response.status_code == 404:
                    print(f"The URL {url} is not valid.")
            except (
                    requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,
                    requests.exceptions.InvalidSchema):
                continue
            new_emails = set(re.findall(regex, response.text, re.I))
            if check:
                new_real_emails = []
                for e in new_emails:
                    for tld in tlds:
                        tld = tld.strip().replace(" ", "").lower()
                        if str(e).endswith(tld) and not str(e).endswith("jpg") and not str(e).endswith("png"):
                            new_real_emails.append(e)
                            break
                new_emails = set(new_real_emails)
            emails.update(new_emails)

            soup = BeautifulSoup(response.text, features="lxml")

            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif link.startswith('http'):
                    link = link
                elif "php" in link or "html" in link:
                    link = base_url +"/"+link
                if not link in urls and not link in scraped_urls:
                    urls.append(link)
            bar()
except KeyboardInterrupt:
    print(termcolor.colored('[!] Closing...', 'red'))

print("100.0%")
time.sleep(1.2)
# system("cls")
print(f"[*] {len(emails)} Emails found.")
if SAVE:
    file = open(file_name, 'w')
    for mail in emails:
        if verbose:
            print(mail)
        file.write(mail+"\n")
    file.close()
else:
    for mail in emails:
        print(termcolor.colored(mail, 'blue'))


if SAVE:
    print(termcolor.colored("[!] Done!","green"))
    print(termcolor.colored(f"[!] Saved to {file_name}","green"))
    print(termcolor.colored("[!] Closed.", 'red'))
else:
    input("Enter to clear and close >> ")
    system("cls")
    print(termcolor.colored("[!] Done!","green"))
    print(termcolor.colored("[!] Closed.", 'red'))
exit(0)
