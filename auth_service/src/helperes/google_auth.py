from authlib.integrations.starlette_client import OAuth

from core.config import app_settings

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=app_settings.client_id,
    client_secret=app_settings.client_secret,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': app_settings.redirect_url,
    }
)
