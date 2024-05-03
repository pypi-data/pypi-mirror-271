from requests.structures import CaseInsensitiveDict
from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class DownloadJobInstanceLogs:
    def get_job_instance_log_records(job_id, log_type):
        url = f"{config.YEEDU_RESTAPI_URL}/spark/job/{job_id}/log/{log_type}"
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, stream=True, verify=False)

            if (response.status_code == 200 and CaseInsensitiveDict(response.headers).get('Content-Type') == 'text/plain' and CaseInsensitiveDict(response.headers).get('Content-disposition')):
                try:
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            logger.info(line)

                    return True, response.status_code

                except Exception as e:
                    logger.exception(
                        f"Failed to get spark job instance logs due to : {e}")
                    sys.exit(-1)
            else:
                return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
