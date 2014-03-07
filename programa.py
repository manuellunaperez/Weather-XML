#encoding=utf-8
import requests
import json
from jinja2 import Template
import webbrowser
import os

provincias = ['Almeria','Cadiz','Cordoba','Huelva','Jaen','Malaga','Sevilla']

f = open('template.html','r')
web = open('web.html','w')
html = ''


def direccion(orientacion):
	for degree in str(orientacion):
		if (orientacion > 337.5 and orientacion <= 360) or (orientacion >= 0 and orientacion < 22.5):
			return 'N'
		elif orientacion >= 22.5 and orientacion <= 67.5:
			return 'NE'
		elif orientacion > 67.5 and orientacion < 112.5:
			return 'E'
		elif orientacion >= 112.5 and orientacion <= 157.5:
			return 'SE'
		elif orientacion > 157.5 and orientacion < 202.5:
			return 'S'
		elif orientacion >= 202.5 and orientacion <= 245.5:
			return 'SO'
		elif orientacion > 245.5 and orientacion < 292.5:
			return 'O'
		elif orientacion >= 292.5 and orientacion <= 337.5:
			return 'NO'


for linea in f:
	html += linea


listaviento = []
listaorientacion = []
listatemp_min = []
listatemp_max = []




for provincia in provincias:
	respuesta = requests.get('http://api.openweathermap.org/data/2.5/weather',params={'q':'%s,spain' % provincia})
	datos = json.loads(respuesta.text)
	viento1 = datos["wind"]["speed"]
	orienta = datos["wind"]["deg"]
	tempmax1 = datos['main']['temp_max']
	tempmin1 = datos['main']['temp_min']
	tempmax = round(tempmax1 - 273,1)
	tempmin = round(tempmin1 - 273,1)
	viento = round(viento1*1.61)
	orientacion = direccion(orienta)
	listaorientacion.append(orientacion)
	listatemp_min.append(tempmin)
	listatemp_max.append(tempmax)
	listaviento.append(viento)


template1 = Template(html)
template1 = template1.render(provincias=provincias,temp_min=listatemp_min,temp_max=listatemp_max,viento=listaviento,direccion=listaorientacion)
web.write(template1)
webbrowser.open('web.html')
