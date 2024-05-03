# Roco - Runtime config generator

Command line utility which prints to the standard output javascript valid 
text generated from environment variables.

For example, given following environment variables:

    PAPERMERGE__AUTH__OIDC_CLIENT_ID=papermerge
    PAPERMERGE__AUTH__OIDC_AUTHORIZE_URL=http://keycloak.trusel.net:8080/realms/myrealm/protocol/openid-connect/auth
    PAPERMERGE__AUTH__OIDC_REDIRECT_URL=http://demo.trusel.net:12000/oidc/callback
    PAPERMERGE__AUTH__OIDC_LOGOUT_URL=http://keycloak.trusel.net:8080/realms/myrealm/protocol/openid-connect/logout

will result in the following text (valid javascript) as output:

    window.__PAPERMERGE_RUNTIME_CONFIG__ = {
      oidc: {
          client_id: 'papermerge',
          authorize_url: 'http://keycloak.trusel.net:8080/realms/myrealm/protocol/openid-connect/auth',
          redirect_url: 'http://demo.trusel.net:12000/oidc/callback',
          logout_url: 'http://keycloak.trusel.net:8080/realms/myrealm/protocol/openid-connect/logout'
          scope: 'openid email',
      }
    };

## Install

    pip install roco

## Usage

If no relevant environment variables were defined just running:

    roco

Will result in following output:

    window.__PAPERMERGE_RUNTIME_CONFIG__ = {
    };

i.e. valid, but empty, javascript object.
In order to see current roco's pydantic settings (read from env vars)
run:
    
    roco --settings

The above command will also show the env var prefix i.e. `PAPERMERGE__AUTH__`.

Roco reads from following environment variables:

* `PAPERMERGE__AUTH__OIDC_AUTHORIZE_URL`
* `PAPERMERGE__AUTH__OIDC_CLIENT_ID`
* `PAPERMERGE__AUTH__OIDC_REDIRECT_URL`
* `PAPERMERGE__AUTH__OIDC_LOGOUT_URL`
* `PAPERMERGE__AUTH__OIDC_SCOPE`
