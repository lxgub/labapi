from rest_framework import serializers
from labapi.models import Transactions, Patients


class TransactionsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Transactions
        fields = ('id', 'status', 'urgently', 'payment_type')
        read_only_fields = ('id', )


class PatientsSerializer(serializers.ModelSerializer):
    transactions = TransactionsSerializer(read_only=False, many=True)

    def validate(self, data):
        """
        The serializer contains validation of patient data.
        If the patient is not found in the patient table,
        validation is unsuccessful.
        """
        try:
            if self.initial_data:
                Patients.objects.get(code=self.initial_data['code'], fname=data['fname'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "Not found patient with the specified data. Please be sure to enter the correct "
                "patient data or add a new patient.")
        return data

    class Meta:
        model = Patients
        fields = ('code', 'fname', 'mname', 'lname', 'birthday', 'card_number', 'phone', 'transactions')
        read_only_fields = ('phone', 'card_number', )
