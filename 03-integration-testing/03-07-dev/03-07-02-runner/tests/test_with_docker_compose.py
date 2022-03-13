# pylint: disable=redefined-outer-name
"""Zaadaptowany przykład z dokumentacji pytest-docker-compose."""
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

pytest_plugins = ["docker_compose"]


# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
    """Poczekaj aż aplikacja zacznie odpowiadać"""
    request_session = requests.Session()
    retries = Retry(total=15, backoff_factor=1, status_forcelist=[500])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get("app").network_info[0]
    api_url = f"http://{service.hostname}:{service.host_port}/"
    assert request_session.get(api_url + "health")
    return request_session, api_url


@pytest.mark.uses_docker
def test_fraud_check_validates(wait_for_api):
    """Uderzamy do API sprawdzając czy odrzuci nam żądanie z pustym JSONem."""
    request_session, api_url = wait_for_api

    response = request_session.post(api_url + "fraudCheck", json={})

    assert response.status_code == 400
    response_json = response.json()
    assert "person" in response_json
    assert "uuid" in response_json
