import requests
from requests.auth import HTTPBasicAuth

def get_access_token():
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth('AYlokKpuubb3q2nuuljFig5GQQpIpBND7vgJcYfEjE4RQuWVIo5cZ1HAno57BQcfkIUyfyxly9TlgsOz', 'EJ9x-FXO7IXEOxaSNgm-qtb2OveCMSqUl7D26zSBVujwxp_uDv6VsMOc6FDqdK1bMu-Vrk6VVm3PTxXe'))
    return response.json()['access_token']