new line(s) to replace

    start = job["started_at"]
    end = job["completed_at"]

    start_datetime = date_parser.parse(start)
    end_datetime = date_parser.parse(end)

    duration_in_min = round((end_datetime - start_datetime).total_seconds() / 60.0)

    job_info["started_at"] = start
    job_info["completed_at"] = end
    job_info["duration"] = duration_in_min

    return job_info


def get_job_time(workflow_run_id, token=None):
    job_time = get_job_time(args.workflow_run_id)
    job_time = dict(sorted(job_time.items(), key=lambda item: item[1]["duration"], reverse=True))

    for k, v in job_time.items():
        print(f'{k}: {v["duration"]}')
