import sys
import argparse
import getpass
import configparser
from ldap3 import Server, Connection, Reader, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NC='\033[0m'
    GREEN='\033[1;32m'
    RED='\033[1;31m'


def main():
    config=configparser.ConfigParser()
    config.read('settings.ini')
    server_name=config['DomainController']['server']
    parser=argparse.ArgumentParser()
    parser.add_argument("Domain",help="Domain of User account")
    parser.add_argument("userName", help="Username of account")
    parser.add_argument('--Server',help="Use this flag to specify AD server. Default is set in .env file")
    args = parser.parse_args()
    if args.Server:
        server_name=args.Server
        print(f'Using custom Domain Server: {server_name}')
    else:
        print(f"Using Default Domain Server: {server_name}")
    
    domain_name=args.Domain
    user_name=args.userName
    password=getpass.getpass()
    server=Server(server_name,use_ssl=True,get_info=ALL)
    try:
        conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password, authentication=NTLM, auto_bind=True)
        if conn:
            print(f'{bcolors.OKGREEN}Valid!{bcolors.NC}')
        else:
            print("Error")
        conn.unbind()
    except:
        print(f'{bcolors.FAIL}Invalid{bcolors.NC}')

if __name__ == "__main__":
    main()