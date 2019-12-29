from labapi.models import Transactions, Logger
import json


def append_request(data, patient_code, user_id):
    """
    Creates new transaction.
    """
    if not all((data.get('status', False),
                data.get('urgently', False),
                data.get('payment_type', False))):
        raise (ValueError('Not all required fields were completed.'))

    transfer = Transactions.objects.create(
        patient_id=patient_code,
        user_id=user_id,
        status=data['status'],
        urgently=data['urgently'],
        payment_type=data['payment_type']
    )
    return transfer.id


def change_request(data, transaction_id):
    """
    Updates data in an existing transaction.
    """
    if not any((data.get('status', False),
                data.get('urgently', False),
                data.get('payment_type', False))):
        raise (ValueError('No one of the required fields were completed.'))

    req = Transactions.objects.get(id=transaction_id)
    log_data = {
                'status': req.status,
                'urgently': req.urgently,
                'payment_type': req.payment_type
                }

    if data.get('status', None):
        req.status = data['status']
    if data.get('urgently', None):
        req.urgently = data['urgently']
    if data.get('payment_type', None):
        req.payment_type = data['payment_type']
    req.save()

    return log_data


def logger(request_type, user_id, patient_code, transaction_id=None, before=None, after=None):
    """
    Logs data before and after changes.
    """
    if before:
        before = json.dumps(before)
    if after:
        after = json.dumps(after)
    log = Logger(request_type=request_type, user_id=user_id,
                 transaction_id=transaction_id, patient_code=patient_code,
                 before=before, after=after)
    log.save()
