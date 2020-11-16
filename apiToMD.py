#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import datetime
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QTreeWidgetItem
from PyQt5.QtGui import QFont
from mainwindow_ui import Ui_HttpToMD
from mdInfo_ui import Ui_Form
import httpUtils
from dbTools import DBToolCls


# 主窗口
class MainWindowCls(QWidget, Ui_HttpToMD):

    def __init__(self):
        super().__init__()
        # 加载主窗口 UI
        self.setupUi(self)

        # 实例化子窗口
        self.md_window = MDInfoCls()

        # 实例化数据库工具
        self.db_tools = DBToolCls()

        # 实例树节点
        self.treeWidget_1.setHeaderHidden(True)
        self.initRootNode()

        # 设置用户操作事件
        self.setUserEvent()

    # 设置用户操作事件
    def setUserEvent(self):
        self.comboBox_1.setCurrentIndex(1)
        self.pushButton_1.clicked.connect(self.clickButten_1)
        self.pushButton_2.clicked.connect(self.clickButten_2)
        self.pushButton_3.clicked.connect(self.clickButten_3)
        self.pushButton_4.clicked.connect(self.clickButten_4)
        self.pushButton_5.clicked.connect(self.clickButten_5)
        self.pushButton_6.clicked.connect(self.clickButten_6)
        self.pushButton_7.clicked.connect(self.clickButten_7)
        self.pushButton_8.clicked.connect(self.clickButten_8)
        self.pushButton_9.clicked.connect(self.clickButten_9)
        self.lineEdit_1.setText('http://192.168.2.7:8080/mate/groupByInfo')
        self.plainTextEdit_1.setPlainText('{"header":"header_data"}')
        self.plainTextEdit_2.setPlainText('{"body":"body_data"}')

        self.treeWidget_1.doubleClicked.connect(self.treeRecoverData)


    # 按日期分组添加根节点
    def initRootNode(self):
        self.treeWidget_1.clear()
        root_node_name_sql = "SELECT in_date FROM request_log GROUP BY in_date ORDER BY in_date DESC"
        query_root_name_res = self.db_tools.querySearch(sql_str=root_node_name_sql)
        if query_root_name_res:
            for this_root_dict in query_root_name_res:
                this_date = this_root_dict.get('in_date', '2020-01-01') or '2020-01-01'

                self.this_root_node = QTreeWidgetItem(self.treeWidget_1)
                self.this_root_node.setText(0, this_date)
                child_name_sql = f"SELECT id, request_type, request_url FROM request_log WHERE in_date='{this_date}' ORDER BY id DESC"
                query_child_name_res = self.db_tools.querySearch(sql_str=child_name_sql)
                if query_child_name_res:
                    for this_child_dict in query_child_name_res:
                        request_id = this_child_dict.get('id')
                        request_type = this_child_dict.get('request_type')
                        request_url = this_child_dict.get('request_url')
                        this_child_name = str(request_id) + ' ' + request_type + ' ' + request_url

                        self.this_child_node = QTreeWidgetItem(self.this_root_node)
                        self.this_child_node.setText(0, this_child_name)
                        self.this_child_node.setToolTip(0, this_child_name)


    # 格式化 json
    def formatJson(self, json_data):
        try:
            this_dict = json.loads(json_data)
            format_data = json.dumps(this_dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            return format_data
        except BaseException as e:
            print('格式化 Json 错误：', e)
            return 0

    # 格式化 4 按钮事件
    def clickButten_4(self):
        header_data = self.plainTextEdit_1.toPlainText()
        res = self.formatJson(header_data)
        if res:
            self.plainTextEdit_1.setPlainText(res)

    # 格式化 5 按钮事件
    def clickButten_5(self):
        body_data = self.plainTextEdit_2.toPlainText()
        res = self.formatJson(body_data)
        if res:
            self.plainTextEdit_2.setPlainText(res)

    # 格式化 6 按钮事件
    def clickButten_6(self):
        res_data = self.plainTextEdit_3.toPlainText()
        res = self.formatJson(res_data)
        if res:
            self.plainTextEdit_3.setPlainText(res)

    # 清空 3 按钮事件
    def clickButten_3(self):
        clear_tree_data_sql = "DELETE FROM request_log"
        truncate_request_log_sql = "UPDATE sqlite_sequence SET seq = 0 WHERE name='request_log'"
        self.db_tools.doSQL(sql_str=clear_tree_data_sql)
        self.db_tools.doSQL(sql_str=truncate_request_log_sql)
        self.treeWidget_1.clear()

    # 清空 7 按钮事件
    def clickButten_7(self):
        self.plainTextEdit_1.clear()

    # 清空 8 按钮事件
    def clickButten_8(self):
        self.plainTextEdit_2.clear()

    # 清空 9 按钮事件
    def clickButten_9(self):
        self.plainTextEdit_3.clear()

    # 发送 1 按钮事件
    def clickButten_1(self):
        request_type = self.comboBox_1.currentText()
        request_url = self.lineEdit_1.text()
        headers_data = self.plainTextEdit_1.toPlainText()
        body_data = self.plainTextEdit_2.toPlainText()
        if request_type == 'GET':
            response = httpUtils.sendGetRequest(url=request_url, headers=headers_data, params=body_data)
            # print(res)
            self.plainTextEdit_3.setPlainText(response)
        elif request_type == 'POST':
            response = httpUtils.sendPostRequest(url=request_url, headers=headers_data, data=body_data)
            # print(res)
            self.plainTextEdit_3.setPlainText(response)
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        insert_data_sql = f"INSERT INTO request_log (in_date, request_type, request_url, request_header, request_data, response_data) " \
                          f"VALUES ('{this_date}', '{request_type}', '{request_url}', '{headers_data}', '{body_data}', '{response}')"
        self.db_tools.doSQL(sql_str=insert_data_sql)
        self.initRootNode()

    # 生成文档 2 按钮事件
    def clickButten_2(self):
        self.md_window.show()
        request_type = self.comboBox_1.currentText()
        url = self.lineEdit_1.text()
        headers = self.plainTextEdit_1.toPlainText()
        body = self.plainTextEdit_2.toPlainText()
        response = self.plainTextEdit_3.toPlainText()
        headers = headers if headers != '' else json.dumps({"headers": "None"})
        body = body if body != '' else json.dumps({"data": "None"})
        response = response if response != '' else json.dumps({"response": "None"})

        md_data = httpUtils.makeMD(request_type=request_type, url=url, headers=headers, data=body, response=response)
        # print(headers)
        self.md_window.showData(md_data)

    # 查看历史数据
    def treeRecoverData(self, node_info):
        this_parent_row = node_info.parent().row()
        this_parent_data = node_info.parent().data()
        this_node_row = node_info.row()
        this_node_data = node_info.data()
        this_request_id = this_node_data.split(' ')[0]

        if this_parent_data:
            this_request_info_sql = f"SELECT * FROM request_log WHERE id='{this_request_id}'"
            this_request_info_res = self.db_tools.querySearch(sql_str=this_request_info_sql)
            if this_request_info_res:
                this_request_type = this_request_info_res[0]['request_type']
                this_request_url = this_request_info_res[0]['request_url']
                this_request_header = this_request_info_res[0]['request_header']
                this_request_data = this_request_info_res[0]['request_data']
                this_response_data = this_request_info_res[0]['response_data']
                if this_request_type == 'GET':
                    self.comboBox_1.setCurrentIndex(0)
                elif this_request_type == 'POST':
                    self.comboBox_1.setCurrentIndex(1)
                self.lineEdit_1.setText(this_request_url)
                self.plainTextEdit_1.setPlainText(this_request_header)
                self.plainTextEdit_2.setPlainText(this_request_data)
                self.plainTextEdit_3.setPlainText(this_response_data)




# 子窗口
class MDInfoCls(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # 加载子窗口 UI
        self.setupUi(self)

        # 加载方法
        self.showData(data='')

    def showData(self, data):
        self.plainTextEdit.setPlainText(data)



if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # 实例化主窗口
    main_window_obj = MainWindowCls()
    main_window_obj.show()

    sys.exit(app.exec_())