'''
Created on 2024/04/26

@author: kuyamakazuhiro
'''
from django.urls import path
from rest_framework import routers
from .views import ActivityViewSet, BulkCreateActivityView, TimePeriodView, PaginatedEventView, TotalEventTimeByHour
from activities.viewset.merged_event import MergedEventView
from activities.viewset.categorized_event import CategorizedEventView
from activities.viewset.periodical_graph import TotalEventTimeForPeriodicalGraph
from activities.viewset.keyword_candidate import KeywordCandidateView
from activities.viewset.perspective_editor import PerspectiveEditorView
from activities.viewset.user_definition import PerspectiveViewSet, CategoryViewSet, CategorizedActivityViewSet,\
                                                 CategorizedKeyWordViewSet,_PerspectiveView,BulkCreateCategorizedActivityView,\
                                                 BulkCreateCategorizedKeyWordView, DeleteCategorizedActivityView, DeleteCategorizedKeyWordView
from activities.viewset.sort_out_by_categories import SortOutByCategoriesView
from activities.viewset.sort_out_by_multi_categories import SortOutByMutiCategoriesView
from activities.viewset.periodical_categories import PeriodicalCategoriesView
from activities.viewset.activity_db_info import ActivityDbInfoView
from activities.viewset.file_upload import FileUploadView

router = routers.DefaultRouter()
router.register(r'Activity', ActivityViewSet)
router.register(r'user_def/Perspective', PerspectiveViewSet)
router.register(r'user_def/Category', CategoryViewSet)
router.register(r'user_def/CategorizedActivity', CategorizedActivityViewSet)
router.register(r'user_def/CategorizedKeyword', CategorizedKeyWordViewSet)
#router.register(r'Activity/ActivityDbInfo', ActivityDbInfoViewSet)


urlpatterns = [
    path('Activity/bulk/', BulkCreateActivityView.as_view(), name="bulk_create"),
    path('Activity/time_period/', TimePeriodView.as_view(), name="time_period_view"),
    path('Activity/merged_event/', MergedEventView.as_view(), name="merged_event_view"),
    path('Activity/paginated_event/', PaginatedEventView.as_view(), name="paginated_event_view"),
    path('Activity/total_event_time_by_hour/', TotalEventTimeByHour.as_view(), name="total_event_time_by_hour_view"),
    path('Activity/total_event_time_for_periodical/', TotalEventTimeForPeriodicalGraph.as_view(), name="total_event_time_for_periodical"),
    path('user_def/_Perspective/<pk>/', _PerspectiveView.as_view(), name="_perspective_view"),
    path('Activity/categorized_event/', CategorizedEventView.as_view(), name="categorized_event_view"),
    path('Activity/sort_out_by_categories/', SortOutByCategoriesView.as_view(),name="sort_out_by_categories"),
    path('Activity/sort_out_by_multi_categories/', SortOutByMutiCategoriesView.as_view(),name="sort_out_by_multi_categories"), 
    path('Activity/periodical_categories/', PeriodicalCategoriesView().as_view(),name="periodical_categories"),   
    path('user_def/bulk_c_activity/', BulkCreateCategorizedActivityView.as_view(), name="bulk_create_c_activity"),
    path('user_def/bulk_c_keywords/', BulkCreateCategorizedKeyWordView.as_view(), name="bulk_create_c_keyword"),    
    path('user_def/delete_c_activity/', DeleteCategorizedActivityView.as_view(), name="delete_c_activity"),
    path('user_def/delete_c_keywords/', DeleteCategorizedKeyWordView.as_view(), name="delete_c_keywords"),   
    path('user_def/candidate_words/', KeywordCandidateView.as_view(), name="keyword_candidate"),
    path('user_def/perspective_editor/', PerspectiveEditorView.as_view(), name="perspective_editor"),
    path('Activity/activity_db_info/<pk>/', ActivityDbInfoView.as_view(), name="activity_db_info"),
    path('Activity/file_upload/', FileUploadView.as_view(), name="file_upload")
]

urlpatterns += router.urls
