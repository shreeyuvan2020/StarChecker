from bs4 import BeautifulSoup
from src.StarChecker.ChangeCheck import star_check
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import InvalidSessionIdException
def main():
    user_cookies = input("Enter the cookie value for _journey_session in your broswer in summer.hackclub.com. Do this by opening DevTools and then going to Storage and then _journey_session should be there in Cookies. Copy the value and paste it here: ")
    def create_driver(user_cookies):
        options = ChromeOptions()
        options.add_argument("--headless=new")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://summer.hackclub.com")
        driver.add_cookie({"name": "_journey_session", "value": f"{user_cookies}"})
        return driver

    driver = create_driver(user_cookies)
    some_url = "https://summer.hackclub.com/my_projects"
    driver.get(some_url)
    current = driver.page_source
    star_dictionary = {}
    soup = BeautifulSoup(current, "html.parser")
    projects = soup.select_one('div[class^="grid"]')
    links = projects.find_all('a')
    while True:
        time.sleep(60)
        for link in links:
            href = link.get('href')
            if href:
                try:
                    star_pairs = star_check(f"https://summer.hackclub.com/{href}", driver)
                except InvalidSessionIdException:
                    print("Session lost, creating new driver")
                    driver = create_driver()
                    star_pairs = star_check(f"https://summer.hackclub.com/{href}", driver)
                for star_pair in star_pairs:
                    if star_pair:
                        if not star_dictionary:
                            star_dictionary[star_pair[0]] = int(star_pair[1])
                        else:
                            if star_pair[0] in star_dictionary:
                                if star_dictionary[star_pair[0]] != int(star_pair[1]):
                                    diff = int(star_pair[1]) - star_dictionary.get(star_pair[0])
                                    number = star_pair[0]
                                    if int(number) == 1:
                                        number = number + "st"
                                    elif int(number) == 2:
                                        number = number + "nd"
                                    elif int(number) == 3:
                                        number = number + "rd"
                                    else:
                                        number = number + "th"
                                    requests.post("https://ntfy.sh/Devlog_Stars", data=f"Star count changed for {star_pair[0]} devlog in project {star_pair[2]} by {diff} stars".encode(encoding='utf-8'))
                                    star_dictionary[star_pair[0]] = int(star_pair[1])

                            else:
                                star_dictionary[star_pair[0]] = int(star_pair[1])
if __name__ == "__main__":
    main()