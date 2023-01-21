# Tweet Replies With Links

This script allows you to retrieve all the replies to a specified Tweet that contain URLs. For each reply, the handle, content, and URLs in the replies are extracted. The data is then stored in a CSV file. Only those tweets which have a URL in them are saved, others are ignored. The CSV can also be exported to a HTML file.

## Requirements

- Python 3.6 or later
- Selenium
- BeautifulSoup
- configparser
- csv
- os

You can install the dependencies by running:
```
pip install -r requirements.txt
```
This project uses setuptools for building and distributing the package. To build the package, you can use the following command:
```
python setup.py
```

## Configuration

Edit the `config.ini` file in the same directory as the script and specify the following parameters:
```
[DEFAULT]
content_file = <content_filename>.csv
tweet_file = <tweets_filename>.csv
output_html = <output_html_filename>.html
headless = False
```
- `content_file`: The name of the file where the extracted data will be stored
- `tweet_file`: The name of the file where the tweets will be stored
- `output_html`: The name of the file where the HTML table will be stored
- `headless`: If set to true, Selenium will run in headless mode (i.e. without a GUI). Headless mode currently does not work, it's a TODO for the future, so it has to be set to `False` for now.

## Usage

1. Run the script with the following command:
```
python tweet_replies.py <url-to-tweet>
```
The script will open the specified URL in a Selenium webdriver, scroll down to load more tweets and replies, and then extract the handle, content, and URLs of the tweets and replies. The extracted data will be stored in the specified CSV file.

If the `content_file` already exists, the script will read the data from the file and extract the handle, content, and URLs of tweets and replies, and store the data in a list of dictionaries.

2. Use the `csv_to_html.py` script to convert the `tweet_file` to an HTML table:
```
python csv_to_html.py
```

## Note

- Make sure you have Chrome browser installed in your machine.
- If you get any issue related to chrome driver, please download the chrome driver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it in your PATH, e. g., place it in /usr/bin or /usr/local/bin
- The generated HTML file uses DataTables and Materialize CSS for styling and functionality.