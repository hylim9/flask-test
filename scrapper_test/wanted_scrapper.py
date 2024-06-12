from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)  # initialize browser

# browser = p.chromium.launch() # headless=True 시 실패.

page = browser.new_page()

# page.goto("https://www.wanted.co.kr")  # headless mode (내부적 실행)
page.goto("https://www.wanted.co.kr/search?query=python&tab=position")

# time.sleep(3)

# page.click("button.Aside_searchButton__rajGo")

# time.sleep(3)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")

# time.sleep(3)

# page.keyboard.down("Enter")

# time.sleep(5)

# page.click("a#search_tab_position")


for x in range(5):
    time.sleep(3)
    page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__REty8")

jobs_list = []
for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__HBpZf").text
    company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
    reward = job.find("span", class_="JobCard_reward__cNlG5").text

    job_dict = {
        "title": title,
        "company_name": company_name,
        "reward": reward,
        "link": link,
    }
    jobs_list.append(job_dict)

file = open("jobs.csv", "w")

writer = csv.writer(file)

writer.writerow(jobs_list[0].keys())  # header

for job in jobs_list:
    writer.writerow(job.values())

file.close()
# print(jobs_list)
# print(len(jobs_list))

# page.screenshot(path="screenshot.png")
