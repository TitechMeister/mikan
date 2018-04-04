# Mikan

## Requirements
- Python3

## Setup

Install packages
```bash
pip install -r requirements.txt
```

Edit mikan/settings/local_settings.py
```python
SECRET_KEY = ""

ALLOWED_HOSTS = ["localhost"]

CORS_ORIGIN_WHITELIST = [
    "127.0.0.1:3000",
    "localhost:3000",
]

PASSWORD_RECOVERY_URL = "http://localhost:3000/recover"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_SIGNATURE = ""
EMAIL_TITLE_PREFIX = ""

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
```

Create superuser
```bash
python manage.py createsuperuser
```

## Run
```bash
python manage.py runserver
```
