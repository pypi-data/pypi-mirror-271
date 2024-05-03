#! /usr/bin/python3
from sbo_service.service import Service

import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = os.getenv('test_comp')
test_serv = os.getenv('test_serv')

today = date.today().strftime('%Y%m%d')

document = {
    'DocType': 'dDocumentItems',
    'DocDate': today,
    'DocDueDate': today,
    'CardCode': 'C999999999',
    'NumAtCard': 'test order...should be canceled',
    'Comments': 'Original test comment',
    'DocumentLines': [
        {
            'ItemCode': '7896300',
            'TaxCode': 'EX',
            'Quantity': 10
        }
    ]
}


def test_invoices(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    document_type = svc.entity('invoices')

    # test creation
    create = svc.create_document(document_type, document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    create.pop('data')

    if create['error']:
        assert False

    if create['code'] != 201:
        assert False

    update_document = {
        'DocEntry': doc_entry,
        'Comments': 'This is an updated document'
    }

    update = svc.update_document(
        document_type,
        update_document,
        'DocEntry')

    if not update['success']:
        assert False, update['error_message']

    # test close
    close = svc.close_document(document_type, doc_entry)

    # cannot close an invoice
    if close['error'] != -5006:
        assert False

    if close['code'] != 400:
        assert False

    # create another one
    create = svc.create_document(document_type, document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    create.pop('data')

    if create['error']:
        assert False

    if create['code'] != 201:
        assert False

    cancel = svc.cancel_document(document_type, doc_entry)

    if cancel['code'] != 204:
        assert False

    if cancel['error']:
        assert False

    assert True


def test_orders(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    document_type = svc.entity('sales orders')

    # test creation
    create = svc.create_document(document_type, document)
    
    print(create)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    create.pop('data')

    if create['error']:
        assert False

    if create['code'] != 201:
        assert False

    # test close
    close = svc.close_document(document_type, doc_entry)

    # can close an order
    if close['error']:
        assert False

    if close['code'] != 204:
        assert False

    # create another one
    create = svc.create_document(document_type, document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    create.pop('data')

    if create['error']:
        assert False

    if create['code'] != 201:
        assert False

    cancel = svc.cancel_document(document_type, doc_entry)

    if cancel['code'] != 204:
        assert False

    if cancel['error']:
        assert False

    assert True
