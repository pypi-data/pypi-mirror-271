# Django Allauth Themes

Themes for Django-Allauth

## Requirements

1. Django
1. Django-Allauth

## Install

```shell
pip install django-allauth-themes
```

Add your desired theme to `INSTALLED_APPS` before `allauth`:

```python
INSTALLED_APPS = [
    ...,
    'allauth_themes.allauth_bootstrap',
    'allauth_themes.bootstrap',
    ...,
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    ...
]
```

## Available Themes

1. `allauth_themes.allauth_bootstrap`
    - Example theme provided by Django-Allauth
    - Must add `path("i18n/", include("django.conf.urls.i18n")),` to `urls.py`
    ![](https://i.imgur.com/eCtNzPb.png)

1. `allauth_themes.bootstrap`
    - Basic Bootstrap 5 style
    - Blue buttons, rounded corners
    ![](https://i.imgur.com/QVSZGUf.png)
