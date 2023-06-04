# digitalocean-proxy
This Python script enables the creation of droplets that function as proxy servers. Offering a cost-effective solution, it is an excellent choice if you're seeking high-quality, private IPv4 proxies for one-day usage.

## Features
- Automated droplet creation with specific configuration
- Password generation for each droplet
- Logging of droplet details (host, port, user, password)
- Option to generate proxy details in TXT or CSV format

## Disclaimer
This script will create droplets on your DigitalOcean account and therefore will incur costs. Please be aware of this before running the script. It will provide you an estimate of the cost based on the DROPLET_PRICE variable in the .env file and the number of droplets you wish to create, and it will ask for your confirmation before proceeding.

## Environment Configuration

The script uses a `.env` file to read configuration details. A sample `.env` file might look like this:
- `AUTH_TOKEN`: Your DigitalOcean authorization token.
- `PROXY_PORT`: The port to be used for the proxy. Default is 3128.
- `REGION`: The region in which the droplet should be created.
- `DROPLET_TAG`: A tag for your droplet.
- `PROXY_USER`: The username for the proxy.
- `DROPLET_PRICE`: The price of the droplet (for cost calculation).
- `GHOST_BROWSER_FORMAT`: The output format for the droplet details (`0` for TXT, `1` for CSV).

```
AUTH_TOKEN='your_digitalocean_access_token'
PROXY_USER='proxy'
DROPLET_PRICE=6
GHOST_BROWSER_FORMAT=0
REGION='ams3'
DROPLET_TAG='autoproxy'
```

## Usage

Run the script from the command line with the following command:

```bash
python main.py [proxy_count] [per_file]
```

* proxy_count: The number of droplets to create (default: 1).
* per_file: The number of droplets' details to store per file (default: 1).

* The script will create a new directory ./proxy_{date_tag}, where the droplet details will be stored in either TXT or CSV format, depending on the GHOST_BROWSER_FORMAT variable in the .env file.