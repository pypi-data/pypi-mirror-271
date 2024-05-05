import json
import logging
from typing import Optional
import requests

from pathlib import Path
from uploader.urls import ENDPOINT_UPLOAD_RESULTS, TESTPULSE_RECEIVER

from uploader.domain import TestRun

logger = logging.getLogger(__name__)

LOCAL_URL = 'http://127.0.0.1:8000'


def upload_test_results(zip: Path, test_run: TestRun) -> Optional[str]:
    files = {'file': open(zip, 'rb')}

    data = {
        "commit_id": test_run.commit,
        "repository": test_run.repository,
        "organization": test_run.organization,
        "github_run_id": test_run.github_run_id,
    }

    if test_run.test_configuration:
        data['test_configuration'] = json.dumps(test_run.test_configuration)

    if test_run.test_type:
        data['test_type'] = test_run.test_type

    headers = {
        "Authorization": f"Bearer {test_run.token}",
    }

    url = LOCAL_URL if test_run.localhost else TESTPULSE_RECEIVER
    url = url + ENDPOINT_UPLOAD_RESULTS

    logging.debug(f'Making request to {url}')

    req = requests.post(url=url,
                        files=files,
                        data=data,
                        headers=headers)
    if req.status_code != 200:
        logging.error(f'Something went wrong: {req.text}')
        return None

    response = req.json()

    if 'link' not in response:
        logging.error(f'Did not receive a valid response: {response}')
        return None

    return response['link']
