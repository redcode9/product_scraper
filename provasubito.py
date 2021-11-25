from bs4 import BeautifulSoup
from datetime import datetime
from progress.bar import Bar
import requests

contatoreScaricate = 0

#input prodotto da cercare
search = input("Product: \n")
search = search.lower()
#trasformazione per inserire il prodotto nell'url
searchUrl = search.replace(' ','+')
nomefile = search+".csv"

#concateno la stringa inserita all'url di subito
url = "https://www.subito.it/annunci-italia/vendita/usato/?q="+searchUrl
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
outAlternative = soup.find_all(class_='index-module_sbt-button__2K3Qy index-module_text__3TLHK index-module_medium__2LeWP jsx-2950730121 pagination__btn')
#print(outAlternative)


for lineX in outAlternative:
    #print("\nSei dentro al for per ottenere il numero di pagine")
    #Ottenimento numero pagine rispettivo all'oggetto cercato
    maxPagine = str(outAlternative)
    #print(maxPagine)
    maxPagine = lineX.find_all(class_='index-module_button-text__1ZqCr')
    maxPagine = str(maxPagine)[162:len(maxPagine)-9]


print("\nRequest previste(il valore può variare leggermente): ")
n_req = (int(maxPagine)*33)/2
print(n_req)
input("\nPremi per continuare..")
entry = {}   
cont = 0

bar = Bar('Processing',max = n_req)
for i in range(1, int(maxPagine)):
#for i in range(1, 10):
   
    #Gestione multipagina
    numPage = "&o="+str(i)

    #concateno la stringa inserita all'url di subito
    url = "https://www.subito.it/annunci-italia/vendita/usato/?q="+searchUrl+numPage
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    #ottenimento card oggetti all'interno della pagina
    out = soup.find_all(class_='SmallCard-module_link__9Ey4a link')

    #print("\nPAGINA ",i)
    #print(out)
    #print("\n\n\n\n")
    #print(out)
    #input ("Premi per terminare..")

    #names = soup.find_all(class_='classes_sbt-text-atom__2GBat classes_token-h6__1ZJNe size-normal classes_weight-semibold__1RkLc jsx-3045029806 item-title jsx-3924372161')

    for line in out:

        #name section, TODO CHECK RANGE
        name_tag = line.find_all(class_='SmallCard-module_item-title__3e8Rq')
        s = BeautifulSoup(str(name_tag),'html.parser')
        temp = s.find('h2')
        name = temp.text
        name = name.lower()

        #Vecchio modo per individuare il nome attraverso lo slicing del testo e troncamento agli estremi
        #name = str(name_tag)[194:len(name_tag)-7]
        #print("\nNome tagliato classico:",name)

        if( search in name):

            #print("NOME")
            #print(name)
            now = datetime.now()
            entry["data"] = now.strftime("%Y-%m-%d")
            entry["name"] = name

            #price section
            #print("\n\n\nRIGA: ")
            price_tag = list(line.find_all(class_='index-module_price__2WXSC'))
            if len(price_tag) > 0:
                s = BeautifulSoup(str(price_tag),'html.parser')
                temp = s.find('p')
                price = temp.text
                price = price.lower()
                price = str(price)[0:len(price)-2]
                entry["price"] = price

            else:
                entry["price"] = None


            #Vecchio modo per individuare il prezzo
            '''
            if len(price_tag) > 0:
                price_tag = price_tag[0]
                print("\nPRICE TAG:")
                print(price_tag)
                price = str(price_tag)[99:len(price_tag)-7]
                #print("\nPREZZO:")
                print("\nPrezzo: ",price)
                #print("\nLunghezza: ",len(price))

                #controllo se ci sono dei caratteri all'interno dil campo price
                x = price.isnumeric()
                #print("\nIl prezzo è numerico, Si = 1, No = 0:",x)

                #se ci sono dei caratteri pulisco la stringa
                if(x == 0):
                    #print("\nSono dentro IF in quanto il prezzo non è solo numerico")
                    price = str(price)[0:len(price)-364]
                    #print("\nPrezzo dopo trasformazione:",price)
                entry["price"] = price
            else:
                entry["price"] = None
            '''

            #location section
            location_tag = list(line.find_all(class_='index-module_town__2GUfh'))
            s = BeautifulSoup(str(location_tag),'html.parser')
            temp = s.find('span')
            location = temp.text

            #Vecchio modo per estrapolare la citta
            #location = str(location_tag)[175:len(location_tag)-10]
            entry["location"] = location

            #link section (root cannot be parsed)
            temp = []
            for i in str(line)[1:]:
                if i != "<":
                    temp.append(i)
                else:
                    break
            insertion_url = ''.join(temp[50:len(temp)-2])
            entry["insertion_url"] = insertion_url

            #Creazione e popolamento file
            #print("Nome:",name," Prezzo:",price," Location:",location," Link:",insertion_url)
            with open(nomefile, 'a') as f:
            #Formattazione del file in NOME,PREZZO,LOCATION,LINK
                    contatoreScaricate = contatoreScaricate + 1
                    for key, value in entry.items(): 
                        f.write(f"{value},")
                        cont = cont +1
                        if cont == 5:
                            f.write(f".\n")
                            cont = 0
            
            f.close()
            bar.next()

        #print(len(out))

bar.finish()
print("Hai inserito ",contatoreScaricate," prodotti")
input ("\nPremi per terminare..")


