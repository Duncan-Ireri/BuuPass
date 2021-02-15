from rest_framework import serializers
from tickets.models import Tickets

class CreateTicketSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tickets
        fields = ('ticket_route', 'ticket_number', 'user')


class UpdateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('ticket_approved', )
