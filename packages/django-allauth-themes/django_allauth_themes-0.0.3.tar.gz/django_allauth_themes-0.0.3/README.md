# Django Allauth Themes

Themes for Django-Allauth

## Requirements

1. Django
1. Django-Allauth

## Install

```shell
pip install django-allauth-themes
```

Add your desired theme to the `DIRS` list within `TEMPLATES`

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'example' / 'templates',
            'allauth_themes/bootstrap5'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
