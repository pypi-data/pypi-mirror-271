import pytest
from nl_matcher import LocationMatcher

location_matcher = LocationMatcher()

testdata = [
    (
        "Al ruim twee jaar rookt bij elke frisse dag de houtkachel aan de "
        "Fluitekamp in Hoogland.",

        'Fluitekamp in Hoogland'
    ),

    (
        "Terwijl dit gesprek door gaat, komt een man de Hema in Montfoort "
        "binnen en rekent twee powerbanks af met de pas van het slachtoffer.",

        'Hema in Montfoort'
    ),

    (
        "Was u getuige van de aanval in de Maarssense wijk Zwanenkamp op "
        "woensdag 1 februari? Bel dan met de tiplijn: 0800 - 6070 of bel "
        "Meld Misdaad Anoniem: 0800 - 7000. Beelden waarop de dader te "
        "zien is kunt u uploaden via politie.nl/upload",

        'Maarssense wijk Zwanenkamp'
    ),

    (
        "Het 75-jarige jubileum van de vrijwillige politie werd vandaag "
        "gevierd bij evenementenlocatie Mereveld in Utrecht.",
        'Mereveld in Utrecht'
    ),

    (
        """Vleuten - Zondagavond 12 maart rond 22.30 uur was er een explosie bij een woning aan de Moersbergen in Vleuten.""",
        'Moersbergen in Vleuten'
    ),

    (
        """Utrecht - Straatafval, drugshandel, geluidoverlast en intimidatie. Bewoners van een flat aan de Marco Pololaan in de Utrechtse wijk Kanaleneiland zijn naar eigen zeggen al jaren met politie en gemeente in de weer om de overlast van een groep hangjongeren en volwassen mannen in hun straat te weren, vooralsnog zonder resultaat.""", 'Marco Pololaan in de Utrechtse wijk Kanaleneiland'),

    (
        """Vleuten - Zondagavond 12 maart rond 22.30 uur was er een explosie bij een woning aan de Moersbergen in Vleuten.""",
        'Moersbergen in Vleuten'
    ),

    (
        """Zeist - Op 7 februari steelt een man voor zo'n 300 euro aan tandpasta en andere mondverzorgingsproducten bij de Kruidvat in Zeist.""",
        'Kruidvat in Zeist'
    ),

    (
        """Het gaat om een gebouw aan de Parklaan in de wijk Molenvliet en om een woningbouwgebied dat nog ontwikkeld moet worden bij Snellerpoort en het Stationsgebied.""",
        'Parklaan in de wijk Molenvliet'
    ),

    (
        """Benschop - In één maand tijd is bij drie muziekstudio's ingebroken. Bij de eerste inbraak bij 'Barn in de Meadow' in Benschop verdwenen onder andere gitaren van de Utrechtse band Kensington.""",
        'Benschop'
    ),

    (
        """Wilnis - Een 84-jarige vrouw en haar 59-jarige zoon zijn in de nacht van 5 op 6 maart met geweld overvallen in hun woning in Wilnis.""",
        'Wilnis'
    ),

    (
        """De proef met het inzamelen van lege flesjes op station Utrecht Centraal wordt uitgebreid: vanaf 1 april kun je ook blikjes inleveren voor statiegeld.""",
        'station Utrecht Centraal'
    ),

    (
        """Anouar T., een neef van vermeend topcrimineel Ridouan T., heeft maandag tijdens zijn voorgeleiding de rechter-commissaris van de rechtbank in Zwolle gewraakt. Hij werd vrijdag opgepakt in Utrecht.""",
        'Zwolle'
    ),

    (
        """In Utrecht hoeven jongeren met een bijstandsuitkering niet eerst vier weken te wachten voor ze geld krijgen.""",
        'Utrecht'
    ),

    (
        """Bilthoven - De advocaat van Utrechtse crimineel Ridouan T.""",
        'Bilthoven'
    ),

    (
        """Op de A2 bij Utrecht is een vrachtwagen op een pilaar gebotst. De chauffeur zat bekneld in de cabine maar is door de brandweer bevrijdt.""",
        'A2 bij Utrecht'
    ),

    (
        """Burgemeester Gilbert Isabella van Houten heeft een dwangsom van maximaal 6000 euro opgelegd na de ontdekking van drugshandel en illegale bewoning.""",
        'Houten'
    ),

    (
        """Provincie Utrecht - De huizenprijzen zijn in het eerste kwartaal van dit jaar het hardst gedaald in de provincie Utrecht, namelijk met 3 procent ten opzichte van de eerste drie maanden van vorig jaar.""",
        'Provincie Utrecht'
    ),

    (
        """Provincie Utrecht - Trapper niet in!, is de campagne die de provincie heeft gelanceerd om Utrechters bewuster te maken van de risico's van dronken op de fiets stappen. Want beschonken fietsers belanden steeds vaker en met hevigere verwondingen op de eerste hulp, valt ook de ziekenhuizen op.""",
        'Provincie Utrecht'
    ),

    (
        """Toen was er inderdaad sprake van een lek, Kasteel Heemstede werd op die manier overrompeld met een ster.""",
        'Kasteel Heemstede'
    ),

    (
        """De agenten hielden rond 5.00 uur 's nachts toezicht op uitgaanspubliek op de Hof, waar ze twee mannen aanspraken op hun gedrag.""",
        'de Hof'
    ),
    (
        """Het ging afgelopen vrijdag mis op de Biltse Rading toen de vrouw met twee kinderen overstak op een oversteekplaats tussen de Voorveldse Polder en de Veemarkt.""",
        'oversteekplaats tussen de Voorveldse Polder en de Veemarkt'
    ),

    (
        """De eerste wedstrijd om het landskampioenschap werd vandaag precies 125 jaar geleden gespeeld op het veld van USV Hercules in Utrecht.""",
        'USV Hercules in Utrecht'
    ),

    (
        """In de Utrechtse binnenstad nam de chauffeur van lijn 74 een verkeerde afslag en belandde op de Nieuwegracht, waar de harmonicabus geen kant meer op kon.""",
        'Nieuwegracht'
    ),

    (
        """In het buitengebied van Groenekan vlakbij Voordaan komt een zonneveld van ongeveer 17 hectare.""",
        'Groenekan vlakbij Voordaan'
    ),

    (
        """In Nederland zwaaien de klokken heen en weer en dat is in feite bim bam." Wanneer je bovenin de Onze Lieve Vrouwetoren in Amersfoort staat om naar de enorme klokken te kijken, dan moet je goede gehoorbescherming dragen wanneer ze geluid worden.""",
        'Lieve Vrouwetoren in Amersfoort'
    ),
    (
        """Na het overlijden van de laatste brugwachter Stok in mei 1945, kwam het brugwachtershuisje naast de Evert Stokbrug in Maarssen leeg te staan.""",
        'Evert Stokbrug in Maarssen'
    ),

    (
        """Op de A1 bij de afslag Baarn - Soest is een auto met caravan gecrasht.""",
        'A1 bij de afslag Baarn'
    ),
    (
        """Bij Collectief Eemland zijn ze daar blij mee, want de weidevogel zit in groten getale in de Eempolder.""",
        'in de Eempolder'
    ),
    (
        """Het Comité Joods Monument Baarn is na onderzoek meer te weten gekomen over de identiteit van achttien leerlingen die op de klassenfoto staan.""",
        'Baarn'
    ),

    (
        """Bij het hoofdkantoor bij de Rabobank in Utrecht zijn vanochtend leden van Extinction Rebellion en Christian Climate Action op het dak geklommen om een spandoek op te hangen.""",
        'Rabobank in Utrecht'
    )
]


@pytest.mark.parametrize(["sent", "expected"], testdata)
def test_location_matches(sent, expected):
    span = location_matcher(sent)

    assert span is not None
    assert len(span) > 0
    assert span[0].text == expected
