from rest_framework import serializers
from .. import models

class AuthPermissionsListSerializer(serializers.ModelSerializer):
    '''
    PERMISSION SERIALIZER
    '''

    class Meta:
        model = models.AuthPermissions
        fields = ('id','perm_name','perm_description','permission_uuid')