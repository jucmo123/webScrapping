#Importando Libs
#Para instalar uma biblioteca: pip install 'nome da biblioteca'
from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
import requests
from random import randint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

paginas = np.arange(1, 5, 50)
headers = {'Accept-Language': 'pt-BR,pt;q=0.8'}

titulos = []
anos = []
generos = []
tempo_duracao = []
votos = []
ratings = []
imdb_ratings = []
imdb_ratings_standardized = []

for pagina in paginas:

    response = get("https://www.imdb.com/search/title/?genres=sci-fi&"
                   + "start=" + str(pagina) + "&explore=title_type,genres&ref_=adv_prv", headers=headers)
    
    sleep(randint(8,16)) # tempo para enganar algoritmo e aguardar eventual atraso na resposta
    if response.status_code != 200:
        warn(f'O pedido: {requests} retornou o código: {response.status_code}')

    # Pegando informações das páginas
    pagina_html = BeautifulSoup(response.text, 'html.parser')

# print(pagina_html)

    # Pegando informações por containers
    movie_containers = pagina_html.find_all('div', class_ = 'lister-item mode-advanced')

    for container in movie_containers:

        # capturando títulos
        if container.find('div', class_ = 'ratings-metascore')is not None:
            title = container.h3.a.text
            titulos.append(title)

        #capturada a informação do título, acima, agora capturar as demais de cada filme:

            #Capturando anos
            if container.h3.find('span', class_ = 'lister-item-year text-muted unbold') is not None:
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text # '.text' para trazer o conteúdo
                anos.append(year)
            else:
                anos.append(None)

            #Capturando avaliação (container.p avaliacao)
            if container.p.find('span', class_ = 'certificate') is not None:
                avaliacao = container.p.find('span', class_ = 'certificate').text # '.text' para trazer o conteúdo
                ratings.append(avaliacao)
            else:
                ratings.append(None)

            #Capturando Gênero -> 
            if container.p.find('span', class_ = 'genre') is not None:
                genero = container.p.find('span', class_ = 'genre').text.replace('\n', '').strip().split(',') # '.text' para trazer o conteúdo
                generos.append(genero)
            else:
                generos.append(None)
            # Toda vez que encontrar uma vírgula, entende que a palavra acabou
            # ação, 

            # Capturando duração dos filmes
            #nome da classe é 'runtime'
            #Capturando Gênero -> 
            if container.p.find('span', class_ = 'runtime') is not None:
                tempo = container.p.find('span', class_ = 'runtime').text.replace('min', '') # .text(trazer o conteúdo).replace('tira algo', 'coloca algo')
                #int acima para eventual análise dos valores númericos
                tempo_duracao.append(tempo)
            else:
                tempo_duracao.append(None)

            #Capturando votos IMDB -> 
            if container.strong.text is not None:
                imdb = float(container.strong.text.replace(',', '.')) # .text(trazer o conteúdo).replace('tira algo', 'coloca algo')
                imdb_ratings.append(imdb)
            else:
                imdb_ratings.append(None)

            #Capturando votos
            if container.find('span', attrs = {'name':'nv'})['data-value'] is not None:
                voto = int(container.find('span', attrs = {'name':'nv'})['data-value'])
                votos.append(voto)
            else:
                votos.append(None)

dt_inicial = pd.DataFrame({
    'ano': anos,
    'genero': generos,
    'tempo': tempo_duracao,
    'imdb': imdb_ratings,
    'votos': votos
    })

# -7 -6 -5 -4 -3 -2 -1 (.str[-5:-1])
#  c  l  a  r  i  f  y
#  1  2  3  4  5  6  7
dt_inicial.loc[:, 'ano'] = dt_inicial['ano'].str[-5:-1] # 20-03-2023 -> str[do -5: a -1'que é o último elemento da lista]
dt_inicial['imdb_conv'] = dt_inicial['imdb'] * 10 # cria coluna imdb_conv e recebe dt_inicial

                    # localizar
dt_final = dt_inicial.loc[dt_inicial['ano'] != 'Movie']

print(dt_final)








    # import scrapy

# class ImdbSpider(scrapy.Spider):
#     name = 'imdb'
#     start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

#     def parse(self, response): # 39min
#         for filmes in response.css('.titleColumn'):
#             yield{
#                 'titulo': filmes.css('.titleColumn a::text').get(),
#                 'ano': filmes.css('.secondaryInfo ::text').get()[1:-1],
#                 'nota': response.css('strong::text').get()
#             }

