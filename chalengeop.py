
import requests

def get_access_code():
    client_id = '1562860169862020'
    redirect_uri = 'https://challengeop.herokuapp.com/'
    url = 'https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id={}&redirect_uri={}&response_type=code&redirect_uri={}'.format(client_id, redirect_uri)
    return url
    
print(get_access_code())
