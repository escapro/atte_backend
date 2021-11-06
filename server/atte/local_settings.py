SECRET_KEY = 'django-insecure-trw463gewe5d^8jy651f+8(ujtert&zlt#@n$+756$5ybwr6=!fretw__234gw'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'cyborg.127.0.0.1',
    'cafe.127.0.0.1',
    'attedev',
    'cyborg.attedev',
    'http://localhost:3000',
    'http://cyborg.localhost:3000',
    'http://cafe.localhost:3000'
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://cyborg.localhost:3000',
    'http://cafe.localhost:3000'
)

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'qwe',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
