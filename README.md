[![DOI](https://zenodo.org/badge/20943/stenskjaer/kardinaldyder.svg)](https://zenodo.org/badge/latestdoi/20943/stenskjaer/kardinaldyder)

Korpus
======

Data og værktøjer anvendt i mine undersøgelser af kardinaldyderne i den græske litteratur frem til starten af fjerde århundrede.

Dette repository indeholder fire mapper:
- frekvenstabel: antal forekomster af de eftersøgte termer i litteraturen frem til og med Platon.
- kollokationer: Kollokationslister for kardinaldyderne og omkringliggende begreber frem til og med Platon.
- lemmata: Fem forskellige lemmafiler der kan anvendes til korpuslingvistisk analyse af græske tekster. 
- scripts: En lille gruppe programmer jeg har skrevet og anvendt i forbindelse med undersøgelserne.

## Frekvenstabel

Tabel med frekvenser for de udvalgte søgetermer samt yderligere nogle termer som ikke er inddraget i bogen. Tabellen indeholder absolutte og relative værdier for samtlige begreber i alle de inddragede forfatterskaber samt nogle få ekstra. For samtlige frekvenser er der beregnet log likelihood værdi for dens afvigelse af gennemsnittet, og på baggrund af denne sandsynligheden for at denne afvigelse af tilfældig.

Filerne er struktureret som CSV-filer (comma seperated values). Det er almindelige tekstfiler som enten kan læses online eller downloades. Vælger man at åbne filerne lokalt, læses de nemmest i en spreadsheet editor som understøtter UTF-8.

Jeg anbefaler at åbne filerne i [Libre Office](http://da.libreoffice.org/), som læser dem problemfrit. Excel kan anvendes, men jeg anbefaler det ikke da det kan give problemer med de græske bogstaver.


## Kollokationer


Kollokationslister for litteraturen frem til Platon (inklusive). Når kun meget få og uvæsentlige kollokationer har optrådt for et begreb, er listen ikke tilgængelig.

Listerne er ikke fejlfri. På grund af sammenfald af former der kan tilskrives forskellige græske lemmaer, misforstår softwaren til tider hvilket lemma der forekommer i teksten. Der er sorteret i lemma-listerne (se nedenfor) for at afhælpe de største problemer.


## Lemmata


Fem forskellige, men forbundne, lemma-lister. De kan være meget praktiske til korpuslingvistisk analyse af oldgræsk litteratur. 

Listerne er baseret på _LSJ_ og kompileret af TLG-softwaren _Diogenes_. 
Filen `beta_lemmata.txt` er tilgængelig på [SourceForge](http://sourceforge.net/projects/diogenes/files/diogenes/3.1.6/)
 (diogenes-expert-data-3.1.6.tar.bz2) 

`original_lemmata.txt` er `beta_lemmata.txt` konverteret til unicode med værktøjet [BetaCodeConverter](http://www.lucius-hartmann.ch/programme/bcconver.php) til Mac OS X. 

`modified_lemmata.txt` er ovenstående fil modificeret for at afhjælpe de største problemer med sammenfaldende former. Jeg har fjernet de dobbelte former der måtte være i det lemma der generelt er mindst hyppigt. Det er naturligvis ikke nogen optimal fremgangsmåde, men uden et annoteret korpus der angiver netop hvilket lemma hvert ord er, ser jeg ikke anden løsning her. Hvis man mangler en almen lemmaliste til korpuslingvistisk analyse af oldgræske tekster, er dette den mest anvendelige fil. 

`concat_orthodox_lemmata.txt` er ovenstående fil med fire trunkerede lemmata for de fire ortodokse kardinaldyder. Disse lemmata anvendes til at danne kollokationslister efter samme principper som de generelle TLG-søgninger, der også baserer sig på trunkerede former. Principperne for disse søgninger er behandlet i min bog.

`concat_extended_lemmata.txt` svarer til ovenstående fil, men hvor de trunkerede lemmata inkluderer de tre forbundne former som også indgår i ordgrundlaget (φρον, οσι, ευσεβ).

## Programmer

To små programmer beregnet på manipulation og beregning af tekster til
brug i korpusundersøgelser. Begge programmer er skrevet i `Python` og
kræver version 3.0 eller derover. De er ikke testet grundigt, men
forventes at virke som forventet på Unix-systemer (Max OSX, Linux og
lignende). De er ikke testet på Windows endnu.

Nedenfor beskriver jeg kort hvad programmer kan og hvordan man bruger
dem. De er beregnet til at køre fra en terminal-emulator (BASH, shell,
zsh, Terminal og lignende). Med argumentet `-h` eller `--help` kan man
også se en kort vejledning til brug af programmerne og hvilke
kommandoer der er indbygget (eksempelvis
`preprocess.py --help`). Programkoden er også relativt
veldokumenteret, så der kan man også finde en del mere info.

Det er forudsat at man har en smule erfaring med navigation og
anvendelse af en terminal. Se eventuelt
[her](http://www.dummies.com/how-to/content/how-to-use-basic-unix-commands-to-work-in-terminal.html)
og
[her](https://mattwilcox.net/archives/a-very-basic-introduction-to-the-command-line-terminal-and-shell/).

### `preprocess.py`

Programmet skal forberede tekstfiler til yderligere korpuslingvistisk
analyse. Det indeholder følgende muligheder:
* Fjernelse af overflødig luft (mellemrum, tabulator o.l.).
* Fjernelse af accenter i fx græsk eller fransk tekst.
* Fjernelse af linjeskift.
* Konvertering af filer i beta-code format til Unicode UTF-8 (kræver
programmet TLGU, se nedenfor).

Man kan enten processere filer i en mappe eller en enkelt fil som
allerede er i Unicode-format. Alternativt kan man konvertere én
beta-code formateret (eksporteret fra TLG) fil til Unicode som en del
af processen. En fil eksporteret fra TLG databasen svarer til ét
forfatterskab. 

Konverteringen opdeler teksterne efter værker. En konvertering af
Homer vil eksempelvis resultere to filer, én for henholdsvis *Iliaden*
og *Odysseen*. I TLG-databasen og på hjemmesiden
(http://stephanus.tlg.uci.edu/) foreligger lister over hvilke værker
et forfatterskab omfatter. Den ligger også herinde under navnet
`doccan1_u.txt`.

Når man konverterer en beta-code fil eller processerer en mappe med
flere Unicode-filer, er det muligt at vælge hvorvidt de færdige filer skal
samles til én fil eller gemmes som separate filer.

Konverteringen fra beta-code til Unicode kræver at programmet TLGU er
installeret. Det kan downloades på http://tlgu.carmen.gr/ og skal
enten befinde sig i samme mappe som `preprocess.py`-skriptet eller
et andet sted hvor systemet kan finde det (se mere på dette
[link](http://www.cyberciti.biz/faq/unix-linux-adding-path/)). 

Efter de forskellige parametre for processeringen følger det eneste
obligatoriske argument hvor det angives hvor den fil eller mappe som
skal behandles befinder sig. Endelig kan man tilføje hvor resultatet
skal gemmes.

#### Eksempler

Følgende eksempler antager at vi befinder os i samme mappe som
programmet. 

```
./preprocess.py --linebreaks --whitespace homer-unicode.txt
```

Fjern linjeskift og mellemrum i én fil som hedder `homer-unicode.txt`
og befinder sig i samme mappe som programmet. Resultatet bliver
spyttet ud som én fil med titlen `output.txt`. I stedet for
`--linebreak` og `--whitespace` kan de kortere version `-l` og `-w`
også bruges og må gerne skrives sammen til `-lw`

```
./preprocess.py -bwlm ~/Documents/korpus/raw/homer.txt ~/Documents/korpus/processed
```
Et lidt mere kompleks eksempel. Konverterer fra beta-code til Unicode
(`-b`), fjerner overflødige mellemrum (`-w`) og alle linjeskif (`-l`)
og samler endelig alle de processerede filer til én samlet fil.
Programmet vil finde den fil der skal konverteres i
`~/Documents/korpus/raw/homer.txt` og putte den færdige fil i
`~/Documents/korpus/processed` (hvis mappen ikke findes, oprettes
den).

```
./preprocess.py -bwlma ~/Documents/korpus/raw/homer.txt ~/Documents/korpus/processed
```
Magen til ovenstående, men fjerner også alle accenter. Denne kommando
har jeg anvendt til at forberede filer til behandling med programmet `positions.py`

### `positions.py`


