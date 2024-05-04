"""Define content items which will be rendered into templates to generate static python.lt website.

Keys in content_items denote top level menu items.
List items denote information which will be rendered inside elements of flexbox page area.
"""


content_items = {
    'Naujienos': [
        {
            'name': 'NSA informacinių technologijų egzamine nauja programavimo kalba',
            'link': 'https://www.nsa.smm.lt/2022/06/13/informaciniu-technologiju-egzamine-nauja-programavimo-kalba/',
        },
        {
            'name': 'Informatikos mokytojai dalyvavo seminaruose apie Python programavimo kalbos mokymo patirtį',
            'link': 'https://if.ktu.edu/news/informatikos-mokytojai-dalyvavo-seminaruose-apie-pitono-programavimo-kalbos-mokymo-patirti/',
        },
    ],
    'Renginiai': [
        {
            'name': 'PyCon Lithuania - kasmetinė tarptautinė konferencija',
            'link': 'https://pycon.lt/',
        },
        {'name': 'VilniusPy', 'link': 'https://www.meetup.com/VilniusPy'},
        {'name': 'KaunasPy', 'link': 'https://www.meetup.com/KaunasPy'},
        {'name': 'PyData Vilnius', 'link': 'https://www.meetup.com/PyData-Vilnius/'},
        {'name': 'PyData Kaunas', 'link': 'https://www.meetup.com/PyData-Kaunas/'},
    ],
    'Bendruomenė': [
        {
            'name': 'Python Lietuva facebook grupė',
            'link': 'https://www.facebook.com/groups/pythonlt/',
        },
        {
            'name': 'Github projektai su žyme Lietuva',
            'link': 'https://github.com/topics/lithuanian',
        },
    ],
    'Išmok Python': [
        {'name': 'Angis', 'link': 'https://angis.net/#/'},
        {'name': 'Angis github', 'link': 'https://github.com/mantasurbonas/angis'},
        {
            'name': 'IT Brandos egzaminų sprendimai Python kalba',
            'link': 'https://github.com/python-dirbtuves/it-brandos-egzaminai',
        },
        {
            'name': 'Programavimas Python (Youtube grojaraštis)',
            'link': 'https://www.youtube.com/watch?v=IuByH_vrwGA&list=PLB7EF2523A58A7854',
        },
        {
            'name': 'Griaustinis tech Django (Youtube grojaraštis)',
            'link': 'https://www.youtube.com/watch?v=998PannJtHo&list=PL3aaklOBGuJmxk9mrsbbWd45WYFyOWfLc&ab_channel=GriaustinisTech',
        },
    ],
    'Įrankiai': [
        {
            'name': 'Lietuvių kalbos rašybos tikrintuvai bei Hunspell žodynai gramatika',
            'link': 'https://github.com/Semantika2/Lietuviu-kalbos-rasybos-tikrintuvai-bei-Hunspell-zodynai-gramatika',
        },
        {'name': 'Spacy Lietuviu kalbai', 'link': 'https://spacy.io/models/lt'},
    ],
}
