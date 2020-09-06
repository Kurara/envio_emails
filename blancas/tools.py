from bs4 import BeautifulSoup as bs
import re


character_map = {
    " ": "%20",
    "!": "%21",
    "#": "%23",
    "$": "%24",
    "%": "%25",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "*": "%2A",
    "+": "%2B",
    "/": "%2F",
    ":": "%3A",
    ";": "%3B",
    "=": "%3D",
    "?": "%3F",
    "@": "%40",
    "[": "%5B",
    "\\": "%5C",
    "]": "%5D",
    "^": "%5E",
    "`": "%60",
    "{": "%7B",
    "|": "%7C",
    "}": "%7D",
    "~": "%7E",
    "¢": "%A2",
    "£": "%A3",
    "¥": "%A5",
    "|": "%A6",
    "§": "%A7",
    "«": "%AB",
    "¬": "%AC",
    "¯": "%AD",
    "º": "%B0",
    "±": "%B1",
    "ª": "%B2",
    ",": "%B4",
    "µ": "%B5",
    "»": "%BB",
    "¼": "%BC",
    "½": "%BD",
    "¿": "%BF",
    "À": "%C0",
    "Á": "%C1",
    "Â": "%C2",
    "Ã": "%C3",
    "Ä": "%C4",
    "Å": "%C5",
    "Æ": "%C6",
    "Ç": "%C7",
    "È": "%C8",
    "É": "%C9",
    "Ê": "%CA",
    "Ë": "%CB",
    "Ì": "%CC",
    "Í": "%CD",
    "Î": "%CE",
    "Ï": "%CF",
    "Ð": "%D0",
    "Ñ": "%D1",
    "Ò": "%D2",
    "Ó": "%D3",
    "Ô": "%D4",
    "Õ": "%D5",
    "Ö": "%D6",
    "Ø": "%D8",
    "Ù": "%D9",
    "Ú": "%DA",
    "Û": "%DB",
    "Ü": "%DC",
    "Ý": "%DD",
    "Þ": "%DE",
    "ß": "%DF",
    "à": "%E0",
    "á": "%E1",
    "â": "%E2",
    "ã": "%E3",
    "ä": "%E4",
    "å": "%E5",
    "æ": "%E6",
    "ç": "%E7",
    "è": "%E8",
    "é": "%E9",
    "ê": "%EA",
    "ë": "%EB",
    "ì": "%EC",
    "í": "%ED",
    "î": "%EE",
    "ï": "%EF",
    "ð": "%F0",
    "ñ": "%F1",
    "ò": "%F2",
    "ó": "%F3",
    "ô": "%F4",
    "õ": "%F5",
    "ö": "%F6",
    "÷": "%F7",
    "ø": "%F8",
    "ù": "%F9",
    "ú": "%FA",
    "û": "%FB",
    "ü": "%FC",
    "ý": "%FD",
    "þ": "%FE",
    "ÿ": "%FF"
}

def encode_html(string):
    encoded_string = ""
    for char in string:
        encoded_string += character_map.get(char, char)

    return encoded_string
      
      
def extract_paginas_blancas(html_datas):
    list_data = []
    dom = bs(html_datas, "lxml")
    table = dom.find(id="PPAL")

    if table is not None:
        items = table.find_all('div', {"class": "yellad"})
        for item in items:
            _telephone = item.find("span", {"class": "telef"})
            unicode_telephone = re.sub(
                r'(\t|\n|\r)+', '', _telephone.get_text(strip=True)
            )
            telephone = unicode_telephone.replace(u'\xa0', ' ').replace(
                'Imprimir Ficha', ''
            )
            _name = item.find('h3')
            name = ''
            address = '<no disponible>'
            if _name:
                unicode_name = re.sub(
                    r'(\t|\n|\r)+', '', _name.get_text(strip=True)
                )
                name = unicode_name.replace(u'\xa0', ' ').replace(
                    'Imprimir Ficha', ''
                )
            _address = item.find("p")
            if _address:
                unicode_address1 = re.sub(
                    r'(\t|\n|\r)+', '', _address.contents[2].strip()
                )
                unicode_address2 = ''
                if len(_address.contents) > 3:
                    unicode_address2 = re.sub(
                        r'(\t|\n|\r)+', '', _address.contents[4].strip()
                    )
                address = unicode_address1 + ' ' + unicode_address2 
            list_data.append({
                'name': name,
                'telephone': telephone,
                'address': address
            })

    return list_data