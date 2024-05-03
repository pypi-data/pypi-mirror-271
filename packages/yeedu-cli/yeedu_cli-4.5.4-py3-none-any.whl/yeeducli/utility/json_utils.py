from difflib import SequenceMatcher
from yeeducli.utility.logger_utils import Logger
from argparse import ArgumentTypeError
from yeeducli.constants import *
import pathlib
import json
import yaml
import sys

logger = Logger.get_logger(__name__, True)


def check_minimum(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ArgumentTypeError(
                f"--page_number value must be greater than 0")
        return ivalue
    except Exception as e:
        logger.error(e)
        sys.exit(-1)


def check_range(mini, maxi):
    try:
        def range_checker(arg):
            f = int(arg)
            if f < mini or f > maxi:
                raise ArgumentTypeError(
                    f"must be in range between [" + str(mini) + " .. " + str(maxi)+"]")
            return f
    except Exception as e:
        logger.error(e)
        sys.exit(-1)

    return range_checker


def change_output(json_data_payload):
    try:
        for k, v in dict(json_data_payload).items():
            if type(v) == list and k not in VARCHAR_ARRAY_COLUMN_FULL_LIST:
                json_data_payload[k] = json_data_payload.pop(k)[0]

                if str(v[0]).lower() == 'true':
                    json_data_payload[k] = True
                elif str(v[0]).lower() == 'false':
                    json_data_payload[k] = False
    except Exception as e:
        logger.error(e)
        sys.exit(-1)
    return json_data_payload


def trim_namespace_json(args):
    try:
        json_data = vars(args)

        if json_data["yeedu"] in ['configure', 'logout']:
            del json_data["yeedu"]
            return json_data

        del json_data["yeedu"]
        del json_data["subcommand"]

        return json_data
    except Exception as e:
        logger.error(e)
        sys.exit(-1)


def get_similar_subcommand(args_subcommand, list_of_subcommand):
    try:
        if args_subcommand is not None:
            list_of_similar_subcommand = []
            splitted_args_command = args_subcommand.split('-')
            for subcommand in list_of_subcommand:
                splitted_subcommand = subcommand.split('-')
                i = 0
                percentage_match = 0
                for each_splitted_args_command in splitted_args_command:
                    if i >= 0 and i < len(splitted_subcommand):
                        percentage_match += similar(
                            splitted_subcommand[i], each_splitted_args_command)
                        i += 1
                if percentage_match >= 1.21:
                    list_of_similar_subcommand.append(subcommand)
            if len(list_of_similar_subcommand) > 0:
                return f"Did you mean? {list_of_similar_subcommand}"
            else:
                return f"Cannot find the provided subcommand: {args_subcommand}"
        else:
            return list_of_subcommand
    except Exception as e:
        logger.error(e)
        sys.exit(-1)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def trim_network_config_json(args):

    json_data = vars(args)

    json_payload = json_data.copy()

    del json_payload["json_output"]
    del json_payload["yaml_output"]

    try:

        for k, v in dict(json_payload).items():

            if v is None:
                del json_payload[k]

            if all(key in json_payload for key in ('network_conf_id', 'cloud_provider_id')):
                del json_payload["network_conf_id"]
                del json_payload["cloud_provider_id"]
            else:
                pass

    except Exception as error:
        logger.error(f"Error while preparing Network Config payload: {error}")
        sys.exit(-1)

    return json_payload


def remove_output(args):
    json_data = vars(args)

    json_payload = json_data.copy()

    del json_payload["json_output"]
    del json_payload["yaml_output"]

    try:
        for k, v in dict(json_payload).items():
            if v is None:
                del json_payload[k]

        for k, v in dict(json_payload).items():

            if str(k) == "cluster_type":
                json_payload[k] = str(v[0]).upper()

            if str(k) in VARCHAR_ARRAY_COLUMN_LIST and len(str(v).split(",")) >= 1:
                json_payload[k] = str(v).split(",")

            if str(k) == "conf":
                json_payload[k] = conf_setter(v)

            if str(k) == "labels":
                json_payload[k] = labels_setter(v)

            if str(k) == "network_tags":
                if v == []:
                    pass
                else:
                    json_payload[k] = tags_validator(v)

            # if str(k) in JSON_ARGUMENTS_LIST:
            #     json_payload[k] = validateJSON(v)

            if str(k) == 'base64_encoded_credentials':
                credentials_json = {"encoded": str(v[0])}
                json_payload[k] = credentials_json

            if str(v).lower() == 'true':
                json_payload[k] = True
            elif str(v).lower() == 'false':
                json_payload[k] = False

            if all(key in json_payload for key in ('max_parallel_spark_job_execution_per_instance', 'standalone_workers_number')):

                engine_cluster_spark_config = {'engine_cluster_spark_config': {'max_parallel_spark_job_execution_per_instance': int(
                    json_payload['max_parallel_spark_job_execution_per_instance']), 'standalone_workers_number': int(json_payload['standalone_workers_number'])}}

                json_payload.update(engine_cluster_spark_config)

                del json_payload['max_parallel_spark_job_execution_per_instance']
                del json_payload['standalone_workers_number']

            elif set(['max_parallel_spark_job_execution_per_instance']).issubset(json_payload.keys()):

                engine_cluster_spark_config = {'engine_cluster_spark_config': {
                    'max_parallel_spark_job_execution_per_instance': int(json_payload['max_parallel_spark_job_execution_per_instance'])}}

                json_payload.update(engine_cluster_spark_config)

                del json_payload['max_parallel_spark_job_execution_per_instance']

            elif set(['standalone_workers_number']).issubset(json_payload.keys()):

                engine_cluster_spark_config = {'engine_cluster_spark_config': {
                    'standalone_workers_number': int(json_payload['standalone_workers_number'])}}

                json_payload.update(engine_cluster_spark_config)

                del json_payload['standalone_workers_number']

    except Exception as error:
        logger.error(f"Error while preparing payload: {error}")
        sys.exit(-1)

    return json_payload


def tags_validator(tagsString):
    # if (len(tagsString.split(",")) % 2 == 0):
    tagsList = []
    uniquetagList = []
    duplicatetagList = []

    for tag in tagsString.split(","):
        tagsList.append(str(tag))

    for eachTag in tagsList:
        if eachTag not in uniquetagList:
            uniquetagList.append(eachTag)
        else:
            duplicatetagList.append(eachTag)
    if len(duplicatetagList) > 0:
        logger.error(
            f"The duplicate values for --tags are: {duplicatetagList}")
        sys.exit(-1)

    return tagsList
    # else:
    #     logger.error(
    #         f"Invalid input for '--network_tags'\n\nVALID\n --network_tags={VALID_NETWORK_TAG}\nINVALID\n --network_tags={INVALID_NETWORK_TAG}")
    #     sys.exit(-1)


def validateJSON(jsonData):
    try:
        return json.loads(jsonData)
    except ValueError as err:
        logger.error(
            f"Invalid json string. \n\nVALID: The JSON data should be enclosed in single quotes.\n --jsonString={VALID_JSON}\nINVALID\n --jsonString={INVALID_JSON}")
        sys.exit(-1)


def conf_setter(conf):
    confList = []
    confListJSON = "{"
    conffLength = len(conf)

    for confValue in conf:
        if (len(confValue[0].split('=', maxsplit=1)) % 2 == 0):
            # if len(confValue[0].split(",")) > 1:
            #     logger.error(
            #         f"\nMultiple key=value pair detected in --conf='{confValue[0]}'.\n\nPlease provide a single key=value pair as --conf='key=value'")
            #     sys.exit(-1)
            # for confItem in confValue[0].split(","):

            confList.append(confValue[0])

            if conffLength == 1:
                confItem = '"' + confValue[0].replace("=", '":"', 1) + '"}'
                confListJSON = confListJSON + confItem
            else:
                confItem = '"' + confValue[0].replace("=", '":"', 1) + '",'
                confListJSON = confListJSON + confItem
            conffLength = conffLength-1
        else:
            logger.error(
                f"Invalid input for '--conf'\n\nVALID\n --conf1='key1=pair1'\n --conf2='key2=pair2'\nINVALID\n --conf1='key1=pair1'\n --conf2='key2'")
            sys.exit(-1)
    return_bool, return_value = json.loads(
        confListJSON, object_pairs_hook=check_duplicate_key)

    if return_bool:
        return confList
    elif (not return_bool) and (type(return_value) == dict):
        return_value = next(iter((return_value.items())))
        logger.error(
            f"\nThe provided --conf has duplicate key=value pair as '{return_value[0]}={return_value[1]}'.\n")
        sys.exit(-1)


def check_duplicate_key(ordered_pairs):
    """Reject duplicate keys."""
    result = {}
    for key, value in ordered_pairs:
        if key in result:
            return False, {key: value}
        else:
            result[key] = value
    return True, result


def labels_setter(labels):
    labelsList = "{"
    labelsLength = len(labels)
    for labelsValue in labels:
        if (len(labelsValue[0].split('=', maxsplit=1)) % 2 == 0):

            if len(labelsValue[0].split(",")) > 1:
                logger.error(
                    f"\nMultiple key=value pair detected in --labels='{labelsValue[0]}'.\n\nPlease provide a single key=value pair as --labels='key=value'")
                sys.exit(-1)

            for labelItem in labelsValue[0].split(","):
                if labelsLength == 1:
                    labelItem = '"' + \
                        labelsValue[0].replace("=", '":"', 1) + '"'
                    labelsList = labelsList + labelItem
                else:
                    labelItem = '"' + \
                        labelsValue[0].replace("=", '":"', 1) + '",'
                    labelsList = labelsList + labelItem
                labelsLength = labelsLength-1
        else:
            logger.error(
                f"Invalid input for '--labels'\n\nVALID\n --labels1='key1=pair1'\n --labels2='key2=pair2'\nINVALID\n --labels1='key1=pair1'\n --labels2='key2'")
            sys.exit(-1)

    labelsList = labelsList + '}'

    return_bool, return_value = json.loads(
        labelsList, object_pairs_hook=check_duplicate_key)
    if return_bool:
        return return_value
    elif (not return_bool) and (type(return_value) == dict):
        return_value = next(iter((return_value.items())))
        logger.error(
            f"\nThe provided --labels has duplicate key=value pair as '{return_value[0]}={return_value[1]}'.\n")
        sys.exit(-1)


def confirm_output(response_json, status_code, json_data):

    if status_code in [200, 201, 400, 401, 404, 409, 422]:

        if json_data["json_output"] == 'default':
            logger.info(response_json)

        elif json_data["yaml_output"] == 'true':
            logger.info(yaml.dump(response_json, indent=2, sort_keys=False))

        else:
            logger.info(json.dumps(response_json, indent=2))

    elif status_code in [204, 405, 403, 500]:

        logger.info(json.dumps(response_json, indent=2))


def response_validator(response):
    try:
        if response.status_code in [200, 201, 400, 401, 403, 404, 204, 405, 409, 422, 500]:
            return response.json(), response.status_code
        else:
            logger.error(
                f"Received BAD RESPONSE : '{response.text}'\nwith status code : {response.status_code}")
            sys.exit(-1)
    except ValueError:
        logger.error(
            f"Response JSON Decoding failed as \nResponse is : '{response.text}'\nStatus code : {response.status_code}")
        sys.exit(-1)


def response_json_custom_order(response_json, custom_response_order):
    try:
        sorted_list = []
        json_length = len(response_json)
        if isinstance(response_json, dict):
            return {key: response_json[key] for key in custom_response_order}
        else:
            for i in range(json_length):
                sorted_list.append(
                    {key: response_json[i][key] for key in custom_response_order})
            return sorted_list
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# ?engine_cluster_instance_status=INITIATING&engine_cluster_instance_status=RUNNING
def prepareQueryParamsForTypeArray(listOfStatus, pageNumber, limit):
    try:

        lengthOfStatus = len(listOfStatus)
        queryParams = ''

        for status in listOfStatus:
            if lengthOfStatus == 1:
                queryParams = queryParams + \
                    f"cluster_status={status}&pageNumber={pageNumber}&limit={limit}"
            else:
                queryParams = queryParams + \
                    f"cluster_status={status}&"
            lengthOfStatus = lengthOfStatus-1

        return queryParams

    except Exception as e:
        logger.error(f"Failed to prepare query params due to: {e}")
        sys.exit(-1)


def checkFilePathExists(file_path, argument):
    try:
        if (file_path != None and os.path.isfile(file_path)):
            return file_path

        elif (file_path == None):
            logger.error("Please provide a local file path\n")
            sys.exit(-1)
        else:
            file_error = {
                "error": f"The file cannot be found at '{file_path}' for the argument --{argument}"}
            logger.error(json.dumps(file_error, indent=2))
            sys.exit(-1)
    except Exception as e:
        logger.error(f"Failed to check file path exists due to: {e}")
        sys.exit(-1)


def checkUnixFileFormat(file_path):
    try:
        file_extension = pathlib.Path(file_path).suffix

        if file_extension == '.sh':
            return file_path
        else:
            file_error = {
                "error": f"File format of {file_path} is not UNIX"}
            logger.error(json.dumps(file_error, indent=2))
            sys.exit(-1)

    except Exception as e:
        logger.error(
            f"Failed to check file format for {file_path} due to: {e}")
        sys.exit(-1)


def readFileContent(file_path):
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
            f.close()
            return file_content

    except Exception as e:
        logger.error(
            f"Failed to read file content from {file_path} due to: {e}")
        sys.exit(-1)


def appendSheBang(file_content):
    try:
        if not file_content.startswith("#!/bin/bash"):
            return "#!/bin/bash\n\n" + file_content
        else:
            return file_content

    except Exception as e:
        logger.error(
            f"Failed due to: {e}")
        sys.exit(-1)


def createOrUpdateHiveMetastoreConfig(config):
    try:
        requestBody = {}

        columnAlias = {
            'hive_site_xml_file_path': 'hiveSiteXml',
            'core_site_xml_file_path': 'coreSiteXml',
            'hdfs_site_xml_file_path': 'hdfsSiteXml',
            'krb5_conf_file_path': 'krb5Conf'
        }

        for key, value in config.items():

            if isinstance(value, str):

                checkFilePathExists(file_path=value, argument=key)

                requestBody[columnAlias[key]] = readFileContent(value)

        return requestBody

    except Exception as e:
        logger.error(
            f"Failed to create or update Hive metastore configuration due to: {e}")
        sys.exit(-1)
