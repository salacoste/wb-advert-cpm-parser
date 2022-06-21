import psycopg2
import psycopg2.extras

kSettingNameIntervalSec = 'scan_interval_sec'


def connect(params):
    db = psycopg2.connect(database=params.db_name, user=params.db_user,
                          password=params.db_password, host=params.db_host, port=params.db_port)
    db.autocommit = True
    return db


def __parse_settings(settings):
    s_dict = {}
    for s in settings:
        s_dict[s[0]] = s[1]
    required_settings_list = [kSettingNameIntervalSec]
    for name in required_settings_list:
        if s_dict[name] is None:
            raise RuntimeError("Setting '{0}' not found".format(name))
    return s_dict


def get_queries(db):
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT q.id, q.query_text, g.group_name "
        "FROM ads_search_query q "
        "JOIN ads_search_group g ON q.group_id = g.id "
        "WHERE g.turn_on = TRUE;")
    return cursor.fetchall()


def save_ads_search_result(db, query_id, json_str, status):
    cursor = db.cursor()
    insert_query = f"INSERT INTO ads_search_scan_result (query_id, json_result, result_status)" \
        f"VALUES ({query_id},'{json_str}','{status}');"
    cursor.execute(insert_query)
    print('saved. query_id: {0}, status: {1}'.format(query_id, status))


def get_settings(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT setting_name, setting_value FROM ads_search_settings;")
    settings = cursor.fetchall()
    return __parse_settings(settings)
