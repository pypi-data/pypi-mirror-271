#! /usr/bin/python3
from sbo_service.service import Service

import os
from dotenv import load_dotenv

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = os.getenv('test_comp')
test_serv = os.getenv('test_serv')

entity_id = 'z_testitem'
entity_key = 'ItemCode'

duplicate_message = f"Item code '{entity_id}' already exists"

entity = {
    'ItemCode': entity_id,
    'ItemName': 'This is a test item'
}


def test_create_entity(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    entity_type = svc.entity('items')

    svc.delete_entity(entity_type,
                      entity_id)

    create = svc.create_entity(entity_type,
                               entity)

    svc.logout()

    if create['error']:
        assert False

    assert True


def test_duplicate_entity(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    entity_type = svc.entity('items')

    svc.delete_entity(entity_type, entity_id)

    # create twice to force duplication
    svc.create_entity(entity_type,
                      entity)
    create = svc.create_entity(entity_type,
                               entity)

    print(f'Create Response: {create}')

    if create['code'] != 400:
        assert False

    if create['error'] != -10:
        assert False

    if create['error_message'] != duplicate_message:
        assert False

    svc.logout()

    assert True


def test_delete_entity(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    entity_type = svc.entity('items')

    svc.create_entity(entity_type,
                      entity)

    delete = svc.delete_entity(entity_type,
                               entity_id)

    print(f'Delete response: {delete}')

    if delete['code'] != 204:
        assert False

    svc.logout()

    assert True


def test_cleanup(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    entity_type = svc.entity('items')

    svc.delete_entity(entity_type, entity_id)

    svc.logout()

    assert True
