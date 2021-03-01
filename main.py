from time import sleep
from lib.scraper import Scraper

def readFromFile(sc: Scraper, pathIn, pathOut = "info.txt"):
    with open(pathIn, 'r') as urlList:
        for url in urlList:
            sc.setUrl(url)
            sc.sendRequest()
            res = sc.extraction()
            print(res)
            with open(pathOut, 'a') as outputFile:
                for element in res:
                    if type(res[element]).__name__ == 'list':
                        outputFile.write(element+": ")
                        for cat in res[element]:
                            outputFile.write("posizione "+str(cat[0])+" nella categoria "+cat[1]+"\n")
                    else:
                        outputFile.write(element+": "+str(res[element])+"\n")
                outputFile.write("\n\n")


if __name__ == "__main__":
    sel = "selettore.yml"
    sc = Scraper(sel)
    readFromFile(sc, "list.txt")
