import math

import requests


def get_job_links(workflow_run_id, token=None):
    headers = None
    if token is not None:
        headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}

    url = f"https://api.github.com/repos/huggingface/transformers/actions/runs/{workflow_run_id}/jobs?per_page=100"
    result = requests.get(url, headers=headers).json()
    job_links = {}

    try:
        job_links.update({job["name"]: job["html_url"] for job in result["jobs"]})
        pages_to_iterate_over = math.ceil((result["total_count"] - 100) / 100)

        for i in range(pages_to_iterate_over):
            result = requests.get(url + f"&page={i + 2}", headers=headers).json()
            job_links.update({job["name"]: job["html_url"] for job in result["jobs"]})

        return job_links
    except Exception:
        print(f"Unknown error, could not fetch links:\n{traceback.format_exc()}")

    return {}


def get_artifacts_links(workflow_run_id, token=None):
    headers = None
    if token is not None:
        headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}

    url = f"https://api.github.com/repos/huggingface/transformers/actions/runs/{workflow_run_id}/artifacts?per_page=100"
    result = requests.get(url, headers=headers).json()
    artifacts = {}

    try:
        artifacts.update({artifact["name"]: artifact["archive_download_url"] for artifact in result["artifacts"]})
        pages_to_iterate_over = math.ceil((result["total_count"] - 100) / 100)

        for i in range(pages_to_iterate_over):
            result = requests.get(url + f"&page={i + 2}", headers=headers).json()
            artifacts.update({artifact["name"]: artifact["archive_download_url"] for artifact in result["artifacts"]})

        return artifacts
    except Exception:
        print(f"Unknown error, could not fetch links:\n{traceback.format_exc()}")

    return {}
