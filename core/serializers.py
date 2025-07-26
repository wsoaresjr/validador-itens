from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import Group

class ItemUploadSerializer(serializers.Serializer):
    grupo = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    arquivos = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    def create(self, validated_data):
        grupo = validated_data['grupo']
        arquivos = validated_data['arquivos']

        itens = []
        for arq in arquivos:
            item = Item.objects.create(
                titulo=arq.name,
                pdf=arq,
                grupo=grupo
            )
            itens.append(item)
        return itens
