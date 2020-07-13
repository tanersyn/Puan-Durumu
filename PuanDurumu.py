# Gerekli kütüphaneleri dahil ediyoruz
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sqlite3

# Veri çekmek için url değişkeninin içine siteyi ekliyoruz
url = "https://www.goal.com/tr/s%C3%BCper-lig/puan-durumu/482ofyysbdbeoxauk19yg7tdt"

# Siteye get isteğinde bulunuyoruz
response = requests.get(url)

# Site icerigini cekiyoruz
html_icerigi = response.content

# Gelen html icerigini parcalıyoruz
soup = BeautifulSoup(html_icerigi,"hmtl.parser")

# Tüm tbody etiketlerini cekiyoruz
test = str()
tbody = soup.find_all("tbody")

# tbody etiketlerinin icindeki text ifadeleri alıyoruz
for i in tbody:
    test += i.text

# Gelen verilerde bosluk olmasını istemedigimiz icin replace() fonksiyonuyla istedigimiz ifade ile yer degistiriyoruz.
test = test.replace("    "," ")
test = test.replace("   "," ")
test = test.replace("  "," ")

# Liste2 tüm verileri tutan liste
liste2 = list()
liste2 = test.split(" ")

# String ifadelere ayırdıgımız icin 'Yeni' ve 'Malatya' farklı ifadeler almakta bu yüzden birlestiriyoruz
liste2[62] = liste2[62] +" "+ liste2[63]
liste2.remove("Malatya")

# Listenin içindeki sıralamaları alıp s listesine ekliyoruz
s=[]
for siralama in range(1,len(liste2)-1,5):
    s.append(liste2[siralama])

# Listenin içindeki takımları alıp t listesine ekliyoruz
t=[]
for takimlar in range(2,len(liste2)-1,5):
    t.append(liste2[takimlar])

# Listenin içindeki oynanan macları alıp omm listesine ekliyoruz
omm=[]
for om in range(3,len(liste2)-1,5):
    omm.append(liste2[om])

# Listenin içindeki averajları alıp a listesine ekliyoruz
a=[]
for averaj in range(4,len(liste2)-1,5):
    a.append(liste2[averaj])

# Listenin içindeki puanları alıp p listesine ekliyoruz
p=[]
for puan in range(5,len(liste2)-1,5):
    p.append(liste2[puan])

# Pandas dataframe biçiminde göstermek için df degiskenine atayıp df yazdırıyoruz
df = pd.DataFrame({"Sıralama":s,"Takım":t,"Oynan Maçlar":omm,"Averaj":a,"Puan":p})
print(df)

# Degiskenleri tutan listlerin indekslerini zip() fonksiyonu ile esitliyoruz.
toplu = list(zip(s,t,omm,a,p))
print(toplu)

# Veri tabanı ile baglantı kuruyoruz
conn = sqlite3.connect('C:/Users/taner/Desktop/Test/Employee.db')

# Veri tabanına islem yapmak için bir işleç oluşturuyoruz
c = conn.cursor()

# Veri tabanımızdaki tabloyu olusturmak icin sql sorgularımızı yazıyoruz
c.execute('''CREATE TABLE IF NOT EXISTS Employeer
             (Siralama text, Takim text, OM text, Averaj text, Puan text)''')

# toplu degiskenimizin icindeki her indeksi veri tabanımıza ekliyoruz
for i in toplu:
    c.execute("""INSERT INTO Employeer VALUES (?,?,?,?,?)""",i)

# Baglantımızı isliyoruz
conn.commit()

# Baglantımızı kapatıyoruz.
conn.close()