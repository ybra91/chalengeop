
import requests

def get_access_code():
    client_id = '1562860169862020'
    redirect_uri = 'https://challengeop.herokuapp.com/'
    #scope = 'files.readwrite.all offline_access mail.readwrite'
    url = 'https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id={}&redirect_uri={}
    #url = """https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={}&scope={}
     &response_type=code&redirect_uri={}'.format(client_id, redirect_uri)
    return url
    
print(get_access_code())
