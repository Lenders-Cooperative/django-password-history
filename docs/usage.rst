=====
Usage
=====

To use django-password-history in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_password_history.apps.DjangoPasswordHistoryConfig',
        ...
    )

Add django-password-history's URL patterns:

.. code-block:: python

    from django_password_history import urls as django_password_history_urls


    urlpatterns = [
        ...
        url(r'^', include(django_password_history_urls)),
        ...
    ]
