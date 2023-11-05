# from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from store.models import Collection
from model_bakery import baker


# api_client.force_authenticate(user=User(is_staff=True))
# arrange
# act

# @pytest.mark.skip
@pytest.fixture
def create_collection(api_client):
    def do_create_collection(data):
        return api_client.post('/store/collection/', data)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_return_401(self, create_collection):
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, create_collection, authenticate):
        authenticate(is_staff=False)
        response = create_collection({'title': 'a'})
        print(response.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection({})
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        api_client.force_authenticate(User(is_staff=True))
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collection/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        # assert response.data == {
        #     'id': collection.id,
        #     'title': collection.title,
        #     'product_count': 0,
        # }
