#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import logging
import hashlib
import pymysql
import time
import os, sys
import shortuuid
import urllib
import urlparse
import pyodbc
import pprint
import binascii
from logging.handlers import RotatingFileHandler

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

rotateFile = RotatingFileHandler('main.log',maxBytes=10*1024*1024,backupCount=5)
rotateFile.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotateFile.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(rotateFile)

DATA_BLOB = '0D1B400A0D1B401D2F031B33001B2A213F000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001FF0001FF0001FF0001FF0001FF00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F0001FF0001FF0001FF0001FF0001FF00000000000000000000000000000000013F00013F00013F00013F00013F00000F00000F00000F00000F00000F0001FF0001FF0001FF0001FF0001FF00000000000000000000000000000000000F00000F00000F00000F00000F00000F00000F00000F00000F00000F00000000000000000000000000000000000F00000F00000F00000F00000F00000F00000F00000F00000F00000F00000000000000000000000000000000000F00000F00000F00000F00000F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00000F00000F00000F00000F00000F00013F00013F00013F00013F00013F00000000000000000000000000000000013F00013F00013F00013F00013F00000000000000000000000000000000000000000000000000000000000000000F00000F00000F00000F00000F00000F00000F00000F00000F00000F0000000000000000000000000000000001FF0001FF0001FF0001FF0001FF00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F00013F0001FF0001FF0001FF0001FF0001FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000070000070000070000070000077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF07000007000007000007000007000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000001FFF001FFF001FFF001FFF001FFF801F00801F00801F00801F00801F008000FF8000FF8000FF8000FF8000FF03E0F803E0F803E0F803E0F803E0F8801F07801F07801F07801F07801F07FFE0F8FFE0F8FFE0F8FFE0F8FFE0F8033F033F033F033F033F3FF883FFF883FFF883FFF883FF3F3FFF3FFF3FFF3FFF3F7C00F87C00F87C00F87C00F87C00F883FFFF3FFF3FFF3FFF3FFF7C00007C00007C00007C00007C0000001FFF001FFF001FFF001FFF001FFF3FF8FC1FF8FC1FF8FC1FF8FC1F3F3F7F3F7F3F7F3F7F3F0000000000000000000000000000007F3F7F3F7F3F7F3F7F3F033F00033F00033F00033F00033F007F3F7F3F7F3F7F3F7F3FFFE0F8FFE0F8FFE0F8FFE0F8FFE0F83FFF3FFF3FFF3FFF3FFF000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000070000070000070000070000077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF07000007000007000007000007000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003F007C3F007C3F007C3F007C3F007CC1F003C1F003C1F003C1F003C1F003C1F07CC1F07CC1F07CC1F07CC1F07C3FFF3FFF3FFF3FFF3FFFC1F000C1F000C1F000C1F000C1F0003F803F803F803F803F80C1F07CC1F07CC1F07CC1F07CC1F07C013F00013F00013F00013F00013F003F00003F00003F00003F00003F0000013F013F013F013F013F3F00033F00033F00033F00033F0003000000000000000000000000000000C1F07FC1F07FC1F07FC1F07FC1F07F3E0F3F0F3F0F3F0F3F0FFCC000003F00003F00003F00003F00003FFFFF3FFFFF3FFFFF3FFFFF3FFFFF3F83C1FF83C1FF83C1FF83C1FF3FF07C01F07C01F07C01F07C01F07CFF3F00FF3F00FF3F00FF3F00FF3F003FFF3FFF3FFF3FFF3FFFFCFE007F3F007F3F007F3F007F3F007F3F3F3F3F3F3F3F3F3F3FFFF07CFFF07CFFF07CFFF07CFFF07C01FF8001FF8001FF8001FF8001FF80FF3FFF3FFF3FFF3FFF3F00007C00007C00007C00007C00007C3FFF3FFF3FFF3FFF3FFF000F80000F80000F80000F80000F803F83FE0F83FE0F83FE0F83FE0F3F000F80000F80000F80000F80000F803FFF3FFF3FFF3FFF3FFFC1F07CC1F07CC1F07CC1F07CC1F07CC1F000C1F000C1F000C1F000C1F0003F007C3F007C3F007C3F007C3F007C3FFF3FFF3FFF3FFF3FFF3F007C3F007C3F007C3F007C3F007C3FFCC1FFFCC1FFFCC1FFFCC1FF3F0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003F003F003F003F003F3FC0E0FFC0E0FFC0E0FFC0E0FF3F000001000001000001000001000001FF3F00FF3F00FF3F00FF3F00FF3F0000FF3F00FF3F00FF3F00FF3F00FF3FFF3FFF3FFF3FFF3FFF3F073F073F073F073F073F003E1F003E1F003E1F003E1F003E00073F00073F00073F00073F00073F3F00FF3F00FF3F00FF3F00FF3F00E0F800E0F800E0F800E0F800E0F80000FF3F00FF3F00FF3F00FF3F00FFC1E0FFFEE0FFFEE0FFFEE0FFFEE0FF3F00011F00011F00011F00011F00011FFF3FFF3FFF3FFF3FFF3FFF3FFF3FFF3FFF3FFFC1E0FFC0E0FFC0E0FFC0E0FFC0E0FF3F003F1F003F1F003F1F003F1F003F00FF3F00FF3F00FF3F00FF3F00FF3F00003E00003E00003E00003E00003EFF3F00FF3F00FF3F00FF3F00FF3F003F00013F00013F00013F00013F00011F073F073F073F073F073F003F003F003F003F003FFF07FFFF07FFFF07FFFF07FFFF07FF1FFF3FFF3FFF3FFF3FFF3F073F073F073F073F073F0007FF0007FF0007FF0007FF0007FFFF0001FF0001FF0001FF0001FF000100FFFF00FFFF00FFFF00FFFF00FFFFFF0001FF0001FF0001FF0001FF00011F00001F00001F00001F00001F00001F00011F00011F00011F00011F00011FFF3FFF3FFF3FFF3FFFC0E03FE0F801E0F801E0F801E0F80100FF3F00FF3F00FF3F00FF3F00FF3F0007FF0007FF0007FF0007FF0007FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003FE0F003E0F003E0F003E0F0033F00033F00033F00033F00033F00033F801FFF801FFF801FFF801FFF801F0FFFFF0FFFFF0FFFFF0FFFFF0FFFFF0F3F000F3F000F3F000F3F000F3F003FE0F003E0F003E0F003E0F003E0F07C1FF07C1FF07C1FF07C1FF07C1F0F3F000F3F000F3F000F3F000F3F000F801F0F801F0F801F0F801F0F801F0F3F0F3F0F3F0F3F0F3F00001F00001F00001F00001F00001FF07C00F07C00F07C00F07C00F07C00000000000000000000000000000000F07C1FF07C1FF07C1FF07C1FF07C1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF83E0FF83E0FF83E0FF83E0FF83E0007C00007C00007C00007C00007C00FFFF3FFF3FFF3FFF3FFFE0F003FF3FFF3FFF3FFF3FFF0FFFFF0FFFFF0FFFFF0FFFFF0FFFFF0F3F0F3F0F3F0F3F0F3F3FE0F003E0F003E0F003E0F003E0F07C00F07C00F07C00F07C00F07C003FFF3FFF3FFF3FFF3FFFF07C00F07C00F07C00F07C00F07C00FF3FFF3FFF3FFF3FFF3F0F3F0F3F0F3F0F3F0F3FF07C00F07C00F07C00F07C00F07C00FFFF3FFF3FFF3FFF3FFFE0F0001F3F001F3F001F3F001F3F001F3FFF3FFF3FFF3FFF3FFF0F3F0F3F0F3F0F3F0F3FF07C1FF07C1FF07C1FF07C1FF07C1F0F3F0F3F0F3F0F3F0F3F3F001F3F001F3F001F3F001F3F001F007FFF007FFF007FFF007FFF007FFF3FE0F07FE0F07FE0F07FE0F07F3F0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003F0F3F0F3F0F3F0F3F0F003E00003E00003E00003E00003E0000013F00013F00013F00013F00013F00000000000000000000000000000007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F007C1F0073F073F073F073F073F3F003F003F003F003F003F0F3F0F3F0F3F0F3F0FFFC1F0FFC1F0FFC1F0FFC1F0FFC1F0003F3F003F3F003F3F003F3F003F3F003FFF003FFF003FFF003FFF003FFF003FFF003FFF003FFF003FFF003FFFFF3FFF3FFF3FFF3FFF3F07C1F007C1F007C1F007C1F007C1F0FFC1F0FFC1F0FFC1F0FFC1F0FFC1F03FFF3FFF3FFF3FFF3FFF3FF0F801F0F801F0F801F0F8013FFFFF07FFFF07FFFF07FFFF07FFFF0000000000000000000000000000003F003F003F003F003F0007FF3FFF3FFF3FFF3FFF3F003E0F003E0F003E0F003E0F003E0F073F00073F00073F00073F00073F00FF3F00FF3F00FF3F00FF3F00FF3F0007C1F007C1F007C1F007C1F007C1F0073F073F073F073F073F07FF3FFF3FFF3FFF3FFF3FC1F007C1F007C1F007C1F007C1F000000F00000F00000F00000F00000F3F0F3F0F3F0F3F0F3F0F00000F00000F00000F00000F00000F0001FF0001FF0001FF0001FF0001FF3FF0F801F0F801F0F801F0F8013F003F3F003F3F003F3F003F3F003F3F3FFF3FFF3FFF3FFF3F0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFF07FFFF07FFFF07FFFF07FFFF070000070000070000070000070000070000070000070000070000070000070000070000070000070000070000077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077FFF077C1F077C1F077C1F077C1F077C1F073F00003F00003F00003F00003F00007C1FFF7C1FFF7C1FFF7C1FFF7C1FFF83E0F883E0F883E0F883E0F883E0F87C1FFF7C1FFF7C1FFF7C1FFF7C1FFF7F3F7F3F7F3F7F3F7F3F83E0F883E0F883E0F883E0F883E0F880000080000080000080000080000083E0F883E0F883E0F883E0F883E03F0000FF0000FF0000FF0000FF0000FF03E0F803E0F803E0F803E0F803E0F8801FFF801FFF801FFF801FFF801FFF7C1F007C1F007C1F007C1F007C1F0083E00783E00783E00783E00783E0077F3F007F3F007F3F007F3F007F3F00033F033F033F033F033F7FE0F87FE0F87FE0F87FE0F87FE0F883E0F883E0F883E0F883E0F883E03F3F007F3F007F3F007F3F007F3F00001F00001F00001F00001F00001F007FFF007FFF007FFF007FFF007FFF00FFFF07FFFF07FFFF07FFFF07FFFF077C1FFF7C1FFF7C1FFF7C1FFF7C1FFF001F00001F00001F00001F00001F00801F07801F07801F07801F07801F073F003F003F003F003F00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF83E00783E00783E00783E00783E0070000000000000000000000000000007C1FFF7C1FFF7C1FFF7C1FFF7C1FFF3F073F073F073F073F070000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3F00003F00003F00003F00003F00003FFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC1FFFCC000003F00003F00003F00003F0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF01FF3FFF3FFF3FFF3FFF3F3FFF3FFF3FFF3FFF3F3F00033F00033F00033F00033F0003000003000003000003000003000003013F013F013F013F013F3E00003E00003E00003E00003E00003F00033F00033F00033F00033F00033F3F3F3F3F3F3F3F3F3F3F007F3F007F3F007F3F007F3F007F01FF3FFF3FFF3FFF3FFF3F3FFF3FFF3FFF3FFF3F3E0F3F0F3F0F3F0F3F0F3FFFFFFFFFFFFFFFFFFFFFFFFFFFFF3E0F3F0F3F0F3F0F3F0F3F3F00013F00013F00013F00013F003E0F3F0F3F0F3F0F3F0F3FFF8001FF8001FF8001FF8001FF80000F3F000F3F000F3F000F3F000F83C13FC1F07FC1F07FC1F07FC1F07FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF013F013F013F013F013F3F803F803F803F803F8001FF3FFF3FFF3FFF3FFF3F3FFF3FFF3FFF3FFF3F3F007C3F007C3F007C3F007C3F007C01FF3FFF3FFF3FFF3FFFFCC13F00C1F000C1F000C1F000C1F0003F007F3F007F3F007F3F007F3F007F0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A1B2A213F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FF0000FF0000FF0000FF0000FF00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F0000FF0000FF0000FF0000FF0000FF00000000000000000000000000000000003F00003F00003F00003F00003F00001F00001F00001F00001F00001F00003F00003F00003F00003F00003F00003F00003F00003F00003F00003F0000FF0000FF0000FF0000FF0000FF00003F00003F00003F00003F00003F0000000000000000000000000000000000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF00003F00003F00003F00003F00003F00003F00003F00003F00003F00003F0000FF0000FF0000FF0000FF0000FF00003F00003F00003F00003F00003F0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000000000000000000000000000000000FF0000FF0000FF0000FF0000FF00001F00001F00001F00001F00001F0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF0000FF00003F00003F00003F00003F00003F0000FF0000FF0000FF0000FF0000FF00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00003F00003F00003F00003F00003F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F00001F0000FF0000FF0000FF0000FF0000FF00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000A0D0A0D0A0D0A0D0A'

#-------------------- sql server operation ----------------------
dsn      = 'sqlserverdatasource'
user     = 'sa'
password = 'windjack123'
database = 'wifi2com'
connStr  = 'DRIVER={SQL Server};SERVER=139.196.57.30;PORT=1443;UID=%s;PWD=%s;DATABASE=%s;' % (user, password, database)
logger.info("start setup odbc connection, connStr = {}".format(connStr))
odbcConn = pyodbc.connect(connStr)
odbcCursor = odbcConn.cursor()
logger.info("odbc connection setup successfully!")

def getNewRowsFromUpLog():
    rows = odbcCursor.execute("select * from MessageUpLog where IsNew = 1").fetchall()
    logger.info("running getNewRowsFromUpLog: rows = {}".format(len(rows)))
    return rows
def updateIsNewFromUpLog(row):
    odbcCursor.execute("update MessageUpLog set IsNew = 0 where Id = ?", row[0])
    odbcCursor.commit()
    logger.info("running updateIsNewFromUpLog: update MessageUpLog set IsNew = 0 where Id = {}".format(row[0]))

def doWriteDownLog(upLogRow, frontText, behindText):
    deviceId = upLogRow[1]
    length   = upLogRow[3]
    data     = upLogRow[4]
    port     = choose(upLogRow[2] == 4000, 4001, 4000)
    odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, ?)", deviceId, port, length, data)
    odbcCursor.commit()
    
    frontText = frontText.encode('gb2312').encode('hex').upper()
    length = len(frontText) / 2 
    odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, convert(VARBINARY(max), ?, 2))", deviceId, port, length, frontText)
    odbcCursor.commit()
    
    behindText = behindText.encode('gb2312').encode('hex').upper()
    length = len(behindText) / 2 
    odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, convert(VARBINARY(max), ?, 2))", deviceId, port, length, behindText)
    odbcCursor.commit()
    logger.info("finish doWriteDownLog!")

def doWriteDownLogForApiError(upLogRow, errorText):
    deviceId = upLogRow[1]
    length   = upLogRow[3]
    data     = upLogRow[4]
    port     = choose(upLogRow[2] == 4000, 4001, 4000)
    errorText = errorText.encode('gb2312').encode('hex').upper()
    length = len(errorText) / 2 
    odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, convert(VARBINARY(max), ?, 2))", deviceId, port, length, errorText)
    odbcCursor.commit()
    logger.info("finish doWriteDownLogForApiError!")
#-------------------- mysql operation ----------------------
logger.info("start setup mysql connection.")
mysqlConn = pymysql.connect(host='localhost',
                             user='root',
                             password='hJexOiChC40H',
                             db='qrcode',
                             cursorclass=pymysql.cursors.DictCursor)
logger.info("mysql connection setup successfully!")                          

lastSuccessRow = None
def handleMysqlStatus(upLogRow):
    dataId   = upLogRow[0]
    deviceId = upLogRow[1]
    port     = choose(upLogRow[2] == 4000, 4001, 4000)

    cursor   = mysqlConn.cursor()
    sqlStr   = "select * from qrcode_table where status = 2 and data_id = {}".format(dataId)
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    logger.info("running handleMysqlStatus: {}, rows number is {}".format(sqlStr, len(rows)))
    global lastSuccessRow
    if len(rows) > 0:
        row = rows[-1]
        blobData = row['data_blob']
        length = len(blobData)
        blobData = pyodbc.Binary(blobData)
        logger.info("blobData length: mysql = {}, mssql = {}".format(length, len(blobData)))
        #odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, convert(VARBINARY(max), ?, 2))", deviceId, port, length, blobData)
        odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, ?)", deviceId, port, length, blobData)
        odbcCursor.commit()
        mysqlConn.cursor().execute("update qrcode_table set status = 3 where data_id = {}".format(dataId))
        logger.info("running handleMysqlStatus: {}".format("update qrcode_table set status = 3 where data_id = {}".format(dataId)))
        mysqlConn.commit()
        lastSuccessRow = row
    else:
        if not lastSuccessRow:
            cursor.execute("SELECT * FROM qrcode_table WHERE status=3 ORDER BY data_id DESC LIMIT 0,1")
            logger.info("running: SELECT * FROM qrcode_table WHERE status=3 ORDER BY data_id DESC LIMIT 0,1")
            lastSuccessRow = cursor.fetchall()[0]
            
        blobData = lastSuccessRow['data_blob']
        length   = len(blobData)
        blobData = pyodbc.Binary(blobData)
        logger.info("blobData length: mysql = {}, mssql = {}".format(length, len(blobData)))
        #odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, convert(VARBINARY(max), ?, 2))", deviceId, port, length, blobData)
        odbcCursor.execute("insert into MessageDownLog(DeviceId, Port, Length, Data) values(?, ?, ?, ?)", deviceId, port, length, blobData)
        odbcCursor.commit()
        doWriteDownLogForApiError(upLogRow, "QR Error")
        mysqlConn.cursor().execute("update qrcode_table set status = 4 where data_id = {}".format(dataId))
        logger.info("running handleMysqlStatus: {}".format("update qrcode_table set status = 4 where data_id = {}".format(dataId)))
        mysqlConn.commit()
    logger.info("finish handleMysqlStatus!")

#-------------------- request and store picture operation ----------------------
qrCodeDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "picture"))
if not os.path.exists(qrCodeDir):
    os.mkdir(qrCodeDir)
logger.info(os.path.abspath(qrCodeDir))

SIGNKEY = 'i5OqMrNXVyOJ5GEMYoEtRHqN1P9ghk6I'
URL     = 'http://qiye.wxsdc.ediankai.com/api/v1/suppliers/1/staff/1/box/get'

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('http://', adapter)

def saveToDisk(url, data_id, equ_id):
    ticket = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query)).get('ticket')
    filename = '{}_{}.jpeg'.format(data_id, equ_id)
    urllib.urlretrieve(url, os.path.join(qrCodeDir, filename))
    return open(os.path.join(qrCodeDir, filename), 'rb').read()

def doGetRequest(row):
    SIGNKEY = 'i5OqMrNXVyOJ5GEMYoEtRHqN1P9ghk6I'
    #data_id = shortuuid.ShortUUID(alphabet="0123456789").random(length=10)
    #equ_id  = shortuuid.ShortUUID(alphabet="0123456789").random(length=10)
    data_id, equ_id = row[0], row[1]

    parameterStr = "{SIGNKEY}data_id{data_id}equ_id{equ_id}{SIGNKEY}".format(**locals())
    logger.info("parameter str: {}".format(parameterStr))
    sign = hashlib.md5(parameterStr).hexdigest()
    data = {'equ_id': equ_id, 'data_id': data_id, 'sign': sign}
    logger.info("payload: {}".format(data))
    
    try:
        r = session.post(URL, data=data)
        if r.status_code == requests.codes.ok:
            url = r.json()['data']['url']
            [logger.info(element) for element in (url, r.json()['data']['front_text'], r.json()['data']['behind_text'])]
            imageData = saveToDisk(url, data_id, equ_id)
            mysqlConn.cursor().execute("INSERT INTO qrcode_table (data_id, equ_id, link, image) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE link=%s, image=%s", (data_id, equ_id, url, imageData, url, imageData))
            mysqlConn.commit()
            return (url, r.json()['data']['front_text'], r.json()['data']['behind_text'])
        else:
            logger.error("request failed! status_code={}".format(r.status_code))
            return None
    except requests.ConnectionError as exception:
        logger.error(exception, exc_info=True)
        return None
    except Exception as exception:
        logger.error(exception, exc_info=True)
        doWriteDownLogForApiError(row, "API Error")
        updateIsNewFromUpLog(row)
        logger.info("response text: {}".format(r.text))
        return None
    
def choose(res, left, right):
    logger.info("running choose: {}, {}, {}".format(res, left, right))
    if res:
        return left
    else:
        return right
    
def job():
    logger.info("start job!!!")
    for row in getNewRowsFromUpLog()[:1]:  #每个周期只处理一个
        port = row[2]
        if port == 4000:
            logger.info("skip port = 4000!")
            updateIsNewFromUpLog(row)
            return
        result = doGetRequest(row)
        if result:
            updateIsNewFromUpLog(row)
            #doWriteDownLog(row, result[1], result[2])
            time.sleep(3)
            handleMysqlStatus(row)
    logger.info("finish job!!!")

#import schedule
#schedule.every(2).seconds.do(job)

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

class QRCodeServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "QRCodeService"
    _svc_display_name_ = "QR Code Service"
    _svc_description_ = "This service is used for QR Code handling."  

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def main(self):
        while True:
           schedule.run_pending()
           #job()
           time.sleep(1)

if __name__ == '__main__':
    while True:
       #schedule.run_pending()
       job()
       time.sleep(1)
    #win32serviceutil.HandleCommandLine(QRCodeServerSvc)
    