from rest_framework import serializers
from .. import models

class RoleListSerializer(serializers.ModelSerializer):
    '''
    ROLE LIST SERIALIZER
    '''
    class Meta:
        model = models.Role
        fields = '__all__'

class RoleModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

