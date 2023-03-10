import os
from django.conf import settings
from account.serializers import ImageUploadForm, FileUploadForm
from utils.shortcuts import rand_str
from utils.api import CSRFExemptAPIView, validate_serializer
from utils.test import CreateJudgeCode, CreateFunctionTemplate
from utils.serializers import CreateJudgeCodeSerializer, FunctinoPreviewSerializer
import logging

logger = logging.getLogger(__name__)


class SimditorImageUploadAPIView(CSRFExemptAPIView):
    request_parsers = ()

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data["image"]
        else:
            return self.response({
                "success": False,
                "msg": "Upload failed",
                "file_path": ""})

        suffix = os.path.splitext(img.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.response({
                "success": False,
                "msg": "Unsupported file format",
                "file_path": ""})
        img_name = rand_str(10) + suffix
        try:
            with open(os.path.join(settings.UPLOAD_DIR, img_name), "wb") as imgFile:
                for chunk in img:
                    imgFile.write(chunk)
        except IOError as e:
            logger.error(e)
            return self.response({
                "success": False,
                "msg": "Upload Error",
                "file_path": ""})
        return self.response({
            "success": True,
            "msg": "Success",
            "file_path": f"{settings.UPLOAD_PREFIX}/{img_name}"})


class SimditorFileUploadAPIView(CSRFExemptAPIView):
    request_parsers = ()

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
        else:
            return self.response({
                "success": False,
                "msg": "Upload failed"
            })

        suffix = os.path.splitext(file.name)[-1].lower()
        file_name = rand_str(10) + suffix
        try:
            with open(os.path.join(settings.UPLOAD_DIR, file_name), "wb") as f:
                for chunk in file:
                    f.write(chunk)
        except IOError as e:
            logger.error(e)
            return self.response({
                "success": False,
                "msg": "Upload Error"})
        return self.response({
            "success": True,
            "msg": "Success",
            "file_path": f"{settings.UPLOAD_PREFIX}/{file_name}",
            "file_name": file.name})
        
class CreateJudgeCodeAPIView(CSRFExemptAPIView):
    @validate_serializer(CreateJudgeCodeSerializer)
    def post(self, request):
        return self.response({
            "error": None,
            "data": CreateJudgeCode(request.data["condition"])
        })
class FunctinoPreviewAPIView(CSRFExemptAPIView):
    @validate_serializer(FunctinoPreviewSerializer)
    def post(self, request):
        return self.response({
            "error": None,
            "data": CreateFunctionTemplate(name=request.data["name"], return_type=request.data["return_type"], parameter_list=request.data["parameter"])
        })        
        