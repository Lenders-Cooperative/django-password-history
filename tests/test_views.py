import pytest
from django.test import TestCase
from django.test import RequestFactory

from django_password_history.views import (
    UserPasswordHistoryCreateView,
    UserPasswordHistoryDeleteView,
    UserPasswordHistoryDetailView,
    UserPasswordHistoryListView,
    UserPasswordHistoryUpdateView,
)
from django_password_history.models import UserPasswordHistory
from tests.factory import UserFactory

pytestmark = pytest.mark.django_db


class UserPasswordHistoryViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory(username="history_user")

    @pytestmark
    def test_user_password_history_create_view_uses_model(self):
        view = UserPasswordHistoryCreateView()

        assert view.model is UserPasswordHistory
        assert view.get_queryset().model is UserPasswordHistory


    @pytestmark
    def test_user_password_history_detail_view_get_object(self):
        history = UserPasswordHistory.objects.create(user=self.user)

        request = RequestFactory().get("/")
        view = UserPasswordHistoryDetailView()
        view.setup(request, pk=history.pk)

        assert view.get_object() == history


    @pytestmark
    def test_user_password_history_update_view_get_object(self):
        history = UserPasswordHistory.objects.create(user=self.user)

        request = RequestFactory().get("/")
        view = UserPasswordHistoryUpdateView()
        view.setup(request, pk=history.pk)

        assert view.get_object() == history


    @pytestmark
    def test_user_password_history_delete_view_get_object(self):
        history = UserPasswordHistory.objects.create(user=self.user)

        request = RequestFactory().get("/")
        view = UserPasswordHistoryDeleteView()
        view.setup(request, pk=history.pk)

        assert view.get_object() == history


    @pytestmark
    def test_user_password_history_list_view_queryset(self):
        view = UserPasswordHistoryListView()

        assert view.model is UserPasswordHistory
        assert view.get_queryset().model is UserPasswordHistory
