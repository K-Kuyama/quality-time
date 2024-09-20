'''
Created on 2024/09/07

@author: kuyamakazuhiro
'''
import abc
import os

import csv
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
import requests



class EventProducer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createEvent(self, ar, last_window, end_time):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def createBlankEvent(self, bp):
        raise NotImplementedError()


'''
アクティビティ情報（イベント）をHTTP　POSTでサーバに出力する
''' 
    
class HttpEventProducer(EventProducer):
    def __init__(self, post_url, post_bulk_url, time_zone):
        self.post_url = post_url
        self.post_bulk_url = post_bulk_url
        #self.url = "http://127.0.0.1:8000/api/Activity/"
        self.request_pool =[]
        self.time_zone = time_zone

    def createEvent(self, ar, last_window, end_time):
        event_data = ar.get_data()
        start_time = ar.start_time
        if end_time :
            duration = end_time - start_time
        else :
            duration = datetime.now(ZoneInfo(self.time_zone)) - start_time
        event_data['window'] = last_window
        request_body = {
            'start_time':start_time.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            'duration':duration.seconds,
            'distance_x':event_data['distance_x'],
            'distance_y':event_data['distance_y'],
            'strokes':event_data['strokes'],
            'scrolls':event_data['scrolls'],
            'app':event_data['window']['app'],
            'title':event_data['window']['title'],
            }
        print(f"request:{request_body}")
        self.sendEvent(request_body)



    def sendEvent(self, request_body):
        if (len(self.request_pool)>0):
            self.request_pool.append(request_body)
            try:
                response = requests.post(self.post_bulk_url, json=self.request_pool)
#                print(f"{response} : {self.request_pool}")
                self.request_pool =[]
            except requests.exceptions.ConnectionError:
                print("ConnectinError")
        else:
            try:
                response = requests.post(self.post_url,json=request_body)
                print(response)
            except requests.exceptions.ConnectionError:
#                print("ConnectinError")
                self.request_pool.append(request_body)

 
    def createBlankEvent(self, bp):
        start_time = bp.start_time
#        duration = datetime.now(timezone.utc) - start_time
        duration = datetime.now(ZoneInfo("Asia/Tokyo")) - start_time
#        print(f"BP end at {datetime.now(timezone.utc)}")
#        print("createBlankEvent")
#        self.writer.writerow([start_time, duration.seconds,0,0,0,0,0,'blank', 'blank'])
#        self.f.flush()
        request_body = {
            'start_time':start_time.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            'duration':duration.seconds,
            'distance_x':0,
            'distance_y':0,
            'strokes':0,
            'scrolls':0,
            'app':'blank',
            'title':'blank',
            }
        response = self.sendEvent(request_body)
#        response = requests.post(POST_URL, json=request_body)
        print(response)



'''
アクティビティ情報（イベント）をローカルファイルに出力する
''' 


class FileEventProducer(EventProducer):
    def __init__(self, path, encoding, period, time_zone):
        
        self.encoding = encoding
        self.period = period
        self.path =path
        self.time_zone = time_zone
        self.filename = ""
        self.end_time = None
        self.file = None
        self.writer = None



        # 現在時間を取得
        now_time = datetime.now(ZoneInfo(self.time_zone))
 
        # ファイル名を生成する。       
        base_time = self.getBaseTime(now_time)
        self.filename = self.path+"qt-"+base_time.strftime("%Y-%m-%d")+".csv"      
         
        # ファイルをオープンする。すでにファイルが存在する場合は、ファイル末尾から追記していく。
        print(f"file name ={self.filename}")
        if not os.path.exists(self.filename):
            self.file = open(self.filename, 'w', encoding=self.encoding, errors='none')
            print(f"create file {self.filename}")
        else:
            self.file = open(self.filename, 'a', encoding=self.encoding, errors='none')
            print(f"open file {self.filename}")
        self.writer = csv.writer(self.file)
            
        # ファイルローテートする時間をend_timeに設定する
        if self.period :
            self.end_time = self.getEndTime(now_time)
            print(f"set end_time {self.end_time}")
        
        
    def getEndTime(self, now_time): 
        # ファイルローテートする時間を計算
        end_time =None  
        if self.period == "day":
            end_time = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))+timedelta(days=1)
        elif self.period =="week":
            index = date(now_time.year, now_time.month, now_time.day).isoweekday()%7
            end_time = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))+timedelta(days=(7-index))
        elif self.period =="month":
            end_time = datetime(now_time.year, now_time.month, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))+relativedelta(months=1)
        return end_time

        
    def getBaseTime(self, now_time):
        # ファイル名に付ける基準時間を計算
        base_time =None  
        if self.period == "day":
            base_time = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
        elif self.period =="week":
            index = date(now_time.year, now_time.month, now_time.day).isoweekday()%7
            base_time = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))-timedelta(days=index)
        elif self.period =="month":
            base_time = datetime(now_time.year, now_time.month, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
        return base_time

    # 書き込まれたアクティビティの時間によって、ファイルをローテート
    def checkDate(self, start_time):
        if(start_time >= self.end_time):
            self.writer = None
            self.file.close()
            # ファイルをオープンする。すでにファイルが存在する場合は、ファイルを書き換え。
            self.filename = self.path+"qt-"+start_time.strftime("%Y-%m-%d")+".csv"
            self.file = open(self.filename, 'w', encoding=self.encoding, errors='none')
            self.writer = csv.writer(self.file)
            # ファイルローテートする時間をend_timeに設定する
            self.end_time = self.getEndTime(start_time)
 
           
    def createEvent(self, ar, last_window, end_time):
        event_data = ar.get_data()
        start_time = ar.start_time
        if end_time :
            duration = end_time - start_time
        else :
            duration = datetime.now(ZoneInfo(self.time_zone)) - start_time
        event_data['window'] = last_window
        self.writer.writerow([
            start_time.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            duration.seconds,
            event_data['distance_x'],
            event_data['distance_y'],
            event_data['strokes'],
            event_data['scrolls'],
            event_data['window']['app'],
            event_data['window']['title']
            ])
        self.file.flush()
        # ファイルローテートのチェック
        if self.period:
            self.checkDate(start_time)
        
    def createBlankEvent(self, bp):
        start_time = bp.start_time
        duration = datetime.now(ZoneInfo(self.time_zone)) - start_time
#        print(f"BP end at {datetime.now(timezone.utc)}")
#        print("createBlankEvent")
        self.writer.writerow([
            start_time.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            duration.seconds,
            0, 0, 0, 0, 'blank', 'blank'
            ])
        self.file.flush()

