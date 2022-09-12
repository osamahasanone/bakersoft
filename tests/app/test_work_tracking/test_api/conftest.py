import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from core.models import User
from work_tracking.models import Employee


@pytest.fixture
def employee():
    user = baker.make(User)
    return baker.make(Employee, user=user)


@pytest.fixture
def api_client(employee):
    client = APIClient()
    client.force_authenticate(user=employee.user)
    return client
