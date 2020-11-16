import sqlite3

class DBToolCls():
    def __init__(self):
        self.initTable()

    def initTable(self):
        conn = sqlite3.connect('makeMD_log.db')
        conn.row_factory = self.dictFactory
        cursor = conn.cursor()
        create_table_sql = '''CREATE TABLE IF NOT EXISTS request_log 
        ("id" integer primary key autoincrement,
        "in_date" VARCHAR (16) DEFAULT '2020-01-01',
        "request_type" VARCHAR (8),
        "request_url" text,
        "request_header" text,
        "request_data" text,
        "response_data" text)'''
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
        conn.close()


    def dictFactory(self, cursor, row):
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def doSQL(self, sql_str):
        conn = sqlite3.connect('makeMD_log.db')
        conn.row_factory = self.dictFactory
        cursor = conn.cursor()
        try:
            cursor.execute(sql_str)
            # 通过rowcount获得插入的行数:
            # print(cursor.rowcount)
            conn.commit()
            cursor.close()
            conn.close()
            return 1
        except Exception as e:
            print(e)
            conn.commit()
            cursor.close()
            conn.close()
            return 0


    def querySearch(self, sql_str):
        conn = sqlite3.connect('makeMD_log.db')
        conn.row_factory = self.dictFactory
        cursor = conn.cursor()
        cursor.execute(sql_str)

        # 通过rowcount获得插入的行数:
        # print(cursor.rowcount)

        # 获得查询结果集:
        values = cursor.fetchall()

        cursor.close()
        conn.close()
        return values

if __name__ == '__main__':
    db_tools = DBToolCls()
    # sql_str = "insert into request_log (in_date, request_type, request_url, request_header, request_data, response_data) " \
    #           "values ('2020-11-06', 'GET', 'http://test', 'header_json', 'data_json', 'res_data')"
    # res = db_tools.doSQL(sql_str=sql_str)

    sql_str = "select in_date, request_type, request_url from request_log group by in_date"
    res = db_tools.querySearch(sql_str=sql_str)
    print(res)
