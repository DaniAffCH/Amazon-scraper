from selectorlib import Extractor
import requests
import json
import re
from time import sleep

class Scraper:
    __private_url = str()
    r = None
    ext = None
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'it-IT;q=0.9,it;q=0.8',
    }

    def __init__(self, u, selector):
        if u == None or u == "" or selector == None or selector == "":
            raise Exception("I parametri devono essere inizializzati")
        self.__private_url = u
        self.ext = Extractor.from_yaml_file(selector)

    def setUrl(self, u):
        self.__private_url = u

    def sendRequest(self):
        print("INVIO RICHIESTA")
        tmp = requests.get(self.__private_url, headers=self.headers)
        if tmp.status_code > 400:
            raise Exception("ERRORE! CODICE %s"%tmp.status_code)
        elif "To discuss automated access to Amazon data please contact" in tmp.text:
            raise Exception("AMAZON TI HA BLOCCATO\nURL CORRENTE %s"%self.__private_url)
        else:
            print("DOWNLOAD PAGINA COMPLETATO")
            self.r = tmp

    def __normalize(self, arr):
        arr["price"] = arr["price"].replace(u'\xa0', u'')
        pattern = r"n\. (\d+,*\d*) in (Alimentari e cura della casa|Oli d'oliva)"
        arr["ranking"] = re.findall(pattern,arr["ranking"])

        for n, element in enumerate(arr["ranking"]):
            tmp = list(arr["ranking"][n])
            tmp[0] = int(element[0].replace(',', ''))
            arr["ranking"][n] = tuple(tmp)

        pattern = r"\d+"
        arr["reviews"] = int(re.search(pattern,arr["reviews"]).group())
        return arr

    def extraction(self):
        if(self.r!=None):
            out = self.ext.extract(self.r.text)
            out["AmazonSpedition"] = "spedito da Amazon" in self.r.text
            return self.__normalize(out)

url = "https://www.amazon.it/litri-100-Italiano-Extravergine-Oliva/dp/B07B8SQ7P9/ref=sr_1_13?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3KP0OKGEUEBGI&dchild=1&keywords=olio+evo+italiano&qid=1614272750&rnid=490209031&sprefix=olio+evo%2Caps%2C416&sr=8-13"
sel = "selettore.yml"
sc = Scraper(url, sel)
sc.sendRequest()

print(sc.extraction())
# product_data = []
# with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
#     for url in urllist.read().splitlines():
#         data = scrape(url)
#         if data:
#             for product in data['products']:
#                 product['search_url'] = url
#                 print("Saving Product: %s"%product['title'])
#                 json.dump(product,outfile)
#                 outfile.write("\n")
                # sleep(5)
