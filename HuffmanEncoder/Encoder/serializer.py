from rest_framework import serializers
from .models import Encoding,ExtractedMessage


class EncodingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encoding
        fields = ('compressedMessage','key_1','key_2','compressionEfficiency')


class ExtractedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedMessage
        fields = "__all__"