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
missing_message = f"Entity with value('{entity_id}') does not exist"

entity = {
    'ItemCode': entity_id,
    'ItemName': 'This is a test item'
}


def test_update_entity(
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

    item = {
        'ItemCode': entity_id,
        'ItemName': 'It has been changed'
    }

    change = svc.update_entity(entity_type,
                               item,
                               entity_key)

    svc.delete_entity(entity_type,
                      entity_id)

    print(f'Updated: {change}')

    svc.logout()

    if change['code'] != 204:
        assert False

    assert True


def test_update_missing(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)
    svc.login()
    
    entity_type = svc.entity('items')

    svc.delete_entity(entity_type, entity_id)

    item = {
        'ItemCode': entity_id,
        'ItemName': 'It has been changed'
    }

    change = svc.update_entity(entity_type, item, entity_key)

    print(f'Updated: {change}')

    svc.logout()

    if change['code'] != 404:
        assert False

    if change['error'] != -2028:
        assert False

    if change['error_message'] != missing_message:
        assert False

    assert True
