from rest_framework import serializers

from cart import models


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineItem
        fields = '__all__'
