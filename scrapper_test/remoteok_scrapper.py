import requests
from bs4 import BeautifulSoup


class JobPosition:
    def __init__(self, title, company, position, region, url):
        self.title = title
        self.company = company
        self.position = position
        self.region = region
        self.url = url

    def __str__(self):
        return f"Title: {self.title}\tCompany: {self.company}\tLocation: {self.region}\tURL: {self.url}"


def get_jobs(keyword):
    response = requests.get(
        f"https://remoteok.com/remote-{keyword}-jobs",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")

    all_jobs = []
    for job in jobs:
        company_info = job.find("td", class_="company")
        title = company_info.find("a").text.strip()
        url = company_info.find("a")["href"]
        company = company_info.find("span", class_="companyLink").text.strip()
        region = company_info.find_all("div", class_="location")[0].text.strip()
        tags = job.find("td", class_="tags").find_all("a")[0:3]
        job_tags = []
        for tag in tags:
            job_tags.append(tag.text.strip())

        job_position = JobPosition(title, company, ", ".join(job_tags), region, url)
        print(job_position.position)
        all_jobs.append(job_position)

    return all_jobs


keywords = ["python", "golang", "reactjs"]
keyword_jobs = {}

for keyword in keywords:
    keyword_jobs[keyword] = get_jobs(keyword)
    print(len(keyword_jobs[keyword]))
# print(response.status_code)
# print(response.content)
