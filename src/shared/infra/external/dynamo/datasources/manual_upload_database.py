from src.envs import Envs
import asyncio
import pprint

from src.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.external.dynamo.datasources.mock_db import CLASSES # arquivo temporario com lista das aulas

access_key = Envs.getConfig().access_key
secret_key = Envs.getConfig().secret_key
endpoint_url = None
dynamo_table_name = Envs.getConfig().dynamo_table_name
region = Envs.getConfig().region


def getDuplicates(data, partition_key, sort_key):
    keys = []
    duplicates = []
    duplicates_keys = []
    for item in data:
        if (item[partition_key], item[sort_key]) in keys:
            duplicates.append(item)
            duplicates_keys.append((item[partition_key], item[sort_key]))
        else:
            keys.append((item[partition_key], item[sort_key]))

    return duplicates, duplicates_keys


if __name__ == '__main__':
    dynamo = DynamoDatasource(access_key, secret_key, endpoint_url, dynamo_table_name, region)
    data = CLASSES

    asyncio.run(dynamo.batch_write_items(data))
    # duplicates, keys = getDuplicates(data, "subjectCode", "studentRA")
    # pprint.pprint(duplicates)
    # print("\n\n", keys)

    # print(len(keys))

    # asyncio.run(dynamo.put_item(data))