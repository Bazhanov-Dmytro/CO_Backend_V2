from .models import User, Organization, Message, Indicators, Report
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'lastname', 'age', 'organization', 'role']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.organization = validated_data['organization']
        user.name = validated_data['name']
        user.lastname = validated_data['lastname']
        user.age = validated_data['age']
        user.role = validated_data['role']
        return user


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'workers_count', 'ceo']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.EmailField()
    recipient = serializers.EmailField()

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'header', 'text', 'creation_date']


class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = [
            'user_email',
            'higher_pressure',
            'lower_pressure',
            'heartbeat_rate',
            'temperature',
            'is_critical',
            'timeouts_taken',
        ]


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.EmailField()
    report_details = serializers.CharField(max_length=1000, required=False)
    danger_level = serializers.IntegerField(required=False)
    recommendation = serializers.CharField(max_length=1000, required=False)

    class Meta:
        model = Report
        fields = ['user', 'creation_date', 'report_details', 'danger_level', 'recommendation']
