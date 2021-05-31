import copy
from urllib import parse
import requests
import sys

def usage():
        print("Example: ")
        print("python3 sqliscan.py <target_url> \"<cookie>\" \"<user-agent>\" ")
        print("\n")
        print("<target_url> = http://alvo?parametro_para_teste=1")
        print("<cookie> = \"PHPSESSID=98elkn24bcjrdgn7due0up7pb4\" ")
        print("<user-agent> = \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36\" ")
        print("\n")
        sys.exit(1)

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

# Recebe a URL via linha de comando;
if sys.argv[1] == "--help":
        usage()
else: 
        url = sys.argv[1]

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