"""Script to find contacts on pleinair site."""

import sys
import requests
from BeautifulSoup import BeautifulSoup

base_url = "http://www.fieracavalli.it"
search_url_base = "http://www.fieracavalli.it/mosaic/search/it/espositori-fieracavalli-2014"
args_search = "?loc=&make_search=go&name-field=&tipologia[]=%s"
pagination_url = "page/%s/"


def get_contact_details(url):
    "get email and contact details"

    html = get_html(url)
    contact = {}
        
    # importo il nome dell'azienda
    field = html.find('h1', {'class':'title'})
    name=BeautifulSoup(field.text)
    contact['nome']=name
    #print 'Nome: ',name

    # importo le informazioni
    field = html.find('div', {'class':'content'})
    name=BeautifulSoup(field.text)
    app=name.text
    app = app.replace('\n',' ')
    contact['info']=app
    #print 'Informazioni: ',name

    # importo l'indirizzo
    field = html.find('td', {'class':'bd address'})
    name=BeautifulSoup(field.text)
    contact['ind']=name
    #print 'Indirizzo: ',name

    # importo i recapiti
    # prima la stringa
    field = html.find('table', {'class':'exhibitor_tab anagraphic'})
    field = field.find('td',{'class':'bd'})
    
    name=BeautifulSoup(field.text)
    app=name.text
    
    # poi estraggo i campi
    
    title  = app.find('fax:')
    title1 = app.find('email:')
    title2 = app.find('web:')
    telefono = app[6:title]
    contatti = app[title1:title2]
    title = title+4
    fax = app[title:title1]
    title1=title1+6
    mail = app[title1:title2]
    title2 = title2+4
    web = app[title2:]

    contact['tel'] = telefono
    contact['fax'] = fax
    contact['mail'] = mail
    contact['web']=web

    return contact

def search_contacts(html, result):
    """analyze pages"""

    url = search_url_base
    html = get_html(url)
        
    lista = html.find('div', {'class': 'strongstories right mosaic'})
    links = lista.findAll('div', {'class': 'card article_mosaic article_mosaic_exhibitor'}) 
    
    for alink in links:
        rif = alink.find("a")
        
        new_url = base_url+rif.get("href")
        contact = get_contact_details(new_url)
        result.append(contact)

def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    return soup

def search_locations():
    """Search list of doctors with that name"""

    result = []

    # pagina unica
    url = search_url_base
    html = get_html(url)
    search_contacts(html, result)

    return result


def main():
    """Main entry point for the script."""

    from json2csv import dump_json_as_csv

    result = search_locations()

    fields = ['nome', 'mail', 'web', 'tel', 'fax', 'ind', 'info']
    print dump_json_as_csv(result, fields)


if __name__ == '__main__':
    sys.exit(main())
