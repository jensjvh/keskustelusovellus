# Keskustelusovellus (Tsoha-projekti)

Sovellus on toteutus keskustelufoorumista, jolla on keskustelualueita eri aiheille. Alueilla on keskusteluketjuja, joille näkyy tilastoja, kuten aloittaja, tietoja viimeisimmästä viestistä ja lukijoiden ja vastausten määrä. Sovelluksen tarkoituksena on ottaa inspiraatiota vanhan koulukunnan keskustelupalstoista, ja luoda sovellus jolla on moderni ulkoasu ja toiminnallisuus.

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
 - [ ] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
 - [ ] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
 - [ ] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
 - [ ] Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
 - [ ] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
