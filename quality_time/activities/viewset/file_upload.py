'''
Created on 2024/09/10

@author: kuyamakazuhiro
'''
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime
from django.db import IntegrityError, transaction
import re
import os
import csv

from activities.models import FileUpdateHistory
from activities.models import Activity
from activities.serializers.file_update_history_serializer import FileUpdateHistorySerializer


DATETIME_FORMAT ="%Y-%m-%d %H:%M:%S.%f%z"

class FileUploadView(generics.ListCreateAPIView):
    queryset = FileUpdateHistory.objects.all()
    serializer_class = FileUpdateHistorySerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # データベースにデータを書き込む
        self.perform_create(serializer)

        # データインポート
        # contentsに格納されているURLを、ファイルパスに変換する
        f_name = self.urlToFile(serializer.data['contents'])
        # ファイルからcsvデータを読み出す
        file = open(f_name, "r")
        activities = csv.reader(file)
        # csvの内容をデータベースに反映する
        skips = 0
        for ac in activities:
            activity = self.createActivity(ac)
            try:
                activity.save()
            except IntegrityError:
                print(f" Data import error :{activity}")
                skips += 1
        print(f"Data import success : skip {skips}")
        fh = FileUpdateHistory.objects.get(id=serializer.instance.id)
        fh.status = "imported (skip "+str(skips)+" rows)"
        fh.save()
        
        '''
        try:
            with transaction.atomic():
                for ac in activities:
                    activity = self.createActivity(ac)
                    activity.save()
        except IntegrityError:
            print(f" Data import error :{f_name}")
        else:
            print(f"Data import success :{f_name}")
            # データ書き込みが正常に終わった場合、ステータスを"imported"にアップデート
            fh = FileUpdateHistory.objects.get(id=serializer.instance.id)
            fh.status = "imported"
            fh.save()
        '''    
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        


    def urlToFile(self, url_str):
        MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)
        MEDIA_URL = getattr(settings, "MEDIA_URL", None)
        ro = re.search(MEDIA_URL, url_str)
        t_str = url_str[ro.span()[1]:]
        file_str = os.path.join(MEDIA_ROOT, t_str)
        print(file_str)
        return file_str

   
    def createActivity(self, ac_list):
        a = Activity()
        a.start_time = datetime.strptime(ac_list[0], DATETIME_FORMAT)
        a.duration = int(ac_list[1])
        a.distance_x = float(ac_list[2])
        a.distance_y = float(ac_list[3])
        a.strokes = int(ac_list[4])
        a.scrolls = int(ac_list[5])
        a.app = ac_list[6]
        a.title = ac_list[7]
        return a
    