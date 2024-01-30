# Remove or comment out the section of code executed when the script is run directly
# if __name__ == "__main__":
#     r"""
#     Example:
#
#         python get_github_job_time.py --workflow_run_id 2945609517
#     """
#
#     parser = argparse.ArgumentParser()
#     # Required parameters
#     parser.add_argument("--workflow_run_id", type=str, required=True, help="A GitHub Actions workflow run id.")
#     args = parser.parse_args()
#
#     job_time = get_job_time(args.workflow_run_id)
#     job_time = dict(sorted(job_time.items(), key=lambda item: item[1]["duration"], reverse=True))
#
#     for k, v in job_time.items():
#         print(f'{k}: {v["duration"]}')
    except Exception:
        print(f"Unknown error, could not fetch links:\n{traceback.format_exc()}")

    return {}


if __name__ == "__main__":
    r"""
    Example:

        python get_github_job_time.py --workflow_run_id 2945609517
    """

    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument("--workflow_run_id", type=str, required=True, help="A GitHub Actions workflow run id.")
    args = parser.parse_args()

    job_time = get_job_time(args.workflow_run_id)
    job_time = dict(sorted(job_time.items(), key=lambda item: item[1]["duration"], reverse=True))

    for k, v in job_time.items():
        print(f'{k}: {v["duration"]}')
