import csv


def save_to_csv(file_name, jobs):
    file = open(f"{file_name}.csv", "w")
    writer = csv.writer(file)

    writer.writerow(jobs[0].keys())  # header

    for job in jobs:
        writer.writerow(job.values())

    file.close()

    # file.write("Title,Company,Position,Region,URL\n")

    # for job in jobs:
    #     file.write(
    #         f"{job['title']},{job['company']},{job['position']},{job['region']},{job['url']}\n"
    #     )
    # file.close()
