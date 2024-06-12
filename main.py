from flask import Flask, render_template, request, redirect, send_file
from extractor.remoteok import extract_remoteok_jobs
from extractor.wwr import extract_wwr_jobs
from file import save_to_csv
import os

app = Flask("JobScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html", name="Chloe")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        remoteok = extract_remoteok_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = remoteok + wwr

        db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")

    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_csv(keyword, db[keyword])

    result = send_file(f"{keyword}.csv", as_attachment=True)

    if result.status_code == 200:
        os.remove(f"{keyword}.csv")  # 파일 다운로드 성공 시 생성 파일 삭제

    return result


app.run("127.0.0.1", debug=True)
