import requests
from bs4 import BeautifulSoup


def extract_remoteok_jobs(keyword):
    all_jobs = []

    response = requests.get(
        f"https://remoteok.com/remote-{keyword}-jobs",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")

        for job in jobs:
            company_info = job.find("td", class_="company")
            title = company_info.find("a").text.strip()
            # url = company_info.find("a")["href"]
            url = company_info.find("a").get("href", None)
            company = company_info.find("span", class_="companyLink").text.strip()
            region = company_info.find_all("div", class_="location")[0].text.strip()
            tags = job.find("td", class_="tags").find_all("a")[0:3]
            job_tags = []
            for tag in tags:
                job_tags.append(tag.text.strip())

            job_data = {
                "title": title,
                "company": company,
                "position": ", ".join(job_tags),
                "region": region,
                "url": f"https://remoteok.com{url}" if url else "https://remoteok.com",
            }
            all_jobs.append(job_data)

    except Exception:
        pass

    return all_jobs


# extract_remoteok_jobs("python")
