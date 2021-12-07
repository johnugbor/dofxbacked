import django_heroku
"""
In requirements.txt set PyJWT==1.7.1 2.0 and have compatibility issues 
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'igmcaccount.User'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
     'corsheaders',
     'drf_jwt_2fa',


    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
   
    
   
    #account',
    'igmcaccount',
    #transaction
    'trade',
   
    
    


]

devId = 1
prodId = 2
siteId = devId
SITE_ID = siteId
MIDDLEWARE = [
    
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'backend/templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases




#Productiondb
PRODUCTION_DATABASES = {
    'default': {

        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': env('NAME'),
        'USER': env('USER'),  
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT':env('DB_PORT'),


    }
}


DEFAULT_FROM_EMAIL ='mrjohnugbor@gmail.com'
#developmentdb1
DEVELOPMENT_DATABASES1 = {
    'default': {

        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'azubackend', 
        'USER': 'onyeisijohnl', 
        'PASSWORD': 'egooyibo',
        'HOST': '127.0.0.1', 
        'PORT':'5432',


    }
}


#developmentdb2
DEVELOPMENT_DATABASES2 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = PRODUCTION_DATABASES

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


CSRF_COOKIE_SECURE = False  # To allow http sites

SITE_ID = siteId

AUTHENTICATION_BACKENDS = [
   'django.contrib.auth.backends.ModelBackend',

   # to allow the use of username_email option for login.
   'allauth.account.auth_backends.AuthenticationBackend'
]
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
CSRF_COOKIE_SECURE = False  # To allow http sites

DEV_WHITE_LIST = ["http://localhost:3000",
                    "https://dofxplus.netlify.app",
                        "http://127.0.0.1:8000",
                        "https://webtrader.igmc.uk",
                        "https://igmcbackend.herokuapp.com",
                        ]
PROD_WHITE_LIST= [
                    "https://webtrader.igmc.uk",
                    "https://igmcbackend.herokuapp.com",
                        ]

CORS_ORIGIN_WHITELIST = PROD_WHITE_LIST

DEV_CORE_ORIGINS =["https://dofxplus.netlify.app",
                    "https://webtrader.igmc.uk",
                    "http://localhost:3000",
                        ]
PROD_CORE_ORIGINS=[ "https://dofxplus.netlify.app",
                    "https://webtrader.igmc.uk",
                        
                        ]

CSRF_TRUSTED_ORIGINS = PROD_CORE_ORIGINS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]                       
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER':'igmcaccount.serializers.CustomUserDetailsSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'igmcaccount.serializers.CustomRegisterSerializer'
}

REST_FRAMEWORK = { 

'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

'DEFAULT_AUTHENTICATION_CLASSES':[
   
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    'drf_jwt_2fa.authentication.Jwt2faAuthentication',

    ],
}



JWT2FA_AUTH = {
    # Length of the verification code (digits)
    'CODE_LENGTH': 7,

    # Characters used in the verification code
    'CODE_CHARACTERS': '0123456789',

    # Secret key to use for signing the Code Tokens
    'CODE_TOKEN_SECRET_KEY': env('TOKEN_SECRET'),

    # Secret string to extend the verification code with
    'CODE_EXTENSION_SECRET': env('CODE_SECRET'),

    # How long the code token is valid
    'CODE_EXPIRATION_TIME': timedelta(minutes=15),

    # Throttle limit for code token requests from same IP
    'CODE_TOKEN_THROTTLE_RATE': '12/3h',

    # How much time must pass between verification attempts, i.e. to
    # request authentication token with a with the same code token and a
    # verification code
    'AUTH_TOKEN_RETRY_WAIT_TIME': timedelta(seconds=2),

    # Function that sends the verification code to the user
    'CODE_SENDER': 'drf_jwt_2fa.sending.send_verification_code_via_email',

    # From Address used by the e-mail sender
    'EMAIL_SENDER_FROM_ADDRESS': DEFAULT_FROM_EMAIL,

    # Set to this to a (translated) string to override the default
    # message subject of the e-mail sender
    'EMAIL_SENDER_SUBJECT_OVERRIDE': None,

    # Set to this to a (translated) string to override the default
    # message body of the e-mail sender
    'EMAIL_SENDER_BODY_OVERRIDE': None,
}

REST_USE_JWT = True

JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH = {
    # Authorization:Token xxx
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
REST_USE_JWT = True

#heroku gmail config
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS= True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.gmail.com'

#console email test
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025


#production
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = env('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
#EMAIL_PORT = env('EMAIL_PORT')
#EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', '')
#EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '')
#EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
#EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'access',

    
}
ACCOUNT_ADAPTER = 'igmcaccount.adapter.DefaultAccountAdapterCustom'
URL_FRONT = 'webtrader.igmc.uk'
# dev
#LOGIN_URL = 'http://localhost:8000/account/login/'
#prod
LOGIN_URL ='https://backend.herokuapp.com/login'
# Activate Django-Heroku.
django_heroku.settings(locals())                        