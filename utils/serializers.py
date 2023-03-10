from rest_framework import serializers

from options.options import SysOptions


class InvalidLanguage(serializers.ValidationError):
    def __init__(self, name):
        super().__init__(detail=f"{name} is not a valid language")


class LanguageNameChoiceField(serializers.CharField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data and data not in SysOptions.language_names:
            raise InvalidLanguage(data)
        return data


class SPJLanguageNameChoiceField(serializers.CharField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data and data not in SysOptions.spj_language_names:
            raise InvalidLanguage(data)
        return data


class LanguageNameMultiChoiceField(serializers.ListField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        for item in data:
            if item not in SysOptions.language_names:
                raise InvalidLanguage(item)
        return data


class SPJLanguageNameMultiChoiceField(serializers.ListField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        for item in data:
            if item not in SysOptions.spj_language_names:
                raise InvalidLanguage(item)
        return data

class JudgeConditionSerializer(serializers.Serializer):
    parameter = serializers.CharField()
    data_type = serializers.CharField()
    relation = serializers.CharField()
    value = serializers.CharField()
    value_type = serializers.CharField()

class CreateJudgeCodeSerializer(serializers.Serializer):
    condition = serializers.ListField(child=JudgeConditionSerializer(), allow_empty=False)

class FuncParameterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    ptr = serializers.BooleanField()
    arr = serializers.BooleanField()

class FunctinoPreviewSerializer(serializers.Serializer):
    name = serializers.CharField()
    return_type = serializers.CharField()
    parameter = serializers.ListField(child=FuncParameterSerializer(), allow_empty=True)
