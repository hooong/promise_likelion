"""
Django settings for saekki_pro project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_SECRET_DIR = os.path.join('/srv/', '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')
config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_secret_common['django']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'promise',
    'accounts',
    'django_apscheduler',

    # allauth 추가
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saekki_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['saekki_pro/templates'],
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

WSGI_APPLICATION = 'saekki_pro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saekki',				
        'USER': config_secret_common['django']['db_user'],			
        'PASSWORD': config_secret_common['django']['db_pw'],		
        'HOST': config_secret_common['django']['db_host'],
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

# USE_I18N = True

# USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'promise', 'static'),
    os.path.join(BASE_DIR, 'saekki_pro', 'static'),
]   

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')   #medai폴더로 파일들을 모으겠다는 의미
MEDIA_URL = '/media/'   #URL설정


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = '/'

APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"

# allauth 추가
AUTHENTICATION_BACKENDS = [ 'django.contrib.auth.backends.ModelBackend', # 기본 인증 백엔드
'allauth.account.auth_backends.AuthenticationBackend', # 추가 
]
# 디폴트 SITE의 id
# 등록하지 않으면,각 요청 시에 host명의 Site 인스턴스를 찾습니다.
SITE_ID =1
# 이메일 확인을 하지 않음.
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none' # 아니면  smtp 로 설정
SOCIALACCOUNT_AUTO_SIGNUP = True

ACCOUNT_FORMS = {
'signup': 'accounts.forms.CustomSignupForm',
}