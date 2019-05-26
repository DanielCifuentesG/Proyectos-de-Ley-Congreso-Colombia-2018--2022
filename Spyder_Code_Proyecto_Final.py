# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:31:23 2019

@author: hp4440
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import itertools

from selenium import webdriver
import time

# lista de urls con las páginas a hacer scrap 
proyectos = 'https://congresovisible.uniandes.edu.co/proyectos-de-ley/#q=2019&page='

# lista con las url de las 123 paginas con los proyectos de ley 
proyectos_list = []
for i in [x for x in range(1,126)]:
    proyectos_list.append(proyectos + str(i))


# lista de todas las urls con los proyectos de ley

def sacar_links_pdl(lista):
    browser = webdriver.Chrome(executable_path=r"C:\web_drivers\chromedriver.exe")
    browser.get(lista)
    time.sleep(2)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    time.sleep(0)
    soup = BeautifulSoup(html,'lxml')
    
    elements = soup.find_all('a')
    #str_elements = str(elements)
    pl_prefix = 'https://congresovisible.uniandes.edu.co/proyectos-de-ley/'
    
    pl_sufix = re.findall('/proyectos-de-ley/(p.+?)\">', str(elements))
    
    pl_all_list = [pl_prefix + url for url in pl_sufix]
    
    return pl_all_list

# sacar la lista con todas las url de los proyectos de ley 
    
url_proyectos_ley = list(map(sacar_links_pdl,proyectos_list))

# por alguna razon no salieron los elemntos de la pag #12 

page_11 = sacar_links_pdl('https://congresovisible.uniandes.edu.co/proyectos-de-ley/#q=2019&page=12')
#sacar info pag 12
 
#agregar la lista nueva a la lista general                         
url_proyectos_ley.append(page_11) 

#borrar lista vacía 
del(url_proyectos_ley[11])

################# SACAR Links de lista -> 625 Links) #######
url_625_PdL = list(itertools.chain.from_iterable(url_proyectos_ley))
                   
############ asiganr NA a los [] de las variables 

def Na_taguer(var):
            if var == []:
                var = 'NA'
            else:
                pass
            return var

# SACAR LOS ELEMENTOS DE CADA UNA DE LAS URL CON LOS PdL

def scrap_elementos(url):
       
    try: 
        get_url = requests.get(url).text
        sopa = BeautifulSoup(get_url,'lxml')
        
        r_titulo = sopa.find_all('h1')
        try:
            titulo = re.findall('\">"|“(.+?)\[', str(r_titulo))[-1]
        except:
            titulo = titulo = re.findall('\">“(.+?)\.', str(r_titulo))
        
        try:
            tagtitulo = re.findall('\[([A-Z\d].+?)\]', str(r_titulo))[-1]
                #tagtitulo = re.findall('\[([A-Z\d].+?)\]\”', str(r_titulo))[-1]
        except:
            tagtitulo = 'NA'
        del r_titulo
        
        r_estado = sopa.find('div', class_='module5').find_all('li', text='')
        estado = re.findall('\">(.+?)</a>', str(r_estado))[-1]
        proceso = re.findall('\">(.+?)</a>', str(r_estado))
        fechas_proceso = re.findall('<p>(.+?)</p>', str(r_estado))
        del r_estado
        
        try:
            r_sinopsis = sopa.find('div', class_='module7').find('p', text='')
            sinopsis = re.findall('p>(.+?)</', str(r_sinopsis))
            sinopsis = [w.replace('<br/>', ' ') for w in sinopsis][-1]
            del r_sinopsis
        except:
            sinopsis = 'NA'
        
        r_datos_grls = sopa.find('ul', class_='lista6').find_all('li', text='')
        str_datos_grls = str(r_datos_grls)
        del r_datos_grls
        
        temas = re.findall('Tema</h3><p>(.+?)</p>', str_datos_grls)
        temas = Na_taguer(temas)
        tipo = re.findall('Tipo</h3><p>(.+?)</p>', str_datos_grls)[-1]
        tipo = Na_taguer(tipo)
        
        fecha_radicacion = re.findall('Fecha de Radicación </h3><p>(.+?)</p>', str_datos_grls)[-1]
        
        tags = re.findall('#q=(.+?)\">', str_datos_grls)
        tags = [x.strip(' ') for x in tags]
        tags = Na_taguer(tags)
        
        r_autores = sopa.find('div', class_='module2')
        autores = re.findall('alt=\"([A-ZÁÉÍÓÚ].+?)\" height', str(r_autores))
        autores = Na_taguer(autores)
        del r_autores
        
        r_partido_autores = sopa.find_all('div', class_='module2')
        partido_autores1 = re.findall('\d/\">(.+?)</p>', str(r_partido_autores))
        partido_autores = re.findall('\d/\">(.+?)</a>', str(partido_autores1))
        partido_autores = Na_taguer(partido_autores)
        del r_partido_autores
        del partido_autores1
        
        url_Pdl = url
    
        #return titulo,tagtitulo,estado,autores,partido_autores,proceso,fechas_proceso,sinopsis,temas,tipo,fecha_radicacion,tags,url_Pdl

        return{'Proyecto de Ley':titulo,'Palabra Clave':tagtitulo,'Estado':estado,'Autor':autores,'Partido':partido_autores ,'Proceso':proceso,'Fechas proceso':fechas_proceso,'Resumen':sinopsis,'Tema':temas,'Tipo':tipo,'Fecha Radicación':fecha_radicacion,'Tags':tags,'link':url_Pdl}

    except: 
        
        titulo = 'link dañado'
        tagtitulo = 'link dañado'
        estado = 'link dañado'
        autores = 'link dañado'
        partido_autores = 'link dañado'
        proceso = 'link dañado'
        fechas_proceso = 'link dañado'
        sinopsis = 'link dañado'
        temas = 'link dañado'
        tipo = 'link dañado'
        fecha_radicacion = 'link dañado'
        tags = 'link dañado'
        url_Pdl = url
        
        return{'Proyecto de Ley':titulo,'Palabra Clave':tagtitulo,'Estado':estado,'Autor':autores,'Partido':partido_autores,'Proceso':proceso,'Fechas proceso':fechas_proceso,'Resumen':sinopsis,'Tema':temas,'Tipo':tipo,'Fecha Radicación':fecha_radicacion,'Tags':tags,'link':url}

Macro_Dicc = list(map(scrap_elementos,url_625_PdL))
Macro_DF = pd.DataFrame(Macro_Dicc)

################## SACAR URL  DE REPRESENTANTES ############

def scrap_url_representantes():
    html = requests.get('http://www.camara.gov.co/index.php/representantes').text
    sopa = BeautifulSoup(html, 'lxml')
    r_rep_links = sopa.find_all('span', class_='namereplist')
    rep_prefix = 'http://www.camara.gov.co/index.php/representantes/' 
    rep_sufix = re.findall('href="/representantes/(.+?)" hreflang',str(r_rep_links))
    rep_url = [rep_prefix + x for x in rep_sufix]
    
    return rep_url

rep_urls = scrap_url_representantes()

################### algoritmo para sacar INFO de Rep a la CAMARA ##### 
def rep_info(url):
    try:
        html = requests.get(url).text
        sopa = BeautifulSoup(html, 'lxml')
    
        r_mombre = sopa.find_all('div', class_='field field--name-name field--type-string field--label-hidden field__item')
        nombre = re.findall('field__item">(.+?)</div>', str(r_mombre))[-1]
        
        rep_Info = sopa.find_all('div', class_='col-xs-6 col-sm-6 col-md-6 contatributosrep')
        
        r_rep_partido = sopa.find_all('span', class_='partpolit')
        rep_partido = re.findall('hreflang=\"es\">(.+?)</a>', str(r_rep_partido))[-1]
        
        rep_circuns = re.findall('field--label-hidden field__item\">(.+?)</div>', str(rep_Info))[-1]
        
        try:
            r_rep_votos = sopa.find_all('div', class_='field field--name-field-votos-obtenidos field--type-string field--label-visually_hidden')
            rep_votos = re.findall('field__item\">(.+?)</div>', str(r_rep_votos))[-1]
        except:
            rep_votos= 'NA'
        return{'congresista':nombre,'Partido':rep_partido,'circunscripción':rep_circuns,'votos':rep_votos}
    
    except:
        nombre = 'link dañado'
        rep_partido = 'link dañado'
        rep_circuns = 'link dañado'
        rep_votos = 'link dañado'
        
        return{'congresista':nombre,'Partido':rep_partido,'circunscripción':rep_circuns,'votos':rep_votos}

rep_Dicc = list(map(rep_info,rep_urls))

rep_DF = pd.DataFrame(rep_Dicc)
representantes_DF = pd.DataFrame(rep_DF[['congresista','Partido','Camara']])

####################  URL SENADORES ############ 
    
def scrap_url_senadores():
    html = requests.get('http://www.senado.gov.co/el-senado/senadores').text
    sopa = BeautifulSoup(html, 'lxml')
    
    senadores_prefix = 'http://www.senado.gov.co/el-senado/senadores/213-directorio/'
    senadores_sufix = re.findall('directorio/(.+?)\">', str(sopa.find_all('tbody')))
    url_senadores = [senadores_prefix + x for x in senadores_sufix]
    
    return url_senadores

senador_url = scrap_url_senadores() 

##################  SENADORES  BASE DE DATOS #########

def senador_info(url):
    try:
        html = requests.get(url).text
        sopa = BeautifulSoup(html, 'lxml')
    
        nombre_senador = re.findall('\t([A-ZÁÉÍÓU].+?)\t',str(sopa.find_all('p', id='contact-name')))[-1]
        departamento_senador = re.findall('\t([A-ZÁÉÍÓU].+?)\t',str(sopa.find_all('p', id='contact-position')))[-1]
        partido_senador = re.findall('>(.+?)</p>',str(sopa.find_all('p', id='contact-country')))[-1]
        
        return{'senador':nombre_senador,'Departamento':departamento_senador,'Partido':partido_senador}
    except:
        nombre_senador = 'link dañado'
        departamento_senador = 'link dañado'
        partido_senador = 'link dañado'
        return{'senador':nombre_senador,'Departamento':departamento_senador,'Partido':partido_senador}

senador_Dicc = list(map(senador_info,senador_url))
senador_DF = pd.DataFrame(senador_Dicc)
senador_DF.rename(columns={'senador':'congresista'}, inplace=True)
senado_DF = pd.DataFrame(senador_DF[['congresista','Partido','Camara']])

################# Agregar ID a la Base de datos #######
Macro_DF['ID'] = [x + 1 for x in range(625)]
frame_1['ID'] = [x + 1 for x in range(625)]

rep_DF['Camara'] = 'Camara'   # se agrega la cámara a la que pertenece 
senador_DF['Camara']= 'Senado' # se agrega la cámara a que pertenece 


# 1) BASE DE DATOS UNIVARIABLES 


##############   BASE DE DATOS # 1  (datos de un solo valor) ####### 

frame_1 = pd.DataFrame(Macro_DF[['Proyecto de Ley','Palabra Clave','Estado','Fecha Radicación','Resumen','Tipo','link']]).copy()

##############      BASDE DE DATOS # 2 (ID, Autor, Partido, Camara) ############ 

frame_2 = dict(zip(Macro_DF['ID'],Macro_DF['Autor']))
keys = [k for k in frame_2.keys() for v in frame_2[k]]
values = [v for k in frame_2.keys() for v in frame_2[k]]
frame_2 = pd.DataFrame.from_dict({'index': keys, 'values': values})
frame_2.rename(columns={'index':'ID','values':'congresista'}, inplace=True) # arreglar el nombre de las columnas 
frame_2['CC'] = '' # para poner un ID a cada congresista (manual)

########## este codigo genera la BASE definitiva (con ajustes y completa) [CHECK]
test_frame = congresistas_DF[congresistas_DF['CC'] != '']
test_frame2 = frame_2[frame_2['CC'] != '']
test_frame_3 = pd.merge(test_frame, test_frame2, on='CC', how='right')

########### para poner un ID a cada congresista (manual)
#         # esto con el fin de que se puedan articular todas las bases de datos 

congresistas_DF[congresistas_DF['congresista'].str.contains(r'Puentes')]
frame_2[frame_2['congresista'].str.contains(r'Puentes')]
frame_2.loc[frame_2['congresista'] == 'Gustavo Hernán  Puentes Díaz', 'CC'] = 1090
#asigna un valor de ID (manual) a cada observación 
# (tuve que hacerlo manualmente y asiganr un valor unico a cada congresista)

############### BASE DE DATOS # 3 (ID - TEMAS) ########

frame_3 = dict(zip(Macro_DF['ID'],Macro_DF['Tema']))
keys = [k for k in frame_3.keys() for v in frame_3[k]]
values = [v for k in frame_3.keys() for v in frame_3[k]]
frame_3 = pd.DataFrame.from_dict({'index': keys, 'values': values})
frame_3.rename(columns={'index':'ID','values':'Tema'}, inplace=True)
 
################  BASE DE DATOS # 4 (ID - TAGS) ########

frame_4 = dict(zip(Macro_DF['ID'],Macro_DF['Tags']))
keys = [k for k in frame_4.keys() for v in frame_4[k]]
values = [v for k in frame_4.keys() for v in frame_4[k]]
frame_4 = pd.DataFrame.from_dict({'index': keys, 'values': values})
frame_4.rename(columns={'index':'ID','values':'Tags'}, inplace=True)

##### Exportar a csv las bases de datos

frame_1.to_csv(r'C:\Users\hp4440\OneDrive - Universidad del rosario\Maestria\IV Semestre\MCPP\Mi repositorio\para trabajo final\csv_files\Datos_unicos.csv')
frame_2.to_csv(r'C:\Users\hp4440\OneDrive - Universidad del rosario\Maestria\IV Semestre\MCPP\Mi repositorio\para trabajo final\csv_files\Frame_2.csv')

####################################################


##  DATOS PARA RESPONDER PREGUNTAS ### 

# 1)  cuales partidos están en más PdL 

frame_4_fltro = frame_4[frame_4['Tags'] != 'N']
frame_4_fltro = frame_4_fltro[frame_4_fltro['Tags'] != 'A']
















