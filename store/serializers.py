from rest_framework import serializers

from store import models


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'


class StoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreImage
        fields = '__all__'
