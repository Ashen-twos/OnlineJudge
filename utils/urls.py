from django.conf.urls import url

from .views import SimditorImageUploadAPIView, SimditorFileUploadAPIView, CreateJudgeCodeAPIView

urlpatterns = [
    url(r"^upload_image/?$", SimditorImageUploadAPIView.as_view(), name="upload_image"),
    url(r"^upload_file/?$", SimditorFileUploadAPIView.as_view(), name="upload_file"),
    url(r"^create_judge_code/?$", CreateJudgeCodeAPIView.as_view(), name="create_judge_code")
]
