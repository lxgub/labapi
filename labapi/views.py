from .serializers import PatientsSerializer
from .models import Transactions, Patients
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .services import append_request, change_request, logger
from rest_framework.response import Response
from rest_framework import status


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    """
    ViewSet allows you to Create, Receive,
    Update, Delete transactions for each patient.
    """
    serializer_class = PatientsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Patients.objects.all()

    def get_queryset(self):
        """
        Returns an object with transactions
        of all registered patients
        """
        return self.queryset.all()

    def create(self, request):
        """
        Creates a new transaction for specific patient.
        If patient is not exist, rises Exseption (Incorrect data).
        """
        if len(request.data.get('transactions', None)) != 1:
            content = {'error': 'Incorrect data. Please change only one transaction per one request.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        patient_code = request.data.get('code', None)
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_transaction = serializer.validated_data['transactions'][0]

        try:
            transfer = append_request(valid_transaction, patient_code, user_id)
            logger('POST', user_id, patient_code, transfer, after=valid_transaction)
        except Exception as e:
            content = {'Error field': '{}'.format(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Updates transaction for specific patient.
        If patient or transaction_id is not exist, rises Exseption (Incorrect data).
        """
        if len(request.data.get('transactions', None)) != 1:
            content = {'error': 'Incorrect data. You can change only one transaction per one request.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        patient_code = request.data.get('code', None)
        request_id = request.data.get('transactions', None)[0].get('id', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_transaction = serializer.validated_data['transactions'][0]

        try:
            data = change_request(valid_transaction, request_id)
            logger('PUT', user_id, patient_code, request_id, data, valid_transaction)
        except Exception as e:
            content = {'error': '{}'.format(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        """
        Destroys a transaction.
        """
        try:
            instance = Transactions.objects.get(id=kwargs.get('pk'))
            transaction = {"status": instance.status, "urgently": instance.urgently,
                           "payment_type": instance.payment_type}
            logger('DELETE', instance.user_id, instance.patient_id, instance.id, before=transaction)
        except Exception as e:
            content = {'Error': '{}'.format(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
