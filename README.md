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
 - [ ] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Viestejä ja ketjuja voi poistaa vain ylläpitäjä.
 - [ ] Käyttäjä voi tykätä viesteistä, ja nähdä profiilisivullaan omat ketjunsa, viestinsä ja tykätyt viestit.
 - [x] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
 - [x] Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
 - [ ] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

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
1. Avaa oma ketjusi tai viestisi.
2. Klikkaa "Edit" -painiketta ja tee tarvittavat muutokset.

### Omien ketjujen ja viestien tarkastelu
1. Kirjaudu sisään.
2. Klikkaa oikeassa yläkulmassa sijaitsevaa nappia "Hi, käyttäjänimi".
3. Näet sivulla liittymisaikasi, luomasi ketjut ja luomasi viestit.

### Viestien hakeminen
1. Klikkaa oikeassa yläkulmassa sijaitsevaa suurennuslasinappia.
2. Kirjoita hakusana, ja paina hakunappia "Search".