import os
import zipfile

from utils.extract_warnings import extract_warnings_from_single_artifact


def handle_warnings(artifact_path, targets):
    selected_warnings = set()

    def parse_line(fp):
        # Implementation details of parse_line function
        # ...

    if from_gh:
        for filename in os.listdir(artifact_path):
            file_path = os.path.join(artifact_path, filename)
            if not os.path.isdir(file_path):
                if filename != "warnings.txt":
                    continue
                with open(file_path) as fp:
                    parse_line(fp)
    else:
        try:
            with zipfile.ZipFile(artifact_path) as z:
                for filename in z.namelist():
                    if not os.path.isdir(filename):
                        if filename != "warnings.txt":
                            continue
                        with z.open(filename) as fp:
                            parse_line(fp)
        except Exception:
            logger.warning(
                f"{artifact_path} is either an invalid zip file or something else wrong. This file is skipped."
            )

    return sorted(selected_warnings)
