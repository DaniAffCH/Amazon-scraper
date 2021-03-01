from selenium import webdriver
import re
PATH = "C:\Program Files (x86)\chromedriver.exe"
ricerca = input("Inserisci cosa vuoi comparare su Amazon... ")
ricerca = ricerca.replace(" ", "+")
urlRicerca = "https://www.amazon.it/s?k=" + ricerca
driver = webdriver.Chrome(PATH)
driver.get(urlRicerca)

risultati = driver.find_element_by_css_selector(".a-spacing-top-small > span:nth-child(1)").text
# 2 opzioni di sintassi a seconda che i risultati siano più o meno di 1000
if("più di" in risultati):
    numeroArticoliTotali = re.search('di (.*?) risultati', risultati).group(1)
    numeroArticoliTotali = numeroArticoliTotali.replace(".", "")
    int(numeroArticoliTotali)
else:
    numeroArticoliTotali = re.search('dei (.*?) risultati', risultati).group(1)
    numeroArticoliTotali = numeroArticoliTotali.replace(".", "")
    int(numeroArticoliTotali)

numeroArticoliPerPagina = int(re.search('\-(.*?) dei', risultati).group(1))
print("Secondo Amazon ci sono " + str(numeroArticoliPerPagina) + " prodotti per pagina su un totale di " + str(numeroArticoliTotali) + " prodotti.")

f = open("linkProdotti.txt","w+")
# Estrazione link per pagina
elems = driver.find_elements_by_xpath("//h2[contains(@class, 'a-size-mini a-spacing-none a-color-base s-line-clamp-4')]//a[contains(@class, 'a-link-normal a-text-normal')]")
for k in elems:
    link = k.get_attribute("href")
    f.write(link + "\n")
f.close
driver.close()
