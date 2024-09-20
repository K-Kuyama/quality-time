'''
Created on 2024/06/20

@author: kuyamakazuhiro
'''

#import datetime
from rest_framework import viewsets, generics
from rest_framework.response import Response
from activities.models import  Perspective, Category, CategorizedActivity, CategorizedKeyWord
from activities.serializers.user_definition_serializers import PerspectiveSerializer, CategorySerializer, CategorizedActivitySerializer, CategorizedKeyWordSerializer, _PerspectiveSerializer
# from activities.modules.definition_model import DefinitionModel

class PerspectiveViewSet(viewsets.ModelViewSet):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    
class BulkCreatePerspectiveView(generics.CreateAPIView):
    serializer_class = PerspectiveSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(BulkCreatePerspectiveView, self).get_serializer(*args, **kwargs)


# <pk>で指定されたパースペクティブに紐付く情報を取り出して返す
# 取り出した情報は、シングルトンクラスである、DefinitionModelに登録され、別のアプリケーションから参照できるようにしている
class _PerspectiveView(generics.RetrieveAPIView):
    queryset = Perspective.objects.prefetch_related('categories').all()
    serializer_class = _PerspectiveSerializer   

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
#        print(serializer.data)
#        DefinitionModel().setPerspective(serializer.data)
#        print(DefinitionModel().categories)
        return Response(serializer.data)
    
#   
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related()
    serializer_class = CategorySerializer
    
class BulkCreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(BulkCreateCategoryView, self).get_serializer(*args, **kwargs)


    
class CategorizedActivityViewSet(viewsets.ModelViewSet):
    queryset = CategorizedActivity.objects.all()
    serializer_class = CategorizedActivitySerializer
    
class BulkCreateCategorizedActivityView(generics.CreateAPIView):
    serializer_class = CategorizedActivitySerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(BulkCreateCategorizedActivityView, self).get_serializer(*args, **kwargs)
    
    def post(self, request):
        result = self.create(request)
        print(f"post result => {result}")
#        DefinitionModel().reSetPerspective()
        return result
    
    
# 登録アクティビティ情報から指定されたidを削除する。複数の削除が可能
class DeleteCategorizedActivityView(generics.ListAPIView):    
    model = CategorizedActivity
    
    def post(self, request):
        id_list = request.data
        CategorizedActivity.objects.filter(pk__in=id_list).delete()
#        DefinitionModel().reSetPerspective()
        return Response(id_list)
        
    
    
class CategorizedKeyWordViewSet(viewsets.ModelViewSet):
    queryset = CategorizedKeyWord.objects.all()
    serializer_class = CategorizedKeyWordSerializer
    
class BulkCreateCategorizedKeyWordView(generics.CreateAPIView):
    serializer_class = CategorizedKeyWordSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(BulkCreateCategorizedKeyWordView, self).get_serializer(*args, **kwargs)
    

class DeleteCategorizedKeyWordView(generics.ListAPIView):    
    model = CategorizedActivity
    
    def post(self, request):
        id_list = request.data
        print(f"delete word id list {id_list}")
        CategorizedKeyWord.objects.filter(pk__in=id_list).delete()
#        DefinitionModel().reSetPerspective()
        return Response(id_list)
    
    
