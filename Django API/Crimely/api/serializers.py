from rest_framework import serializers
from api.models import Users, Property

class Userserializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Users
        fields="__all__"

class Propertyserializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

