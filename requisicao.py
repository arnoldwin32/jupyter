#Importacoes
import requests
from  datetime import datetime
import pandas as p
import csv

#Funcao para, dado um data, retornar a data do dia anterior, considerando mes e ano (bissexto)
def diaAnterior(data):
    meses = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    ano = data.year
    mes = data.month
    dia = data.day
    if dia == 1:
        if mes == 1:
            ano-=1
            return datetime(ano,12,31)
        else:
            mes-=1
            #ano bissexto
            if ano % 4 == 0 and mes == 2:
                return datetime(ano,mes,meses[mes]+1)
            else:
                return datetime(ano,mes,meses[mes])
    else:
        return datetime(ano,mes,dia-1)
#Variaveis
hops = 10
data = datetime.now()
dia = int(data.strftime("%d"))
mes = int(data.strftime("%m"))
ano = int(data.strftime("%Y"))
url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{:02d}-{:02d}-{:04d}.csv"
r = requests.get(url.format(mes,dia,ano))

#Verifica que se conseguiu fazer a requisicao, caso não, faz mais 9 tentativas
while r.status_code != 200 and hops > 0:
    novaData = diaAnterior(datetime(ano,mes,dia))
    dia = int(novaData.strftime("%d"))
    mes = int(novaData.strftime("%m"))
    ano = int(novaData.strftime("%Y"))
    hops -=1
    r = requests.get(url.format(mes,dia,ano))
    print("{:02d}{:02d}{:04d}".format(dia,mes,ano))

#Se em alguma tentativa, a requisicao deu certo, ele salva o conteúdo num arquivo csv
if r.status_code == 200:
    dados = p.read_csv(url.format(mes,dia,ano))
    dados.to_csv("jhu.csv")