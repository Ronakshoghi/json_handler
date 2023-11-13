from django.urls import path
from . import views

app_name = "json"
urlpatterns = [
    path('merge', views.MergeResult.as_view(), name="merge"),
    path('download/<str:name>', views.DownloadFileView.as_view(), name="download"),
]
