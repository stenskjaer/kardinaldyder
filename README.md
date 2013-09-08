korpus
======

Data og værktøjer anvendt i mine undersøgelser af kardinaldyderne.


Korpus
======

Data og værktøjer anvendt i mine undersøgelser af kardinaldyderne.

Dette repository indeholder tre simple mapper:
- kollokationer :: Kollokationslister for kardinaldyderne og omkringliggende begreber frem til Platon.
- lemmata :: Fem forskellige lemmafiler der kan anvendes til korpuslingvistisk analyse af græske tekster. 
- scripts :: Lidt forskellige php-skripts anvendt til tekstmanipulation i forbindelse med undersøgelserne.


Kollokationer
------------

Kollokationslister for litteraturen frem til Platon (inklusiv).

Filerne er struktureret som CSV-filer (comma seperated values). Det er almindelige tekstfiler, men læses nemmest i en spreadsheet editor. Skal åbnes i et program der understøtter UTF-8. 

Jeg anbefaler at åbne filerne i [Libre Office](http://da.libreoffice.org/), som læser dem problemfrit. *Brug ikke Microsoft Excel, det kan ikke finde ud af det græske!*

Bemærk: Listerne er ikke fejlfri. På grund af sammenfald af former der kan tilskrives forskellige græske lemmaer misforstår softwaren til tider hvilket lemma der forekommer i teksten. Der er sorteret i lemma-listerne (se nedenfor) for at afhælpe de største problemer.


Lemmata
-------

Fem forskellige, men forbundne lemma-lister.

Listerne er baseret på /LSJ/ og kompileret af TLG-softwaren /Diogenes/. 
Filen =beta_lemmata.txt= er tilgængelig på [SourceForge](http://sourceforge.net/projects/diogenes/files/diogenes/3.1.6/)
 (diogenes-expert-data-3.1.6.tar.bz2) 

original_lemmata.txt er =beta_lemmata.txt= konverteret til unicode med værktøjet [tlgu](http://tlgu.carmen.gr/tlgu.1.html).

=modified_lemmata.txt= er ovenstående fil modificeret for at afhjælpe de største problemer med sammenfaldende former. Jeg har fjernet de dobbelte former der måtte være i det lemma der generelt er mindst hyppigt. Det er naturligvis ikke nogen optimal fremgangsmåde, men uden et annoteret korpus der angiver netop hvilket lemma hvert ord er, ser jeg ikke anden løsning her.

=concat_orthodox_lemmata.txt= er ovenstående fil med fire trunkerede lemmata for de fire ortodokse kardinaldyder. Disse lemmata anvendes til kollokationslister efter samme principper som de generelle TLG-søgninger, der også baserer sig på trunkerede former.

=concat_extended_lemmata.txt= svarer til ovenstående fil, men hvor de trunkerede lemmata inkluderer de tre forbundne former som også indgår i ordgrundlaget (φρον, οσι, ευσεβ).


Scripts
-------

En lille samling af forskellige amatørskripts anvendt til tekstmanipulation og beregninger i forbindelser med ordundersøgelserne.

Der er simple, rodede og uskønne skripts som virkelig kunne trænge til en gennemarbejdning.
De vigtigste i undersøgelserne er:

- compile_corpus.php :: Samler filer for en angiven forfatter i specificeret mappe og samler alle korpusfiler med et trecifret nummer inden .txt-suffikset til én fil. Det erstatter også alle gravis-accenter med acut'er og transponerer hele filen til minuskler for at optimere de statistiske resultater og foretager mindre oprydning i teksten (fjerner linjeskift og overflødige mellemrum)
- str_pos.php :: Beregner placeringen af eftersøgte begreber og generer det output der benyttes til at lave dispersionstabeller i LaTeX. 

De øvrige filer er temmeligt rodede og indgår ikke længere aktivt i arbejdet. Der er blandet andet funktioner til at fjerne accenter fra polytonisk græsk og forskellige forsøg på at konvertere beta kode til unicode (uden meget held). 
 


