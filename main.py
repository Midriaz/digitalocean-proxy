from requests import get, post
from dotenv import dotenv_values
from sys import argv
from math import ceil
from colorama import Fore, Style
from random import choice
from string import ascii_letters
from datetime import datetime
from os import mkdir
from json import loads
from time import sleep

CREATE_DROPLET_ENDPOINT = 'https://api.digitalocean.com/v2/droplets'


def generate_password(length=12):
    return ''.join((choice(ascii_letters) for _ in range(length)))


def create_droplet(headers, name, region, tag, port, user, password):
    """
    :param headers: authentication header
    :param name: droplet name
    :param user: proxy auth
    :param password: proxy auth
    :return: dict(host, port, user, password)
    """
    # cloud config file
    # Guide: https://www.digitalocean.com/community/tutorials/how-to-use-cloud-config-for-your-initial-server-setup
    user_data = """#cloud-config
package_update: true
packages:
  - squid
  - apache2-utils
write_files:
  - path: /etc/squid/squid.conf
    content: |
      auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/htpasswd
      auth_param basic realm proxy
      acl authenticated proxy_auth REQUIRED
      http_access allow authenticated
      http_port 0.0.0.0:%s
runcmd:
  - htpasswd -b -c /etc/squid/htpasswd %s %s
  - systemctl enable squid
  - systemctl restart squid
  - ufw enable
  - ufw allow ssh
  - ufw allow 'Squid'""" % (port, user, password)
    data = {
        'name': name,
        'region': region,
        'size': 's-1vcpu-1gb',
        'image': 'ubuntu-20-04-x64',
        'tags': [tag],
        'user_data': user_data,
        'ipv6': False,
        'volumes': None,
        'backups': False,
        'private_networking': None,
        'ssh_keys': []
    }
    response = post(CREATE_DROPLET_ENDPOINT, headers=headers, data=data)
    if response.status_code in [200, 202]:
        droplet_id = loads(response.text)['droplet']['id']
        print(f'Droplet {droplet_id} was created')
        return droplet_id
    else:
        print(f'{Fore.RED}Something wrong. Response code {response.status_code}{Style.RESET_ALL}. Response body:')
        print(response.text)


if __name__ == '__main__':
    proxy_count = int(argv[1]) if len(argv) >= 2 else 1
    per_file = int(argv[2]) if len(argv) >= 3 else 1

    config = dotenv_values('.env')
    config['PROXY_PORT'] = config.get('PROXY_PORT', '3128')
    headers = {'Authorization': f'Bearer {config["AUTH_TOKEN"]}'}

    # output format
    # 0 - TXT format "host:port:user:password",
    # 1 - for Ghost browser, CSV, "name:host:port:user:password:tags"
    out_format = int(config['GHOST_BROWSER_FORMAT']) if 'GHOST_BROWSER_FORMAT' in config else 0

    # make output dir
    date_tag = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    out_dir = f'./proxy_{date_tag}'
    mkdir(out_dir)

    # droplet list
    droplets = []

    if input(f'Do you really want to create {Fore.YELLOW}{proxy_count}{Style.RESET_ALL} droplets '
             f'and import them to {Fore.YELLOW}{ceil(proxy_count/per_file)}{Style.RESET_ALL} files? '
             f'It will cost you {Fore.YELLOW}~{int(config["DROPLET_PRICE"])/30:.2f}${Style.RESET_ALL} per day. '
             f'{Fore.GREEN}Print "y" to confirm.{Style.RESET_ALL} ') == 'y':
        for i in range(proxy_count):
            droplet_name = f'p{i+1:04d}'
            password = generate_password()
            droplet_id = create_droplet(headers,
                                        droplet_name,
                                        config['REGION'],
                                        config['DROPLET_TAG'],
                                        config['PROXY_PORT'],
                                        config['PROXY_USER'],
                                        password)
            if droplet_id is not None:
                # log id of droplets
                f = open(f'{out_dir}/droplets.log', 'a')
                f.write(f'{droplet_id}\r\n')
                f.close()

                droplets.append({
                    'id': droplet_id,
                    'name': droplet_name,
                    'port': config['PROXY_PORT'],
                    'user': config["PROXY_USER"],
                    'password': password
                })

        pi = 0  # proxy count
        while pi < len(droplets):
            sleep(5)
            for i, drop in enumerate(droplets):
                if 'host' not in drop:
                    response = get(f'{CREATE_DROPLET_ENDPOINT}/{drop["id"]}', headers=headers)
                    if response.status_code == 200:
                        network = loads(response.text)['droplet']['networks']['v4']
                        if len(network) > 1:
                            pi += 1

                            droplets[i]["host"] = network[1]['ip_address']
                            drop['host'] = droplets[i]["host"]
                            if out_format == 1:
                                proxy_str = f'{droplet_name},{drop["host"]},{drop["port"]},{drop["user"]},{drop["password"]},DO'
                            else:
                                proxy_str = f'{drop["host"]}:{drop["port"]}:{drop["user"]}:{drop["password"]}'

                            ext = 'csv' if format == 1 else 'txt'

                            file_no = ceil((pi+1)/per_file)
                            f = open(f'{out_dir}/{file_no:03d}.{ext}', 'a')
                            f.write(proxy_str+'\r\n')
                            f.close()
                    else:
                        drop["host"] = '0.0.0.0'
                        print(f'{Fore.RED}Failed to get host info. Response code {response.status_code}{Style.RESET_ALL}. Response body:')
            print(f'Got IP for {pi} droplets of {len(droplets)}')

