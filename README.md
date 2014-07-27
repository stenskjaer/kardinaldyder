Korpus
======

Data og værktøjer anvendt i mine undersøgelser af kardinaldyderne i den græske litteratur frem til starten af fjerde århundrede.

Dette repository indeholder fire mapper:
- frekvenstabel: antal forekomster af de eftersøgte termer i litteraturen frem til og med Platon.
- kollokationer: Kollokationslister for kardinaldyderne og omkringliggende begreber frem til og med Platon.
- lemmata: Fem forskellige lemmafiler der kan anvendes til korpuslingvistisk analyse af græske tekster. 
- scripts: En lille gruppe programmer jeg har skrevet og anvendt i forbindelse med undersøgelserne.

Frekvenstabel
-------------
Tabel med frekvenser for de udvalgte søgetermer samt yderligere nogle termer som ikke er inddraget i bogen. Tabellen indeholder absolutte og relative værdier for samtlige begreber i alle de inddragede forfatterskaber samt nogle få ekstra. For samtlige frekvenser er der beregnet log likelihood værdi for dens afvigelse af gennemsnittet, og på baggrund af denne sandsynligheden for at denne afvigelse af tilfældig.

Filerne er struktureret som CSV-filer (comma seperated values). Det er almindelige tekstfiler som enten kan læses online eller downloades. Vælger man at åbne filerne lokalt, læses de nemmest i en spreadsheet editor som understøtter UTF-8.

Jeg anbefaler at åbne filerne i [Libre Office](http://da.libreoffice.org/), som læser dem problemfrit. Excel kan anvendes, men jeg anbefaler det ikke da det kan give problemer med de græske bogstaver.


Kollokationer
------------

Kollokationslister for litteraturen frem til Platon (inklusive). Når kun meget få og uvæsentlige kollokationer har optrådt for et begreb, er listen ikke tilgængelig.

Listerne er ikke fejlfri. På grund af sammenfald af former der kan tilskrives forskellige græske lemmaer, misforstår softwaren til tider hvilket lemma der forekommer i teksten. Der er sorteret i lemma-listerne (se nedenfor) for at afhælpe de største problemer.


Lemmata
-------

Fem forskellige, men forbundne, lemma-lister. De kan være meget praktiske til korpuslingvistisk analyse af oldgræsk litteratur. 

Listerne er baseret på _LSJ_ og kompileret af TLG-softwaren _Diogenes_. 
Filen `beta_lemmata.txt` er tilgængelig på [SourceForge](http://sourceforge.net/projects/diogenes/files/diogenes/3.1.6/)
 (diogenes-expert-data-3.1.6.tar.bz2) 

`original_lemmata.txt` er `beta_lemmata.txt` konverteret til unicode med værktøjet [BetaCodeConverter](http://www.lucius-hartmann.ch/programme/bcconver.php) til Mac OS X. 

`modified_lemmata.txt` er ovenstående fil modificeret for at afhjælpe de største problemer med sammenfaldende former. Jeg har fjernet de dobbelte former der måtte være i det lemma der generelt er mindst hyppigt. Det er naturligvis ikke nogen optimal fremgangsmåde, men uden et annoteret korpus der angiver netop hvilket lemma hvert ord er, ser jeg ikke anden løsning her. Hvis man mangler en almen lemmaliste til korpuslingvistisk analyse af oldgræske tekster, er dette den mest anvendelige fil. 

`concat_orthodox_lemmata.txt` er ovenstående fil med fire trunkerede lemmata for de fire ortodokse kardinaldyder. Disse lemmata anvendes til at danne kollokationslister efter samme principper som de generelle TLG-søgninger, der også baserer sig på trunkerede former. Principperne for disse søgninger er behandlet i min bog.

`concat_extended_lemmata.txt` svarer til ovenstående fil, men hvor de trunkerede lemmata inkluderer de tre forbundne former som også indgår i ordgrundlaget (φρον, οσι, ευσεβ).


Scripts
-------

En lille samling af forskellige programmer anvendt til tekstmanipulation, beregninger og produktion af diagrammer i forbindelser med ordundersøgelserne.

Der er simple, rodede og uskønne skripts som virkelig kunne trænge til en gennemarbejdning.
De vigtigste i undersøgelserne er:

- `compile_corpus.php`: Samler filer for en angiven forfatter i specificeret mappe og samler alle korpusfiler med et trecifret nummer inden .txt-suffikset til én fil. Det erstatter også alle gravis-accenter med acut'er og transponerer hele filen til minuskler for at optimere de statistiske resultater og foretager mindre oprydning i teksten (fjerner linjeskift og overflødige mellemrum)
Konvertering af TLG-filer fra beta kode til unicode er udført med [tlgu](http://tlgu.carmen.gr/tlgu.1.html).
- `str_pos.php`: Beregner placeringen af eftersøgte begreber og generer det output der benyttes til at lave dispersionstabeller i LaTeX. Beregner også blandt andet standard afvigelse som indgår i undersøgelserne.

De øvrige filer er temmeligt rodede og indgår ikke længere aktivt i arbejdet. Der er blandet andet funktioner til at fjerne accenter fra polytonisk græsk og forskellige forsøg på at konvertere beta kode til unicode (uden meget held). 
 


