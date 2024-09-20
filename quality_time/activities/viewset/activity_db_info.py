'''
Created on 2024/09/09

@author: kuyamakazuhiro
'''


from rest_framework import generics
from django.db.models import Count, Max, Min
from rest_framework.response import Response
from activities.models import Activity
from activities.serializers.activity_db_info_serializer import ActivityDbInfoSerializer

class ActivityDbInfoView(generics.RetrieveAPIView):
    queryset = Activity.objects.aggregate(Min('start_time'), Max('start_time'), Count('id'))
    serializer_class = ActivityDbInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        # 呼び出し1: get_object()
        qs = self.get_queryset()
        # dictをオブジェクトに変換する
        instance = ActivityDbInfo(qs['start_time__min'], qs['start_time__max'], qs['id__count'])
        #instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# 一時的なオブジェクト
class ActivityDbInfo:
    def __init__(self, start_time, end_time, count):
        self.startTime = start_time
        self.endTime = end_time
        self.count = count
        