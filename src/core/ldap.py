import ssl
from ldap3 import Server, Connection, ALL, Tls
from loguru import logger

from .settings.components.ldap import LDAP_AUTH_URL, LDAP3_USER, LDAP3_PASSWORD, LDAP_AUTH_SEARCH_BASE

server = Server(
        host=f'ldaps://{LDAP_AUTH_URL}',
        port=636,
        tls=Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1),
        get_info=ALL
)


def get_ldap_connection():
    connection = Connection(server, user=LDAP3_USER, password=LDAP3_PASSWORD, auto_bind=True)
    return connection


def search_and_modify_password(username, new_password):
    try:
        conn = get_ldap_connection()

        search_parameters = {
            'search_base': LDAP_AUTH_SEARCH_BASE,
            'search_filter': f'(&(userPrincipalName={username})(objectClass=person))',
            'attributes': ['cn', 'givenName', 'description', 'mail', 'userPrincipalName']
        }
        conn.search(**search_parameters)

        for entry in conn.response:
            attributes = entry.get("attributes", {})
            if entry.get("dn") and attributes.get("userPrincipalName") == username:
                USER_DN = entry["dn"]
                USER_CN = attributes.get("cn")

                conn.extend.microsoft.modify_password(USER_DN, new_password)
                logger.info(f"Password for user {USER_CN} change")
                return True

        logger.warning(f"User <{username}> not found")
        return False
    except Exception as e:
        logger.error(f"Error ldap: {e}")
        return False
