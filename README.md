Backend Knygų API
Ši programa yra autorizuota knygų valdymo sistema, sukurta naudojant FastAPI karkasą ir MySQL duomenų bazę duomenų valdymui.


Ką daro programa
Programa leidžia registruoti vartotojus ir saugiai prie jos prisijungti naudojant JWT žetonus. Registracijos metu galima pasirinkti paprasto 
vartotojo arba administratoriaus rolę. Visi prisijungę naudotojai gali peržiūrėti bendrą visų įrašytų knygų sąrašą, filtruoti jį pagal kategorijų 
pavadinimus bei rūšiuoti pagal reitingą. Taip pat yra atskiras maršrutas, kuriame naudotojas mato tik savo asmeniškai pridėtas knygas. Naujų knygų 
kūrimas automatiškai susiejamas su prisijungusio vartotojo ID. Trinti arba keisti įrašus leidžiama tik tam asmeniui, kuris tą knygą įrašė, arba sistemos 
administratoriui. Tik administratoriai gali kurti naujas knygų kategorijas atskiroje lentelėje.



Reikalavimai ir priklausomybės
Sistemos paleidimui reikalingas Python 3.9 arba naujesnė versija. Visi priklausomi paketai yra surašyti requirements.txt faile. Pagrindinės 
naudojamos bibliotekos apima fastapi ir uvicorn serverio veikimui bei maršrutams, sqlalchemy ir pymysql susijungimui su MySQL duomenų baze, 
pydantic duomenų validacijai, python-jose ir passlib slaptažodžių maišymui bei žetonų generavimui, pytest vienetinių testų vykdymui bei 
python-dotenv aplinkos kintamųjų valdymui.



Projekto paruošimas ir paleidimas lokaliai
Prieš paleidžiant programą, pagrindiniame projekto aplanke būtina sukurti konfigūracinį .env failą ir nurodyti šiuos duomenis:

MYSQL_ROOT_PASSWORD=slaptazodis
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=knygu_db
JWT_SECRET_KEY=slaptas_raktas_123
JWT_ALGORITHM=HS256


Virtualios aplinkos paruošimas:
Atsidarykite terminalą pagrindiniame projekto aplanke. Prieš pradedant kurti virtualią aplinką, pirmiausia būtina pereiti į backend 
direktoriją paleidžiant komandą cd backend. Tuomet įvykdykite komandas pagal savo naudojamą operacinę sistemą ir programą.

Naudojant Windows Command Prompt (cmd):
      python -m venv venv
      call venv\Scripts\activate
pip install -r requirements.txt

Naudojant Windows PowerShell:
      python -m venv venv
      .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Naudojant macOS arba Linux:
      python3 -m venv venv
      source venv/bin/activate
pip install -r requirements.txt



Paleisti docker compose up -d


Serverio paleidimas
Kai virtuali aplinka aktyvuota, esate backend (cd backend) serveris paleidžiamas komanda:
      uvicorn app.main:app --reload

Programa bus pasiekiama adresu http://127.0.0.1:8000, o interaktyvi dokumentacija – http://127.0.0.1:8000/docs.



REST API Galiniai taškai (Endpoints)
Visiems knygų ir kategorijų maršrutams reikalinga autorizacija, o užklausos antraštėje turi būti siunčiamas Authorization: Bearer <token> žetonas. 
Viešai prieinami taškai yra tik du: POST /auth/register, skirtas naujo vartotojo registracijai nurodant USER arba ADMIN rolę, 
ir POST /auth/token, skirtas prisijungimui bei žetono gavimui.


Knygų valdymui skirtas GET /books/ maršrutas, kuris leidžia gauti visas knygas bei jas filtruoti su ?category=Pavadinimas arba rūšiuoti su ?sort=asc arba ?sort=desc, 
tačiau filtruoti pagal konkretaus naudotojo ID naudojant ?user_id=ID čia gali tik ADMIN. Maršrutas GET /books/my grąžina tik prisijungusio vartotojo asmenines knygas. 
Nauja knyga pridedama per POST /books/ užklausą, kurioje privaloma nurodyti egzistuojančios kategorijos ID skaičių per category_id. Knygos atnaujinimas vykdomas per 
PUT /books/{id}, o ištrynimas per DELETE /books/{id} maršrutus, kurie prieinami tik knygos autoriui arba ADMIN. Naujos unikalios kategorijos sukūrimas atliekamas per 
POST /books/categories maršrutą, kurį pasiekti gali išskirtinai tik administratoriai.



Testų paleidimo komandos:
Įsitikinkite, kad jūsų virtuali aplinka yra aktyvuota, esate terminale backend (cd backend) ir vykdykite vieną iš šių komandų:

      Paleisti visus projekte esančius testus:
      python -m pytest

      Paleisti testus su detalesne informacija (parodys, kurie konkretūs metodai praėjo):
      python -m pytest -v


*Jei norite gauti administratoriaus teises testavimo metu, registracijos metu nurodykite "role": "ADMIN" arba rankiniu būdu pakeiskite reikšmę duomenų bazės lentelėje 
users stulpelyje role į ADMIN. Pastaba: pakeitus rolę tiesiogiai duomenų bazėje, būtina per Swagger iš naujo atlikti prisijungimą per POST /auth/token maršrutą, 
kad būtų sugeneruotas naujas JWT žetonas su atnaujintomis teisėmis.





