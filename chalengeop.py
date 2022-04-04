#!/usr/bin/env python

from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint
import json
import requests

#Conectar con mercado libre

configuration = meli.Configuration(
    host = "https://api.mercadolibre.com"
    )

with meli.ApiClient() as api_client:

    api_instance = meli.OAuth20Api(api_client)

    grant_type = 'TG-624b627ac15b8f001cfe88bf-325036294' 
    # Reemplazar por 'refresh_token' la segunda vez

    client_id = '1562860169862020' 
    # tu APP ID

    client_secret = 'yFOwOq0d6dWx5IcgTs0rMLHpgBSegGLw'
    # Tu Secret Key

    redirect_uri = '' 
    # tu Redirect URI

    code = 'https://challengeop.herokuapp.com/' 
    # Tu codigo obtenido $SERVER_GENERATED_AUTHORIZATION_CODE
    # Dejar vacio la segunda vez ya que usaremos Refresh_token

    refresh_token = '' 
    # Dejar Vacio la primera vez, y la segunda colocar refresh_token obtenido luego de actualizar.


# Este modulo se conecta con mercado libre si esta todo ok se genera la autorizacion.

try:                        
    api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, code=code, refresh_token=refresh_token)

    print(api_response)
except ApiException as e:
    print("Exception when calling OAuth20Api->get_token: %s\n" % e)    

             
# Luego de conectarse obtenemos un access_token el cual 
# lo alamcenamos en una variable (tok)
# ya que el mismo dura 6 meses y una vez que ya entremos con refresh_token
# no hay que modificar el codigo.
# Me falta resolver para que este todo automatizado , que cuando expire el acceso
# se vuelva a conectar y no hacerlo manualmente.


tok = str("Bearer ") + api_response.get("access_token")
print(tok)
'''
def extraccion():

    
    url = "https://api.mercadolibre.com/sites/MLA/search?nickname=QUIRINO+BEBIDAS&offset=1050"
    # Yo lo probe en este link y funciona.
    # Cuando lo hacemos del navegador no me deja hacerlo pero por este medio si.


    headers = {"Authorization": tok}
    res = requests.post(url, headers=headers).json()
    

    # Copia los 50 resultados que en el navegador no me dejaba y los guarda.

    results = res["results"]
    dataset = [
        {"id":x.get("id"),
        "title":x.get("title"),
        "price":x.get("price"),
        "available_quantity":x.get("available_quantity"),
        "sold_quantity":x.get("sold_quantity")
        } 
        for x in results
        ]
    print(dataset)

    



if __name__ == '__main__':

 
    extraccion()
'''

