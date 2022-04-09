# -*- coding: utf-8 -*-
import requests
import json
import string
import csv


#Abrimos archivo del acceso y la SO en modo lectura
lista_ordenes = open("Ordenes_ID.txt","r")
listOrdenes = lista_ordenes.readlines()
lista_ordenes.close()

ordenes = []

#Los pásamos a una lista
for i in listOrdenes:
	ordenes.append(i.strip('\n'))

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
##DESPUES DE CONECTAR POR PRIMERA VEZ
url = "https://api.mercadolibre.com/oauth/token"
payload={'grant_type': 'refresh_token',
'client_id': '1562860169862020',
'client_secret': 'yFOwOq0d6dWx5IcgTs0rMLHpgBSegGLw',
'refresh_token': 'TG-624b9e8de5a601001b47e910-325036294',
'redirect_uri': 'https://challengeop.herokuapp.com/',
'refresh_token':'TG-624b9ea91d4346001a68627e-325036294'
}
headers = {
'accept': 'application/json',
'content-type': 'application/x-www-form-urlencoded'
}
response = requests.request("POST", url, headers=headers, data=payload)
json_token = json.loads(response.text)

#GUARDAR TOKER Y USUARIO
for i in json_token:
	if i == 'user_id':
		user_id = json_token[i]
	if i == 'access_token':
		access_token = json_token[i]

#INFORMACION DE LA ORDEN
for a in ordenes:
	headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
	url1 = 'https://api.mercadolibre.com/orders/'+str(a)
	try:
		r = requests.get(url1, headers=headers)
	except:
		print('Orden no encontrada, por favor revisar')
	else:
		json_order = json.loads(r.text)
		json_order_items = json_order['order_items'][0].get('item')
		title = json_order_items["title"]
		variation_color = json_order_items["variation_attributes"][0].get('value_name')
		variation_talla = json_order_items["variation_attributes"][1].get('value_name')
		precio = json_order['order_items'][0].get("unit_price")
		total_precio = json_order['total_amount']
		moneda = json_order['payments'][0].get('currency_id')
		id_payment = json_order['payments'][0].get('id')
		shipping_id = json_order['shipping'].get('id')
		
		#INFORMACION DEL ENVIO
		headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
		payload = {}
		url1 = 'https://api.mercadolibre.com/shipments/'+str(shipping_id)
		r2 = requests.get(url1, headers=headers)
		json_shipments_origin = json.loads(r2.text)
		#TIPO DE LOGISTICA
		logistica_origen = json_shipments_origin['logistic_type']
		envio_origen = json_shipments_origin['tracking_method']
		#INFORMACION DEL CARRIER
		domicilio_tipo = json_shipments_origin['carrier_info']
		if domicilio_tipo == None:
			carrier= 0
		else:
			headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
			payload = {}
			url1 = 'https://api.mercadolibre.com/shipments/'+str(shipping_id)+'/carrier'
			r3 = requests.get(url1, headers=headers)
			json_shipments_carrier = json.loads(r3.text)
			carrier = json_shipments_carrier['name']
			
		#DIRECCION DE DIRECCION DE ENVIO
		pais_json = json_shipments_origin['receiver_address'].get('country')
		pais = pais_json['name']
		estado_json = json_shipments_origin['receiver_address'].get('state')
		estado = estado_json['name']
		barrio_json = json_shipments_origin['receiver_address'].get('city')
		barrio = barrio_json['name']
		calle_json = json_shipments_origin['receiver_address'].get('address_line')
		codigo = json_shipments_origin['receiver_address'].get('zip_code')
		direccion_entrega = pais+' '+estado+' '+barrio+' '+calle_json+' '+'codigo postal:'+codigo
		
		#COSTOS DEL ENVIO
		headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
		payload = {}
		url1 = 'https://api.mercadolibre.com/shipments/'+str(shipping_id)+'/costs'
		r4 = requests.get(url1, headers=headers)
		json_shipments_cost = json.loads(r4.text)
		costo_envio = json_shipments_cost['receiver'].get('cost')
		headers = {'Accept': 'application/json','content-type': 'application/json', 'Authorization': 'Bearer '+ str(access_token)}
		payload = {}
		
		#INFORMACION DE ENTREGA DEL ENVIO
		url1 = 'https://api.mercadolibre.com/shipments/'+str(shipping_id)+'/lead_time'
		r5 = requests.get(url1, headers=headers)
		json_shipments_time = json.loads(r5.text)
		tipo_costo = json_shipments_time['cost_type']
		dia_entrega = json_shipments_time['estimated_delivery_time'].get('date')
		promesa_entrega = json_shipments_time['delivery_promise']
		fecha_promesa_entrega = json_shipments_time['estimated_delivery_limit']
		tipo_ntrega = json_shipments_time['delivery_type']
		
		#GUARDO INFORMACION DEL EXCEL
		f= open("TesGOML.csv", 'w')
		csv_write = csv.writer(f)
		csv_write.writerow(['Nombre','VariacionColor','VariacionTalla','Precio','PagoRealizado','Moneda','Logistica_Origen','Origen','Carrier','Entrega','Costo_Envio','Tipo_Costo','Dia_Entrega','Promesa_Entrega','Entrega_Estimada'])
		csv_write.writerow([title,variation_color,variation_talla,precio,total_precio, moneda, logistica_origen,envio_origen,carrier,direccion_entrega,costo_envio,tipo_costo,dia_entrega,promesa_entrega, tipo_ntrega])
		f.close()
			






