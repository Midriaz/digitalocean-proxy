# digitalocean-proxy
Python script that creates droplets as proxy servers. It is cheapest option if you want good quality private one-day ip4 proxy. 

# RUN
Before run you must create .env file in project directory. Example:
```
AUTH_TOKEN='your_digitalocean_access_token'
PROXY_USER='proxy'
DROPLET_PRICE=5
GHOST_BROWSER_FORMAT=1
REGION='ams3'
DROPLET_TAG='autoproxy'
```