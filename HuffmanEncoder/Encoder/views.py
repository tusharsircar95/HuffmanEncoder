from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import EncodingSerializer,ExtractedMessageSerializer
from .models import Encoding,ExtractedMessage
from .HuffmanEncoder import HuffmanEncoder,HuffmanTree
from .CompressionMap import CompressionMap
# Create your views here.


class EncoderAPI(APIView):

    def get(self,request):
        message = request.GET.get('message',None)
        if message is None or message == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        encoding = HuffmanEncoder.compressMessage(message=message)
        serializer = EncodingSerializer(encoding)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        return Response(status=HTTP_204_NO_CONTENT)


class DecoderAPI(APIView):

    def get(self,request):
        compressedMessage = request.GET.get('compressedMessage',None)
        key_1 = request.GET.get('key_1',None)
        key_2 = request.GET.get('key_2',None)

        encoding = Encoding(compressedMessage=compressedMessage,key_1=key_1,key_2=key_2)
        if not encoding.isValid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        extractedMessage = HuffmanEncoder.extractMessage(encoding)
        serializer = ExtractedMessageSerializer(extractedMessage)
        return Response(serializer.data,status=status.HTTP_200_OK)



def SampleView(request):
    return HttpResponse('34')