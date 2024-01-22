from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ModelSerializer
from . import models


class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
        depth = 1


class CreateMessageView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = models.Message
