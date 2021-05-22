import dns.resolver
import sys

resolver = dns.resolver.Resolver()
alvo = sys.argv[1]
wordlist = sys.argv[2]

file = open(wordlist, 'r')

for subdomain in file:
    subdomain = subdomain.replace("\n", "")
    alvo_final = "{}.{}".format(subdomain, alvo)
    
    try:
        resultados = resolver.resolve(alvo_final, "A")
        for resultado in resultados:
            print("{} -> {}".format(alvo_final, resultado))
    except:
        pass
