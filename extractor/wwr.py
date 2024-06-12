import requests
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    all_jobs = []

    print(f"scrapping {keyword}...")
    url = f"https://weworkremotely.com/remote-{keyword}-jobs"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    try:
        jobs = soup.find("section", class_="jobs").find_all("li")[0:-1]

        for job in jobs:
            title = job.find("span", class_="title").text
            company, position, region = job.find_all("span", class_="company")[0:3]
            # url = job.find("a")
            url = job.find("div", class_="tooltip--flag-logo").next_sibling.get(
                "href", None
            )
            job_data = {
                "title": title,
                "company": company.text,
                "position": position.text,
                "region": region.text,
                "url": (
                    f"https://weworkremotely.com{url}"
                    if url
                    else "https://weworkremotely.com"
                ),
            }
            all_jobs.append(job_data)

    except Exception:
        pass

    return all_jobs


# extract_wwr_jobs("python")
