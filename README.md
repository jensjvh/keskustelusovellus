# Sisällysluettelo
- [Keskustelusovellus (Tsoha-projekti)](#keskustelusovellus-tsoha-projekti)
- [Tekninen kuvaus](#tekninen-kuvaus)
- [Käynnistysohjeet](#käynnistysohjeet)
- [Sovelluksen ominaisuuksia](#sovelluksen-ominaisuuksia)
- [Käyttöohjeet](#käyttöohjeet)

# Keskustelusovellus (Tsoha-projekti)

Sovellus on toteutus keskustelufoorumista, jolla on keskustelualueita eri aiheille. Alueilla on keskusteluketjuja, joille näkyy tilastoja, kuten aloittaja, tietoja viimeisimmästä viestistä ja lukijoiden ja vastausten määrä. Sovelluksen tarkoituksena on ottaa inspiraatiota vanhan koulukunnan keskustelupalstoista, ja luoda sovellus jolla on moderni ulkoasu ja toiminnallisuus.

## Tekninen kuvaus

Sovellus käyttää seuraavia teknologioita:
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Werkzeug

## Käynnistysohjeet:

1. Kloonaa repositorio koneellesi, ja luo juurikansioon tiedosto `.env`. Lisää tiedostoon seuraavat rivit:
```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
2. Luo virtuaaliympäristö komennolla `python3 -m venv venv`. Aktivoi ympäristö komennolla `source venv/bin/activate` ja asenna riippuvudet komennolla `pip3 install -r ./requirements.txt`.
3. Määritä tietokannan skeema komennolla `psql < schema.sql`.
4. Jos haluat lisätä tietokantaan kokeilua varten valmista dataa, suorita komento `python3 initialize_db.py`.
5. Käynnistä sovellus komennolla `flask run`.

## Sovelluksen ominaisuuksia:

 - [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 - [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
 - [x] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
 - [x] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
 - [x] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Viestejä ja ketjuja voi poistaa vain ylläpitäjä.
 - [x] Käyttäjä voi tykätä viesteistä, ja nähdä profiilisivullaan omat ketjunsa, viestinsä ja tykätyt viestit.
 - [x] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana. Vain ylläpitäjät voivat etsiä salaisilta alueilta viestejä.
 - [x] Ylläpitäjä voi lisätä ja poistaa keskustelualueita, sekä muokata niitä.
 - [x] Ylläpitäjä voi luoda salaisen alueen, jonka näkevät vain ylläpitäjät.

## Käyttöohjeet

### Rekisteröityminen
1. Rekisteröidy painamalla etusivulla "Register" -nappia.
2. Noudata laatikon ohjeita tunnusten vaatimuksille ja klikkaa vielä "Register" -nappia laatikossa.
3. Rekisteröitymisen yhteydessä käyttäjä kirjataan sisään.

### Kirjautuminen
1. Kirjaudu painamalla etusivulla "Login" -nappia.
2. Anna rekisteröimäsi tunnukset, tai kirjaudu oletuskäyttäjänä, jos suoritit komennon `python3 initialize_db.py`. Oletuskäyttäjän tunnukset ovat `user defaultpassword`. Oletusylläpitäjän tunnukset ovat `admin adminpassword`. Kirjautuminen tapahtuu "Login"-nappia painamalla.

### Palaaminen etusivulle tai taaksepäin
1. Klikkaa joko ylärivillä sijaitsevaa Forum-logoa, kotilogoa. Palataksesi taaksepäin, voit klikata keskustelualuenäkymän tai ketjunäkymän oikealla puolella sijaitsevaa breadcrumb-valikkoa.

### Ketjun luominen
1. Valitse keskustelualue etusivulla.
2. Klikkaa "New Thread" -nappia.
3. Anna ketjun otsikko ja aloitusviesti.

### Viestin kirjoittaminen
1. Avaa haluamasi ketju haluamallasi keskustelualueella.
2. Kirjoita uusi viesti ja lähetä se "Submit" -napilla.

### Ketjun ja viestin muokkaaminen
1. Avaa oma ketjusi tai navigoi viestiisi.
2. Klikkaa "Edit" -painiketta ja tee tarvittavat muutokset. Ketjun ostikkoa voivat muokata ylläpitäjät ja ketjun luoja. Viestejä voi muokata vain ne luonut käyttäjä. Muokkaaminen lisää viestiin pysyvän tunnisteen muokkaamisesta.

### Ketjujen ja viestien poistaminen
1. Avaa oma ketjusi tai navigoi viestiisi.
2. Klikkaa "Delete" -painiketta. Ketjua poistaessa sinun tulee vahvistaa vielä kertaalleen painamalla "Yes" painiketta vahvistaaksesi, tai "No" jos haluat siirtyä takaisin. Viestien poistoa ei tarvitse vahvistaa, vaan "Delete" poistaa ne suoraan. Ketjun poistaminen poistaa automaattisesti kaikki sen sisällä olevat viestit ja tykkäykset.

### Omien tietojen tarkastelu
1. Kirjaudu sisään.
2. Klikkaa oikeassa yläkulmassa sijaitsevaa nappia "Hi, käyttäjänimi".
3. Näet sivulla liittymisaikasi, tykkäyksesi, luomasi ketjut, luomasi viestit. Voit siirtyä linkkejä klikkaamalla ketjuihin tai viesteihin.

### Viestien hakeminen
1. Klikkaa oikeassa yläkulmassa sijaitsevaa suurennuslasinappia.
2. Kirjoita hakusana, ja paina hakunappia "Search". Ylläpitäjät näkevät haussa myös piilotettujen alueiden viestejä.

### Keskustelualueen luominen (vain ylläpitäjät)
1. Klikkaa etusivulla "New topic" painiketta.
2. Anna sopiva uniikki "Topic text id", joka näkyy URL:ssä, uniikki keskustelualueen otsikko, sekä kuvaus.
3. Halutessasi voit myös ruksata "Hidden topic?"-laatikon, jolloin keskustelualue ei näy normaaleille käyttäjille.

### Keskustelualueen muokkaaminen (vain ylläpitäjät)
1. Siirry jonkin keskustelualueen sivulle etusivulta.
2. Klikkaa "Edit" -painiketta, ja täytä tekstilaatikot samalla tavalla kuin aluetta luodessa. Huomaa, että topic text id:n ja otsikon täytyy edelleen olla uniikki. Muokatessa voi myös muuttaa keskustelualueen "hidden"-tilaa.

### Keskustelualueen poistaminen (vain ylläpitäjät)
1. Siirry jonkin keskustelualueen sivulle etusivulta.
2. Klikkaa "Delete" -painiketta. Vahvista poisto painikkeella "Yes", tai siirry takaisin painikkeella "No". Poistaminen poistaa kaikki ketjut, viestit ja tykkäykset keskustelualueen sisältä.