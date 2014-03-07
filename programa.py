#encoding=utf-8
import requests
from lxml import etree
from jinja2 import Template
import webbrowser
import os

provincias = ['Almeria','Granada','Cadiz','Cordoba','Huelva','Jaen','Malaga','Sevilla']

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
	p = {'q':provincia ,'mode':'xml','units':'metric','lang':'sp'}
	respuesta = requests.get('http://api.openweathermap.org/data/2.5/weather',params=p)
	datos =  etree.fromstring(respuesta.text.encode("utf-8"))
	viento1 = datos.find("wind/speed")
	orienta = datos.find("wind/direction")
	temperatura = datos.find("temperature")
	orientacion = float(orienta.attrib["value"])
	tempmax = round(float(temperatura.attrib["max"]),1)
	tempmin = round(float(temperatura.attrib["min"]),1)
	viento = viento1.attrib["value"]
	orientacion1 = direccion(orientacion)
	listaorientacion.append(orientacion1)
	listatemp_min.append(tempmin)
	listatemp_max.append(tempmax)
	listaviento.append(viento)
	
	



template1 = Template(html)
template1 = template1.render(provincias=provincias,temp_min=listatemp_min,temp_max=listatemp_max,viento=listaviento,direccion=listaorientacion)
web.write(template1)
webbrowser.open('web.html')
