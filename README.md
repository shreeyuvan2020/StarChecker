# Star Checker

###### A web scraper that lets you know when someone stars or unstars one of your Summer of Making devlogs!

## Features:
- Uses ntfy.sh to send notifications
- Uses Selenium and Beautiful Soup for web scraping
- Gets cookies from the user by asking for them

## Usage:
### pip (Recommended)
- Before installing via pip, log in or create an account at ntfy.sh and subscribe to the topic "Devlog_Stars"
- Then run `pip install StarChecker` in the terminal
- You might need to use `pip3 install StarChecker` on some systems
- Then when someone stars your project you should see which devlog is starred in which project in that topic in ntfy.sh
