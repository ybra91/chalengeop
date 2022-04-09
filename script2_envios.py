# -*- coding: utf-8 -*-
import requests
import json
import string
from datetime import datetime, timedelta, tzinfo, time
import dateutil.parser
import csv
import pandas as pd


        
#Abrimos archivo del acceso y la SO en modo lectura
lista_envios = open("Envios_ID.txt","r")
listEnvios = lista_envios.readlines()
lista_envios.close()

envios = []

#Los pásamos a una lista
for i in listEnvios:
	envios.append(i.strip('\n'))

###PRIMERA VEZ USANDO LA API DEL TOKEN
'''
url = "https://api.mercadolibre.com/oauth/token"
payload={'grant_type': 'authorization_code',
'client_id': '1562860169862020',
'client_secret': 'yFOwOq0d6dWx5IcgTs0rMLHpgBSegGLw',
'code': 'TG-624b9e8de5a601001b47e910-325036294',
'redirect_uri': 'https://challengeop.herokuapp.com/'
}
headers = {
'accept': 'application/json',
'content-type': 'application/x-www-form-urlencoded'
}
'''
##DESPUES DE HABERME CONECTADO POR PRIMERA VEZ
url = "https://api.mercadolibre.com/oauth/token"
payload={'grant_type': 'refresh_token',
'client_id': '1562860169862020',
'client_secret': 'yFOwOq0d6dWx5IcgTs0rMLHpgBSegGLw',
'refresh_token': 'TG-624b9e8de5a601001b47e910-325036294',
'redirect_uri': 'https://challengeop.herokuapp.com/',
'refresh_token':'TG-624b9ea91d4346001a68627e-325036294'
}
files=[
]
headers = {
'accept': 'application/json',
'content-type': 'application/x-www-form-urlencoded'
}
response = requests.request("POST", url, headers=headers, data=payload)
json_token = json.loads(response.text)
#Guardo el id de mi usuario y el token
for i in json_token:
	if i == 'access_token':
		access_token = json_token[i]
for a in envios:
	headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
	payload = {}
	url1 = 'https://api.mercadolibre.com/shipments/'+str(a)
	try:
		r2 = requests.get(url1, headers=headers)
	except:
			print(r2.text)
	else:
		#BUSCAMOS EL ESTADO
		json_shipments_origin = json.loads(r2.text)
		status = json_shipments_origin['status']
		tipo_logistica = json_shipments_origin['logistic_type']
		origen_envio = json_shipments_origin['sender_address'].get('name')
		id_metodo_envio = json_shipments_origin['shipping_option'].get('shipping_method_id')
		json_fecha_estimada = id_metodo_envio = json_shipments_origin['shipping_option'].get('estimated_delivery_time')
		fecha_estimada = json_fecha_estimada['date']
		json_fecha_final = id_metodo_envio = json_shipments_origin['shipping_option'].get('estimated_delivery_final')
		fecha_final = json_fecha_final['date']
		
		#BUSCAMOS EL ORIGEN
		headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
		url2 = 'https://api.mercadolibre.com/shipments/'+str(a)+'/costs'
		r3 = requests.get(url2, headers=headers)
		json_shipments_cost = json.loads(r3.text)
		json_deposito_envio = json_shipments_cost['receiver'].get('cost_details')
		deposito_envio = json_deposito_envio[0].get('sender_id')
		if deposito_envio == '4321345667':
			deposito = "Deposito Mercado Libre"
		else:
			deposito = "Deposito Vendedor"
			
		#ESTIMACION ENTREGA
		url3 = 'https://api.mercadolibre.com/shipments/'+str(a)+'/lead_time'
		r4 = requests.get(url3, headers=headers)
		json_shipments_time = json.loads(r4.text)
		dia_entrega = json_shipments_time['estimated_delivery_time'].get('date')

		#ENVIOS ENTREGADOS FUERA DE LA PRIMERA VENTANA ESTIMADA
		#CONVERTIR FECHA (YYYY-mm-ddTHH:MM:SS.mmmZ)
		fecha_final_date= dateutil.parser.parse(fecha_final, ignoretz=True)
		fecha_estimada_date = dateutil.parser.parse(fecha_estimada,ignoretz=True)
		fecha_demora=(fecha_final_date)-(fecha_estimada_date)
		hh = fecha_demora.days * 24
		mm = hh * 60
		ss = mm * 60
		fecha_demora_hhmmss = ("horas: "+str(hh)," minutos: "+str(mm)," segundo: "+str(ss))

		#INSERTAMOS EN LOS EXCELS
		f= open("TesGOML2_1.csv", 'w')
		csv_write = csv.writer(f)
		csv_write.writerow(['Status_Envio','Tipo_Logistica','Origen_Envio','Deposito', 'Fecha_Entrega','Demora_hhmmss'])
		csv_write.writerow([status,tipo_logistica,origen_envio,deposito,dia_entrega,fecha_demora_hhmmss])
		f2= open("TesGOML2_2.csv", 'w')
		csv_write = csv.writer(f2)
		csv_write.writerow(['Status_Envio','Tipo_Logistica','Origen_Envio','Deposito','Fecha_Entrega','Demora_hhmmss'])
		csv_write.writerow([status,tipo_logistica,origen_envio,deposito,dia_entrega,fecha_demora_hhmmss])
		f.close()
		f2.close()
		
		#ORDENAR LA COLUMNA DE FECHA DE ENTREGA DE MAYOR A MENOR
		data = pd.read_csv('TesGOML2_1.csv')
		data1 = pd.read_csv('TesGOML2_2.csv')
		data['Fecha_Entrega'] = pd.to_datetime(data.Fecha_Entrega, infer_datetime_format = True)
		data1['Fecha_Entrega'] = pd.to_datetime(data.Fecha_Entrega, infer_datetime_format = True)
		data.sort_values(by = 'Fecha_Entrega', ascending = True, inplace = True)
		data1.sort_values(by = 'Fecha_Entrega', ascending = True, inplace = True)


