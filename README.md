# Keskustelusovellus (Tsoha-projekti)

Sovellus on toteutus keskustelufoorumista, jolla on keskustelualueita eri aiheille. Alueilla on keskusteluketjuja, joille näkyy tilastoja, kuten aloittaja, tietoja viimeisimmästä viestistä ja lukijoiden ja vastausten määrä. Sovelluksen tarkoituksena on ottaa inspiraatiota vanhan koulukunnan keskustelupalstoista, ja luoda sovellus jolla on moderni ulkoasu ja toiminnallisuus.

## Sovelluksen testaaminen

1. Asenna vaaditut moduulit tiedostosta `requirements.txt`
2. Luo `.env` tiedosto, jossa asetat tietokannan sijainnin ja salaisen avaimen, esim:
```
DATABASE_URL=postgresql:///user
SECRET_KEY=95d3763bb55e744e77dd181a47b4e1c6
```
3. Luo pöydät PostgreSQL tietokantaan käynnistämällä ensin psql, sitten suorittamalla komento `\i schema.sql`
4. Käynnistä sovellus komennolla `flask --app app.py run`

## Sovelluksen ominaisuuksia:

 * Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 * Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
 * Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
 * Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
 * Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
 * Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
 * Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
 * Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.