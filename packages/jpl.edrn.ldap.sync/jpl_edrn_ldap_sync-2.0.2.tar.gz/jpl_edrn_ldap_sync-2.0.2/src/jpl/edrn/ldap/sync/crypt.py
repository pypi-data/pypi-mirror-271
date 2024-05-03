# encoding: utf-8

'''💀 Find all users using older CRYPT password.'''

from . import VERSION
from .constants import USER_CLASS, USER_BASE
from .utils import add_logging_arguments, add_ldap_arguments, get_manager_password
import sys, ldap, argparse, logging

__version__ = VERSION
_logger = logging.getLogger(__name__)
_prog_desc = 'Find all user using older CRYPT passwords'
SCOPE = 'one'


def main():
    '''Here we go. Rooster sound.'''
    parser = argparse.ArgumentParser(description=_prog_desc)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    add_logging_arguments(parser)
    add_ldap_arguments(parser)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s %(message)s')
    connection = ldap.initialize(args.url)
    password = get_manager_password(args)
    connection.simple_bind_s(args.manager_dn, password)

    all_users = connection.search_s(
        USER_BASE, ldap.SCOPE_ONELEVEL, f'(objectClass={USER_CLASS})', ['userPassword', 'description']
    )
    for dn, attrs in all_users:
        if 'userPassword' not in attrs:
            print(dn, 'Missing password')
        else:
            password = attrs['userPassword'][0].decode('utf-8')
            if password.startswith('{CRYPT}'):
                description = attrs['description'][0].decode('utf-8')
                if description.startswith('imported via'): continue
                uid = dn.split(',')[0][4:]
                print(f'{uid} has older CRYPT password; {description}')

    sys.exit(0)


if __name__ == '__main__':
    main()
