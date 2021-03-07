from selectorlib import Extractor
import requests

class LinkGetter:
    __private_srcQuery = str()
    r = None
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.it/',
        'accept-language': 'it-IT;q=0.9,it;q=0.8',
    }
    def __init__(self, query):
        self.__private_srcQuery = query.replace(" ", "+")

    def sendRequest(self, proxy = None):
        link = "https://www.amazon.it/s?k="+self.__private_srcQuery+"&__mk_it_IT=ÅMÅŽÕÑ&ref=nb_sb_noss"
        print(link)
        tmp = requests.get(link, headers=self.headers)
        if tmp.status_code > 400:
            raise Exception("ERRORE! CODICE %s"%tmp.status_code)
        elif "To discuss automated access to Amazon data please contact" in tmp.text:
            raise Exception("AMAZON TI HA BLOCCATO")
        else:
            self.r = tmp
    def link2file(self, fileName):
        yaml_search = """
            section:
                css: null
                xpath: '//h2[contains(@class, 'a-size-mini a-spacing-none a-color-base s-line-clamp-4')]//a[contains(@class, 'a-link-normal a-text-normal')]'
                type: Attribute
                attribute: href
        """
        extractor = Extractor.from_yaml_string(yaml_search)
        res = extractor.extract(self.r.text)
        print(res)
        #with open(fileName, "w+") as f:

g = LinkGetter("olio")
g.sendRequest();
g.link2file("prodottiInfo.txt");

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# ricerca = input("Inserisci cosa vuoi comparare su Amazon... ")
# ricerca = ricerca.replace(" ", "+")
# urlRicerca = "https://www.amazon.it/s?k=" + ricerca
# driver = webdriver.Chrome(PATH)
# driver.get(urlRicerca)
#
# risultati = driver.find_element_by_css_selector(".a-spacing-top-small > span:nth-child(1)").text
# # 2 opzioni di sintassi a seconda che i risultati siano più o meno di 1000
# if("più di" in risultati):
#     numeroArticoliTotali = re.search('di (.*?) risultati', risultati).group(1)
#     numeroArticoliTotali = numeroArticoliTotali.replace(".", "")
#     int(numeroArticoliTotali)
# else:
#     numeroArticoliTotali = re.search('dei (.*?) risultati', risultati).group(1)
#     numeroArticoliTotali = numeroArticoliTotali.replace(".", "")
#     int(numeroArticoliTotali)
#
# numeroArticoliPerPagina = int(re.search('\-(.*?) dei', risultati).group(1))
# print("Secondo Amazon ci sono " + str(numeroArticoliPerPagina) + " prodotti per pagina su un totale di " + str(numeroArticoliTotali) + " prodotti.")
#
# f = open("linkProdotti.txt","w+")
# # Estrazione link per pagina
# elems = driver.find_elements_by_xpath("//h2[contains(@class, 'a-size-mini a-spacing-none a-color-base s-line-clamp-4')]//a[contains(@class, 'a-link-normal a-text-normal')]")
# for k in elems:
#     link = k.get_attribute("href")
#     f.write(link + "\n")
# f.close
# driver.close()
