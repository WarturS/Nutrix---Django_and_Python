from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configurações de Segurança e Ambiente ---

# !!! ATENÇÃO: Substitua por uma chave secreta real em produção !!!
SECRET_KEY = 'sua_chave_secreta_aqui' 

DEBUG = True

ALLOWED_HOSTS = []

# --- Aplicações Instaladas ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nutrix',  # Nosso app principal
    'widget_tweaks',
]

# --- Middlewares ---

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Configurações de URL e Templates ---

# CORREÇÃO APLICADA: 'config' é o nome da sua pasta de projeto
ROOT_URLCONF = 'config.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Opcional: para templates globais
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

# CORREÇÃO APLICADA: 'config' é o nome da sua pasta de projeto
WSGI_APPLICATION = 'config.wsgi.application' 

# --- Banco de Dados (SQLite Padrão) ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Validação de Senha (Padrão) ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- Internacionalização e Fuso Horário ---

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- Arquivos Estáticos ---

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"] # Garante que a pasta static que você criou seja lida

# --- Configurações de Login Personalizadas ---

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/clientes/'

# --- Padrão de ID ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'