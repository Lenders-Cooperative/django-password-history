import pytest
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.apps import apps
from django.contrib.auth.hashers import check_password
from types import SimpleNamespace

from django_password_history.models import UserPasswordHistory
from tests.factory import UserFactory


pytestmark = pytest.mark.django_db


class UserPasswordHistoryModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory(username="history_user")

    @pytestmark
    def test_str_returns_username_password_history(self):
        history = UserPasswordHistory.objects.create(user=self.user)

        assert str(history) == "history_user_password_history"


    @pytestmark
    def test_store_password_rotates_history_and_preserves_previous_passwords(self):
        self.user.set_password("initial-password")
        self.user.save()

        history = UserPasswordHistory.objects.create(user=self.user)
        history.store_password()

        first_stored = history.password_1
        assert first_stored
        assert check_password("initial-password", first_stored)

        self.user.set_password("second-password")
        self.user.save()
        history.store_password()

        assert check_password("second-password", history.password_1)
        assert check_password("initial-password", history.password_2)
        assert history.password_1 != history.password_2


    @pytestmark
    @override_settings(PREVIOUS_PASSWORD_COUNT=1)
    def test_password_is_used_checks_previous_password_count_from_settings(self):
        self.user.set_password("first-password")
        self.user.save()

        history = UserPasswordHistory.objects.create(user=self.user)
        history.store_password()

        self.user.set_password("second-password")
        self.user.save()
        history.store_password()

        assert history.password_is_used("second-password")
        assert not history.password_is_used("first-password")


    @pytestmark
    @override_settings(USE_SITE_SETTINGS_PASSWORD_HISTORY=True)
    def test_password_is_used_uses_site_settings_when_enabled(self):
        class FakeSiteSettingsManager:
            def get(self, id):
                return SimpleNamespace(previous_password_count=1)

        class FakeSiteSettings:
            objects = FakeSiteSettingsManager()

        original_get_model = apps.get_model

        def fake_get_model(app_label, model_name):
            if app_label == "setup" and model_name == "SiteSettings":
                return FakeSiteSettings
            return original_get_model(app_label, model_name)

        with patch.object(apps, "get_model", fake_get_model):

            self.user.set_password("first-password")
            self.user.save()

            history = UserPasswordHistory.objects.create(user=self.user)
            history.store_password()

            self.user.set_password("second-password")
            self.user.save()
            history.store_password()

            self.assertTrue(
                history.password_is_used("second-password", site_id=1)
            )

            self.assertFalse(
                history.password_is_used("first-password", site_id=1)
            )
