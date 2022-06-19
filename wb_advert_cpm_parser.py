import argparse
import db_facade
import wb_requests
import json
import time
import logging
import sys
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='WB advert parser', add_help=False)
    parser.add_argument('-u', '--db-user', dest='db_user', help='db user name')
    parser.add_argument('-p', '--db-password',
                        dest='db_password', help='db password')
    parser.add_argument('-d', '--db-name', dest='db_name',
                        help='database name')
    parser.add_argument('-P', '--db-port', dest='db_port',
                        help='database port')
    parser.add_argument('-h', '--db-host', dest='db_host',
                        help='database host')
    return parser.parse_args()


def main():
    args = parse_arguments()
    db = db_facade.connect(args)
    while True:
        interval = int(db_facade.get_settings(db)[db_facade.kSettingNameIntervalSec])
        work_loop(db)
        time.sleep(interval)


def work_loop(db):
    queries = db_facade.get_queries(db)
    for q in queries:
        json_data = '{}'
        status = 'OK'
        try:
            json_data = wb_requests.search_catalog_ads(q['query_text'])
            json_str = json.dumps(json_data)
        except Exception as e:
            logger.warning("error processing search_catalog_ads: {0}".format(e))
            status = e
        db_facade.save_ads_search_result(db, q['id'], json_str, status)
        time.sleep(0.2)
        

if __name__ == "__main__":
    main()
