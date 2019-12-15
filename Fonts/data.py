#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:06:02 2019

@author: raulf
"""
"""
import json

filename='es_product1.json'

with open(filename) as F:
    json_data = json.load(F)
"""

#%%
"""
import xml.etree.ElementTree as ET
root = ET.parse('es_product9.xml').getroot()

for type_tag in root.findall('bar/type'):
    value = type_tag.get('Discored id')
    print(value)
"""
#%%
"""
#f = open("es_product1.json", "r",encoding="ascii")
f = open("jsonrarebot.json", "r",encoding="utf8")
data=f.read()
links=[]
name=[]

a=1
inici=0
while a!=-1:
    ini1=data[inici:].find('"link"')
    inici+=ini1+6
    ini2=data[inici:].find('"')
    inici+=ini2+1
    final=data[inici:].find('"')
    links.append(data[inici:inici+final])
    
    
    ini1=data[inici:].find('"label"')
    inici+=ini1+7
    ini2=data[inici:].find('"')
    inici+=ini2+1
    final=data[inici:].find('"')
    name.append(data[inici:inici+final])

    a=data[inici:].find('"link"')
"""
#%%


from requests import get
from bs4 import BeautifulSoup
# Defineixo la base que s'haura d'afegir a tots els links,amb el 
# link principal amb el qual començar
base='https://www.orpha.net/consor/cgi-bin/'
url = 'https://www.orpha.net/consor/cgi-bin/Clinics_ERN.php?lng=EN'

response = get(url)    
html_soup = BeautifulSoup(response.text, 'html.parser')


center_containers = html_soup.find_all('div', class_ = 'ERN')
first=center_containers[0]

tipus=[]
mal=[]
i=0
for tag in first.ul.find_all("li", recursive=True):     
    if tag.a.has_attr('href'):
        tipus.append(tag.a.text.lower())
        ini=tag.a.text.find('-')
        nom=tag.a.text[ini+2:]
        mal.append('mal%s'%i)
        exec('mal%s={}'%i)
        eval('mal%s'%i)['link']=tag.a.attrs['href']
        i+=1
        
#%%
#for i in mal:
        
def check(inf):
    nums=[]
    for i in tipus:
        if inf in i:
            nums.append(tipus.index(i))
    return nums
check('cancer')
            
def infor(a):
    for i in a:
        i='mal'+str(i)
        url = base+eval(i)['link']
        response1 = get(url)
        html_soup1= BeautifulSoup(response1.text, 'html.parser') 
        centers = html_soup1.find_all('div', class_ = 'activityLoc')
        first1=centers[0]
        for tag in first1.find_all("div", recursive=True):
            if tag.strong!=None:
                if tag.strong.text not in eval(i):
                    eval(i)[tag.strong.text]=[]
                pais=tag.strong.text
            if tag.p!=None:
                city=tag.p.text
        #        if city not in mal11[pais][0]:
        #            mal11[tag.strong.text][0].append(city)
            if tag.a!=None:
                if [tag.a.attrs['href'],city] not in eval(i)[pais]:
                    eval(i)[pais].append([tag.a.attrs['href'],city])
                

            
"""
i='mal11'
    url = base+eval(i)['link']
    response1 = get(url)
    html_soup1= BeautifulSoup(response1.text, 'html.parser') 
    centers = html_soup1.find_all('div', class_ = 'activityLoc')
    first1=centers[0]
    for tag in first1.find_all("div", recursive=True):
        if tag.strong!=None:
            if tag.strong.text not in eval(i):
                eval(i)[tag.strong.text]=[]
            pais=tag.strong.text
        if tag.p!=None:
            city=tag.p.text
    #        if city not in mal11[pais][0]:
    #            mal11[tag.strong.text][0].append(city)
        if tag.a!=None:
            if [tag.a.attrs['href'],city] not in eval(i)[pais]:
                eval(i)[pais].append([tag.a.attrs['href'],city])
                
for tag in first1.find_all("div", class_='col-xs-12 col-md-3',recursive=True):     
        print(tag.a.attrs['href'])
"""
#%%
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")

location = geolocator.geocode("Dresden")
print(location.address)
print((location.latitude, location.longitude))

#%%

from geopy.distance import geodesic
newport_ri = (location.latitude, location.longitude)
cleveland_oh = (41.499498, -81.695391)
print(geodesic(newport_ri, cleveland_oh).miles)