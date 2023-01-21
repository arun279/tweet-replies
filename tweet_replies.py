import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import os
import configparser
import argparse

class TweetReplies:
    def __init__(self, url, content_file=None, tweet_file=None, headless=None):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if url is None:
            raise ValueError("A url must be provided")
        self.url = url
        if not re.match(r"https://twitter.com/\w+/status/\d+", self.url):
            raise ValueError("Invalid Twitter URL")
        self.content_file = content_file or self.config['DEFAULT']['content_file']
        if not os.path.isfile(self.content_file):
            os.makedirs(os.path.dirname(self.content_file), exist_ok=True)
            open(self.content_file, 'a').close()
        self.tweet_file = tweet_file or self.config['DEFAULT']['tweet_file']
        if not os.path.isfile(self.tweet_file):
            os.makedirs(os.path.dirname(self.tweet_file), exist_ok=True)
            open(self.tweet_file, 'a').close()
        self.headless = headless or self.config.getboolean('DEFAULT', 'headless', fallback=False)


    def setup_selenium(self):
        self.options = webdriver.ChromeOptions()
        if self.headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-notifications")   
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def extract_handle(self, reply_div: str) -> str:
        handle = None
        try:
            soup = BeautifulSoup(reply_div, 'html.parser')
            handle_div = soup.select_one(".css-901oao.r-1bwzh9t.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0")
            handle = handle_div.select_one("a span").get_text()
        except Exception as e:
            pass
        return handle

    def extract_content(self, reply_div: str) -> str:
        content = None
        try:
            soup = BeautifulSoup(reply_div, 'html.parser')
            content_div = soup.select_one(".css-901oao.r-1nao33i.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0")
            content = content_div.get_text()
        except Exception as e:
            pass
        return content

    def extract_url(self, reply_div: str) -> str:
        soup = BeautifulSoup(reply_div, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            match = re.search(r"https://t\.co/\w+", a['href'])
            if match:
                links.append(match.group())
        return ', '.join(set(links))

    def extract_data_from_csv(self):
        data = []
        if os.path.isfile(self.content_file) and os.stat(self.content_file).st_size != 0:
            with open(self.content_file, 'r', encoding='utf-8') as file:
                data = self.process_csv()
        else:
            self.setup_selenium()
            self.driver.get(self.url)
            self.scroll_load()
            data = self.process_csv()
        return data

    def process_csv(self):
        data = []
        with open(self.content_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) # skip the header
            for row in csv_reader:
                tweet_id = row[0]
                tweet_div = row[1]
                handle = self.extract_handle(tweet_div)
                content = self.extract_content(tweet_div)
                url = self.extract_url(tweet_div)
                if handle and content and url:
                    tweet_link = "https://twitter.com/{handle}/status/{tweet_id}".format(handle=handle, tweet_id=tweet_id)
                    data.append({"handle": handle, "content": content, "url": url, "tweet": tweet_link})
                else:
                    continue
        return data

    def scroll_load(self):
        tweets = {}
        last_height = self.driver.execute_script("return Math.max( document.body.scrollHeight);")
        while True:
            # Scroll down to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for the page to load
            time.sleep(2)
            # Get all the tweet divs on the page
            tweet_divs = self.driver.find_elements(By.CSS_SELECTOR, ".css-1dbjc4n.r-1igl3o0.r-qklmqi.r-1adg3ll.r-1ny4l3l")
            # Iterate over the tweet divs
            for tweet_div in tweet_divs:
                # Get the tweet id
                tweet_id = None
                for a in tweet_div.find_elements(By.CSS_SELECTOR, "a"):
                    if 'status' in a.get_attribute("href"):
                        tweet_id = a.get_attribute("href").split("/")[-1]
                        break
                # If the tweet id is not already in the dictionary, add it to the dictionary
                if tweet_id is not None and tweet_id not in tweets:
                    tweets[tweet_id] = tweet_div.get_attribute("innerHTML")
            # Check if the new height is the same as the last height
            new_height = self.driver.execute_script("return Math.max( document.body.scrollHeight);")
            if new_height == last_height:
                break
            last_height = new_height
        # Write the tweets to a CSV file
        with open(self.content_file, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["tweet_id", "tweet_div"])
            for tweet_id, tweet_div in tweets.items():
                csv_writer.writerow([tweet_id, tweet_div])

    def start(self):
        tweet_data = self.extract_data_from_csv()
        with open(self.tweet_file, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=["handle", "content", "url", "tweet"])
            csv_writer.writeheader()
            csv_writer.writerows(tweet_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="The twitter status url")
    parser.add_argument("--content_file", type=str, help="The content file", default=None)
    parser.add_argument("--tweet_file", type=str, help="The tweet file", default=None)
    parser.add_argument("--headless", type=str, help="The headless", default=None)
    args = parser.parse_args()
    tweet_replies = TweetReplies(args.url, args.content_file, args.tweet_file, args.headless)
    tweet_data = tweet_replies.extract_data_from_csv()
    with open(tweet_replies.tweet_file, 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=["handle", "content", "url", "tweet"])
        csv_writer.writeheader()
        csv_writer.writerows(tweet_data)
