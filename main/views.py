from rest_framework import viewsets
from rest_framework.response import Response
from .IndicatorAnalysis import Analyser
from itertools import chain
from .models import User, Organization, Indicators, Message, Report
from .serializers import (
    UserSerializer,
    OrganizationSerializer,
    IndicatorsSerializer,
    MessageSerializer,
    ReportSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import SelfInstanceAccessPermission, IsManager


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [SelfInstanceAccessPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(organization=request.user.organization)

        if request.user.role == None:
            return Response("Not approved account")

        if request.user.role == 2:
            queryset = chain(queryset.filter(id=request.user.id), queryset.filter(role=1))

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user_instance = User.objects.get(email=request.query_params['email'])
        serializer = UserSerializer(user_instance)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        try:
            if request.data["change_role"] and request.user.role == 3:
                user_instance = User.objects.get(email=request.data["email"])
                user_instance.role = request.data['role']
                user_instance.save()
                print("ok")

                return Response("Status: Updated")
        except:
            user_instance = User.objects.get(email=request.data['old_email'])

            if user_instance.check_password(request.data['old_password']):
                user_instance.email = request.data['new_email']
                user_instance.set_password(request.data['new_password'])
                user_instance.save()
                return Response("Status: Updated")

        return Response("Status: Update Failed")


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class IndicatorsViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['GET']
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Indicators.objects.all()
    serializer_class = IndicatorsSerializer


class MessageViewSet(viewsets.ModelViewSet):
    allowed_methods = ['POST', 'GET', 'PUT']
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = User.objects.get(email=request.user.email)

        queryset_sender = queryset.filter(sender=user.id)
        queryset_recipient = queryset.filter(recipient=user.id)

        result_list = sorted(
            chain(queryset_sender, queryset_recipient),
            key=lambda instance: instance.creation_date
        )

        serializer = MessageSerializer(result_list, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        recipient = User.objects.get(email=self.request.data['recipient'])
        header = self.request.data['header']
        text = self.request.data['text']

        message = Message()
        message.sender = user
        message.recipient = recipient
        message.header = header
        message.text = text
        message.save()
        return message


class ReportViewSet(viewsets.ModelViewSet):
    allowed_methods = ['POST', 'GET']
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.GET['email'])
        except:
            user = User.objects.get(email=request.user.email)
        user_organization = request.user.organization
        queryset = self.get_queryset()
        queryset = queryset.filter(organization=user_organization)
        queryset = queryset.filter(user=user.id)
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        indicators = Indicators.objects.get(user_email_id=self.request.user)
        user = User.objects.get(email=self.request.data['user'])
        report = Report()

        report.user = user
        report.organization = self.request.user.organization

        analyser = Analyser(
            indicators.heartbeat_rate,
            (indicators.higher_pressure, indicators.lower_pressure),
            indicators.temperature
        )

        result = analyser.execute_full_analysis()
        report.report_details = result[0]
        report.recommendation = result[1]
        report.danger_level = result[2]
        report.save()


class ReportForWorkersViewSet(viewsets.ModelViewSet):
    allowed_methods = ['GET']
    permission_classes = [IsAuthenticated, SelfInstanceAccessPermission]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)[:15]
        result_list = sorted(
            chain(queryset),
            key=lambda instance: instance.creation_date,
            reverse=True)
        serializer = ReportSerializer(result_list, many=True)
        return Response(serializer.data)
