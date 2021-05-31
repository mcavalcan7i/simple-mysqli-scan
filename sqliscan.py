import copy
from urllib import parse
import requests
import sys

# Função para fazer a requisição
def requests_for(url):
        headers = {
                "Cookie": cookie,
                "User-Agent":  useragent
        }

        try:
               response =  requests.get(url, headers=headers)
               html = response.text
               return html
        except:
                pass

# Função para verificar se existe o erro de código sql no html retornado
def is_vulnerable(html):
        if "You have an error in your SQL syntax" in html:
                return True

# Recebe a URL via linha de comando
url = sys.argv[1];
cookie = sys.argv[2]
useragent = sys.argv[3]

# faz o parse da url e adiciona o valor a variavel url_parsed
url_parsed = parse.urlsplit(url)

# Recebe os parametros que estão associados ao param da url e adiciona a variavel params
params = parse.parse_qs(url_parsed.query);

# Percorre as chaves que estão contidas na variavel params
for param in params.keys():
        query = copy.deepcopy(params)

        # Para cada caractere dentro da string " ou '
        for c in "'\'":
                # Para cada chave dentro de param, modifique seu valor para o valor da sting c
                query[param][0] = c
                #Transforma o objeto em url
                new_params = parse.urlencode(query, doseq=True)

                url_final = url_parsed._replace(query=new_params)
                url_final = url_final.geturl()
                html = requests_for(url_final)
                if html:
                        if is_vulnerable(html):
                                print("VULNERABLE PARAMETER: {}".format(param))
                                quit()

print("NOT VULNERABLE")