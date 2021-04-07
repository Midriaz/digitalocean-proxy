from requests import delete
from dotenv import dotenv_values
from sys import argv
from colorama import Fore, Style

DELETE_DROPLET_ENDPOINT = 'https://api.digitalocean.com/v2/droplets'

if __name__ == '__main__':
    by_tag = True if len(argv) <= 1 else False

    config = dotenv_values('.env')
    headers = {'Authorization': f'Bearer {config["AUTH_TOKEN"]}'}

    if by_tag:
        if input(f'Do you want to delete ALL droplets with tag name {config["DROPLET_TAG"]}? '
                 f'Print "yes" to continue. ') == 'yes':
            response = delete(f'{DELETE_DROPLET_ENDPOINT}?tag_name={config["DROPLET_TAG"]}', headers=headers)
            if response.status_code in [200, 204]:
                print(f'{Fore.GREEN}Droplets destroyed{Style.RESET_ALL}')
            else:
                print(f'{Fore.RED}Error while destoying droplets. Response code {response.status_code}{Style.RESET_ALL}. '
                      f'Response body:')
                print(response.text)

    else:
        f = open(argv[1], 'r')
        ids = f.readlines()
        f.close()

        if input(f'{len(ids)} droplets will be destroyed. Print "yes" to continue. ') == 'yes':
            for i in ids:
                response = delete(f'{DELETE_DROPLET_ENDPOINT}/{i}', headers=headers)
                if response.status_code in [200, 204]:
                    print(f'{Fore.GREEN}Droplet {i} destroyed{Style.RESET_ALL}')
                else:
                    print(f'{Fore.RED}Error while destoying {i}. Response code {response.status_code}{Style.RESET_ALL}. '
                          f'Response body:')
                    print(response.text)
