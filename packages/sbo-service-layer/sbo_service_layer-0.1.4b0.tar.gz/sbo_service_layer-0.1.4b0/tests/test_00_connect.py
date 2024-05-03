#! /usr/bin/python3
from sbo_service.service import Service

import os
from dotenv import load_dotenv

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = os.getenv('test_comp')
test_serv = os.getenv('test_serv')


def test_initialize(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)

    if svc.api_server != server:
        assert False

    if svc.api_company != company:
        assert False

    if svc.api_username != user:
        assert False

    if svc.api_password != password:
        assert False

    if svc.api_url != f'https://{server}:50000/b1s/v1/':
        assert False

    svc = Service(user, password, company, server, 12345)

    if svc.api_url != f'https://{server}:12345/b1s/v1/':
        assert False

    assert True


def test_login(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)

    result = svc.login()

    if result.status_code != 200:
        assert False

    svc.logout()

    assert True


def test_logout(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)

    result = svc.login()

    if result.status_code != 200:
        assert False

    result = svc.logout()

    if result.status_code != 204:
        assert False

    assert True


def test_fullcycle(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    svc = Service(user, password, company, server)

    result = svc.login()

    if result.status_code != 200:
        assert False

    result = svc.logout()

    if result.status_code != 204:
        assert False

    assert True
