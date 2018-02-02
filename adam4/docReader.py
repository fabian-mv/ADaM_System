import re

from os import walk
from os.path import join, abspath , splitext
import base64
import datetime
import copy
import docx2txt

import csv
from adam4 import urlmarker

"""
          _____          __  __    _______     _______ _______ ______ __  __ 
    /\   |  __ \   /\   |  \/  |  / ____\ \   / / ____|__   __|  ____|  \/  |
   /  \  | |  | | /  \  | \  / | | (___  \ \_/ / (___    | |  | |__  | \  / |
  / /\ \ | |  | |/ /\ \ | |\/| |  \___ \  \   / \___ \   | |  |  __| | |\/| |
 / ____ \| |__| / ____ \| |  | |  ____) |  | |  ____) |  | |  | |____| |  | |
/_/    \_\_____/_/    \_\_|  |_| |_____/   |_| |_____/   |_|  |______|_|  |_|
                    -Automatic Database Migration System-                    
"""


#------------------------------------WORK FUNCTIONS------------------------------------#

def get_text_from(path , verbose):
    """Extract and format text from a docx file.

    Keyword arguments:
    path -- path to the file
    """
    text = ""
    try:
        text = str(docx2txt.process(path))                         # gets text from a docx
    except:
        None
    #PRODUCTS_ORG_REPLACEMENTS
    text = text.replace("Asociación Centro de Integración Ocupacional y Servicios Afines: -ACIOSA-" , "Asociación Centro de Integración Ocupacional y Servicios Afines, ACIOSA")
    text = text.replace("Asociación Centro de Integración Ocupacional y Servicios Afines -ACIOSA-", "Asociación Centro de Integración Ocupacional y Servicios Afines, ACIOSA")
    text = text.replace(" Fines:" , " Fines: ")
    text = text.replace("Sí", "Si")                            # replaces characters
    text = text.replace("sí", "Si")                            # replaces characters
    text = text.replace("Observaciones :" , "Observaciones:")  # remove the extra space on "Observaciones" word
    text = text.replace("Teléfono (s)" , " telelelelele ")
    text = text.replace("Teléfono(s)", " telelelelele ")
    text = text.replace("Teléfono (s) ", " telelelelele ")
    text = text.replace("Teléfono(s) ", " telelelelele ")
    text = text.replace("telelelelele:", " telelelelele ")
    text = text.replace("Señale el tipo de oferente del producto de apoyo", " Señale el tipo de oferente del servicio de apoyo")
    text = text.replace("Nombre del servicio de apoyo"," Nombre del producto de apoyo")
    text = text.replace("Fax:", "Fax")
    text = text.replace("fax:", "Fax")
    text = text.replace("fax", "Fax")
    text = text.replace("\n" , " ")                            # removes all newline characters from text
    text = text.replace("\t" , " ")                            # replaces tabs with spaces
    text = text.replace("●" , "")                              # removes all bullets from text
    text = re.sub(' +' , ' ' , text)                           # removes all repeated whitespace from text
    text = text.replace("Nombre del ente que brinda el servicio de apoyo (institución, municipalidad, empresa u organización no gubernamental):", "Nombre del ente que brinda el producto de apoyo (institución, municipalidad, empresa u organización no gubernamental):")
    text = text.replace("4. Descripción del ente", "4. Descripción del ente que brinda el producto de apoyo")
    text = text.replace(" Características generales, uso, aplicaciones y existencia del producto de apoyo", "Ubicación")
    text = text.replace("Nombre del ente que brinda el servicio de apoyo:", "Nombre del ente que brinda el producto de apoyo (institución, municipalidad, empresa u organización no gubernamental):")
    #PRODUCTS_ITEM_REPLACEMENTS
    text = text.replace("Nombre del prod. de apoyo: Indique el nombre completo del servicio de apoyo que se brinda","Nombre del producto de apoyo: Indique el nombre completo del servicio de apoyo que se brinda")
    text = text.replace("Nombre del producto de apoyo: Indique el nombre completo del producto de apoyo, como lo enuncia la entidad que lo brinda.","Nombre del producto de apoyo: Indique el nombre completo del servicio de apoyo que se brinda")
    text = text.replace("Nombre del producto de apoyo: Indique el nombre completo del producto de apoyo como lo enuncia la entidad que lo brinda.","Nombre del producto de apoyo: Indique el nombre completo del servicio de apoyo que se brinda")
    text = text.replace(" fines:","Fines:")
    text = text.replace(" Fínes:","Fines:")
    text = text.replace(" fínes:","Fines:")
    text = text.replace(" fines","Fines:")
    text = text.replace(" Fínes","Fines:")
    text = text.replace(" fínes","Fines:")
    text = text.replace("14. Clasificación del producto de apoyo","Para uso interno ")
    text = text.replace("Observaciones: Consignar en este último apartado, algún detalle o característica del producto de apoyo, que no quede reflejado en los ítems anteriores de esta ficha.","Observaciones:")
    text = text.replace("Localización del servicio de apoyo","7. Uso y aplicaciones del producto de apoyo")
    text = text.replace("7. Localización de la Organización","7. Uso y aplicaciones del producto de apoyo")

    print("\033[94mTEXTO: \033[0m" + text) if verbose else None
    return text


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def get_files_from(path):
    all = []
    count = -1
    for (direc, dirs, files) in walk(path):
        middleList = []
        if files != []:
            allow = False
            for file in files:
                if file.endswith(".docx"):
                    middleList.append(join(abspath(direc), file))
                    all.append(middleList)
                    allow = True
                    count += 1
            if allow:
                for file in files:
                    if file.endswith((".jpeg", ".jpg", ".png", ".gif", ".JPG")):
                        all[count].append(join(abspath(direc), file))
    return all


def encode_image(path):
    prefix = "data:image/" + splitext(path)[1][1:] + ";base64,"
    with open(path, "rb") as image_file:
        encodedImage = prefix + str(base64.b64encode(image_file.read())).replace("b'" , "").replace("'" , "")
        print(encodedImage)
        return encodedImage


# ------------------------------------PRODUCTS------------------------------------ #

def get_product_cost(text):
    start = "Costo del producto de apoyo: "
    end = " Opciones similares a ese producto"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mCost:\033[0m " + needle)
    return needle


def get_product_warranty(text):
    start = "Garantía: "
    end = " El producto se mantiene en el stock"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mwarranty:\033[0m " + needle)
    return needle


def get_product_instock(text):
    start = "El producto se mantiene en el stock: Si ( "
    end = " ) No ("
    needle = text[text.find(start) + len(start): find_nth(text , end , 1)]
    if needle == "X" or needle == "x":
        print("\t\033[94minstock:\033[0m 1")
        return 1
    else:
        print("\t\033[94minstock:\033[0m 0")
        return 0


def get_product_timeDelivery(text):
    start = "Tiempo de duración del trámite de importación: "
    end = " La garantía es igual"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mtimeDelivery:\033[0m " + needle)
    return needle


def get_product_warrantyImported(text):
    start = "La garantía es igual, si el producto es importado:"
    end = " ) No ("
    needle = text[text.find(start) + len(start): find_nth(text , end , 3)]
    if needle == "X" or needle == "x":
        print("\t\033[94mwarrantyImported:\033[0m 1")
        return 1
    else:
        print("\t\033[94mwarrantyImported:\033[0m 0")
        return 0


def get_product_usefulLife(text):
    start = "Stock de repuestos y durabilidad del producto: "
    end = " El personal de la empresa asesora sobre el uso del producto"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94musefulLife:\033[0m " + needle)
    return needle


def get_product_primaryFuncionalities(text):
    start = "Funciones: "
    end = " Usos:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mprimaryFuncionalities:\033[0m " + needle)
    return needle


def get_product_brand(text):
    start = "Marca(s):"
    if text.find(start) == -1:
        start = "Marca (s):"
    end = " Garantía:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mbrand:\033[0m " + needle)
    return needle


def get_date():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# ------------------------------------ITEMS------------------------------------ #

def get_item_name(text):
    start = "Nombre del producto de apoyo: Indique el nombre completo del servicio de apoyo que se brinda"
    if text.find(start) == -1:
        start = "Nombre del producto de apoyo:"
    end = "7. Uso y aplicaciones del producto de apoyo"
    needle = text[text.find(start) + len(start): text.find(end)]
    if needle == "No brinda información":
        needle = "Clinicas Audición"
    print("\t\033[94mName of item:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_name_service(text):
    start = "de apoyo que se brinda "
    if text.find(start) == -1:
        start = "de apoyo como lo enuncia la entidad que lo brinda."
        if text.find(start) == -1:
            start = "de apoyo, como lo enuncia la entidad que lo brinda."
    end = "Localización del servicio de apoyo:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mName of service:\033[0m " + needle)
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_description_products(text):
    start = "Fines:"
    if text.find(start) == -1:
        print("\t\033[94mDescription of product/service:\033[0m -")
        return "-"
    end = "Misión:"
    if text.find(end) == -1:
        end = "Objetivos"
    needle = text[find_nth(text, start, 1) + len(start): text.find(end)]
    print("\t\033[94mDescription of product/service:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_description_service(text):
    start = "Fines:"
    if text.find(start) == -1 or text.count(start) < 2:
        print("\t\033[94mDescription of product/service:\033[0m -")
        return "-"
    end = "Misión:"
    if text.find(end) == -1:
        end = "Objetivos"
    needle = text[find_nth(text, start, 1) + len(start): text.find(end)]
    print("\t\033[94mDescription of product/service:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_observations_products(text):
    start = "Observaciones:"
    end = "Para uso interno "
    needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
    print("\t\033[94mObservations:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_observations_services(text):
    start = "Observaciones: Indique aquí información que considere importante, detalle características del servicio que no queden reflejadas en los ítems anteriores."
    end = "Para uso interno "
    if text.find(end) == -1:
        end = "."
    needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
    print("\t\033[94mObservations:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle

def get_item_typeDeficiency(text):
    start = "Tipo de discapacidad:"
    end = "Otra:"
    if text.find(end) == -1:
        end = "15. Horario del servicio"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mtypeDeficiency:\033[0m " + needle)
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    return needle


def get_item_age(text):
    start = "Grupo etario (edad):"
    if text.find(start) == -1:
        print("\t\033[94mage:\033[0m " + "-")
        return {"age":"No brinda información."}
    end = "Tipo de discapacidad:"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")  # removes all newline characters from text
    needle = needle.replace("\t", " ")  # replaces tabs with spaces
    needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mage:\033[0m " + str({'age' : str(needle)}))
    return {"age" : str(needle)}


def get_item_sex(text):
    start = "Género:"
    end = "Grupo etario"
    if text.find(end) == -1:
        end = ") "
    needle = text[text.find(start) + len(start): find_nth(text, end, 1)]

    count = 0
    if needle.find("X") != -1:
        tofind = needle.find("X")

        while tofind > 0:
            count += 1
            tofind = needle.find("X", tofind+1)
    else:
        tofind = needle.find("x")

        while tofind > 0:
            count += 1
            tofind = needle.find("x", tofind + 1)

    print("\t\033[94msex:\033[0m " + str(count))
    return count


def get_item_organizationidPk_service(text):
    names = {'12' : 'Asociación Pro-Discapacidad San Pedro de Poás' , '41': 'Clinicas Audición', '62': 'Asociación Pro-Ayuda a la Persona con Discapacidad de Zarcero, Llano Bonito y San Antonio, APAMAR', '25': 'Municipalidad de Carrillo, Guanacaste', '74': 'Centro de educación especial Grecia', '53': 'Fundación Doctora Chinchilla de Reyes.', '31': 'Asociación Semillas de Esperanza Pro-Apoyo y Rehabilitación de Hojancha, Guanacaste.', '16': 'Ayudas Técnicas que entrega la CCSS como institución en cada uno de sus hospitales.', '7': 'Asociación Pro-Patronato Nacional de Ciegos.', '46': 'Asociación Atjala ( CAIPAD)', '24': 'Sistema de Accesibilidad Total S.A', '40': 'Clinica de Terapia Física María Goretti.', '17': 'Clínica Dinamarca', '63': 'Hospital de San Carlos - CCSS', '11': 'Centro Educativo Dr. Carlos Sáenz Herrera', '80': 'Asociación Centro de Integración Ocupacional y Servicios Afines, ACIOSA', '36': 'Asociación Fraternidad Cristiana de Personas con Discapacidad', '6': 'Sear Médica', '57': 'Fundación Servio Flores Arroyo', '60': 'Hospital San Rafael de Alajuela - CCSS', '18': 'JR Sánchez Audiología', '79': 'Asociación Centro de Formación Socio-Productivo para el Desarrollo de las Personas Discapacitadas.', '51': 'Hospital Carlos Luis Valverde Vega CCSS', '15': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.', '39': 'Centro de Educación Especial de Turrialba', '37': 'Centro Educación Especial Carlos Luis Valle', '76': 'Asociación de Ayuda al Minusválido de San Carlos, AYUMISANCA.', '65': 'Asociación MORFAS (Miembros Organizados Fomentando Acciones Solidarias).', '78': 'Municipalidad de Alajuela', '70': 'Asociación Taller Protegido de Alajuela.', '64': 'Centro Especializado en Terapia del lenguaje, habla y voz', '81': 'Asociación Amigos del Grupo de Percusión-Inclusión -AAGRUPERI-', '75': 'Ministerio de Educación Pública: Centro de Enseñanza Especial Marta Saborío Fonseca, Alajuela', '10': 'Disprodorme S.A', '14': 'Asociación pro Hospital Nacional de Geriatría y Gerontología Dr. Raúl Blanco Cervantes, APRONAGE.', '61': 'Asociación Sarchiseña de Discapacitados, ASADIS', '19': 'Chupis Ortopédica', '47': 'Municipalidad de Cartago.', '67': 'Asociación de Transparencia.', '5': 'Ortopédica Garbanzo', '28': 'Asociación Guanacasteca de Discapacidad, Autonomía y Comunidad Inclusiva, AGUDACI.', '13': 'AZMONT S.A', '56': 'Asociación para la Promoción de la Salud Mental, APROSAM.', '77': 'Asociación Costarricense de Personas con Discapacidad Visual, ACOPEDIV', '52': 'Asociación para la Atención Integral de Personas Adultas con Discapacidad “El sol Brilla para Todos” CAIPAD', '1': 'Synapsis Medical, Tienda Ortopédica Y Equipo Medico', '21': 'Hospital del Trauma del INS y sus clínicas alrededor del país.', '72': 'Asociación Costarricense Pro- Ayuda al Epiléptico, ACOPE.', '55': 'Asociación Taller de Atención Integral y Capacitación, ATAICA.', '9': 'Empresa Brailler Inc. Costa Rica', '27': 'Asociación de Personas con Discapacidad -APEDI- GUANACASTE', '49': 'Asociación Pro niños con Parálisis Cerebral Cartago', '66': 'Asociación Pro-Personas con Discapacidad de Atenas -APRODISA-', '48': 'Asociación Costarricense de Artriticos', '73': 'Fundación Hogar Manos Abiertas.', '4': 'Asociación Costarricense de Distrofia Muscular, ACODIM.', '71': 'Centro de Terapia Asistida con Animales.', '69': 'Asociación Talita Cumi.', '42': 'Instituto Tecnológico de Costa Rica', '2': 'Asociación Central Pro-Ayuda de la Persona con Discapacidad de Palmares - APRADIS', '29': 'Hospital La Anexión - CCSS', '8': 'TifloproductosCR', '54': 'Asociación de Personas con Discapacidad de Upala, ADEDISUPA.', '43': 'Clínica Fisiosport', '23': 'Hospital Express', '26': 'Centro de Terapia de Lenguaje y Guarderia Semillitas de Dios', '58': 'Fundación Amor y Esperanza.', '33': 'Hospital William Allen Taylor - CCSS', '44': 'Asociación Seres de Luz', '30': 'Fundación Senderos de Oportunidades', '22': 'Equipo Médico Montes Oca', '38': 'Hospital Nacional Psiquiátrico - CCSS Roberto Chacón Paut', '20': 'Asociación Pro Centro Nacional de Rehabilitación, PROCENARE', '68': 'Municipalidad de San Carlos.', '3': 'Alquiler Médicos ByB', '45': 'Colegio Universitario de Cartago -CUC', '50': 'Asociación de Desarrollo Educativo de Paraíso -ASODEPA-', '35': 'Asociación de Apoyo a la Unidad de Rehabilitación Profesional de Turrialba.'}
    needle = str(get_org_name_service(text))

    if needle == "Hospital William Allen Taylor- CCSS":
        needle = "Hospital William Allen Taylor - CCSS"

    if needle == "Hospital William Allen Taylor, CCSS":
        needle = "Hospital William Allen Taylor - CCSS"

    if needle == "Chupis Ortopedica":
        needle = "Chupis Ortopédica"

    if needle == "Hospital San Rafael de Alajuela- CCSS":
        needle = "Hospital San Rafael de Alajuela - CCSS"

    if needle == "No brinda información":
        needle = "Clinicas Audición"

    for key , value in names.items():
        value = str(value)
        if value == needle:
            print("\t\033[94morganizationsIdFk:\033[0m " + key)
            return key

    print("\t\u001B[31morganizationsIdFk:\033[0m ERROR")
    return 100


# ------------------------------------ORGANIZATIONS------------------------------------ #

def get_org_name_product(text):
    start = "Nombre del ente que brinda el producto de apoyo (institución, municipalidad, empresa u organización no gubernamental):"
    end = "4. Descripción del ente que brinda el producto de apoyo"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mname:\033[0m " + needle)
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        if needle == "" or needle == " " or needle == "\n" or needle == " \n":
            print("\t\u001B[31mname:\033[0m No brinda información")
            return "No brinda información"
        else:
            return needle

    else:
        print("\t\u001B[31mname:\033[0m No brinda información")
        return "No brinda información"


def get_org_email_product(text):
    start = "Dirección de correo electrónico:"
    end = "Web del servicio:"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        if needle.replace(" " , "") == "":
            print("\t\u001B[31memail:\033[0m No brinda información")
            return "No brinda información"
        else:
            print("\t\033[94memail:\033[0m " + needle)
            needle = needle.replace("\"", "")
            return needle

    else:
        print("\t\u001B[31memail:\033[0m No brinda información")
        return "No brinda información"


def get_org_web_product(text):
    start = "Web del servicio:"
    end = "Redes sociales:"
    if text.find(start) != -1 and  text.find(start) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mweb:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mweb:\033[0m No brinda información")
        return "No brinda información"


def get_org_telephone_product(text):
    start = " telelelelele "
    end = "Dirección de correo electrónico:"
    if text.find(start) != -1 and text.find(end):
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle[:needle.find("Fax")]
        rawphones = re.findall('\d+', needle)
        fixedphones = []
        for i in range(len(rawphones)):
            if i%2 != 0 and i != 0:
                fixedphones += [str(rawphones[i-1]) + "-" + str(rawphones[i])]
        needle = ""
        for i in fixedphones:
            needle += " " + i
        print("\t\033[94mtelephone:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mtelephone:\033[0m No brinda información")
        return "No brinda información"


def get_org_socialNetworks_product(text):
    start = "Redes sociales:"
    end = "Dirección waze:"
    if text.find(start) and text.find(end):
        needle = text[text.find(start) + len(start): text.find(end)]
        urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
        needle = needle.lower()
        domains = ["facebook", "twitter", "instagram", "linkedin", "youtube"]
        dict = {}
        for name in domains:
            if needle.find(name) != -1:
                new = {name: ""}
                for url in urls:
                    if url.find(name):
                        new[name] = url
                dict.update(new)
        print("\t\033[94msocialnetworks:\033[0m " + str(dict))
        return dict

    else:
        print("\t\u001B[31msocialNetworks:\033[0m No brinda información")
        return "No brinda información"


def get_org_wazeAddress_product(text):
    start = "Dirección waze:"
    end = "Ubicación"
    if text.find(start) != -1 and find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
        print("\t\033[94mwazeAddress:\033[0m " + str(urls))
        return urls

    else:
        print("\t\u001B[31mwazeAddress:\033[0m No brinda información")
        return "No brinda información"


def get_org_reaches_product(text):
    start = "Fines:"
    end = "Misión:"
    if text.find(start) != -1 and  find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        print("\t\033[94mreaches:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mreaches:\033[0m No brinda información")
        return "No brinda información"


def get_org_mision_product(text):
    start = "Misión:"
    end = " Visión: "
    if text.find(start) != -1 and text.find(start) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mmision:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mwazeAddress:\033[0m No brinda información")
        return "No brinda información"


def get_org_vision_product(text):
    start = " Visión: "
    end = "Objetivos:"
    if text.find(end) == -1:
        end = "Señale el tipo"
    if text.find(start) != -1 and find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        print("\t\033[94mvision:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mvision:\033[0m No brinda información")
        return "No brinda información"


def get_org_objective_product(text):
    start = " Objetivos: "
    end = " Señale el tipo de oferente del servicio de apoyo"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mobjective:\033[0m " + needle)
        needle = needle.replace("5." , "")
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mproduct:\033[0m No brinda información")
        return "No brinda información"


# TODO: Generate json version of data.
def get_org_dayOperations_product(text):
    start = "de la semana que atienden para la obtención de productos de apoyo. "
    end = "Forma de atención:"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mdayOperations:\033[0m " + needle)
        needle = needle.replace("13.", "")
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mdayOperations:\033[0m No brinda información")
        return "No brinda información"


def get_org_typesidPk_product(text):
    start = "Es Institución Pública: ("
    mid = ") Municipalidad ("
    mid1 = ") Es Empresa Privada: ("
    mid2 = ") Es Organización no Gubernamental: ("
    end = ") Nombre del producto de apoyo"
    needle1 = text[text.find(start) + len(start): text.find(mid)]
    needle2 = text[text.find(mid) + len(mid): text.find(mid1)]
    needle3 = text[text.find(mid1) + len(mid1): text.find(mid2)]
    needle4 = text[text.find(mid2) + len(mid2): text.find(end)]

    if(needle1.replace(" " , "") == "x" or needle1.replace(" " , "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 3")
        return 3

    elif(needle2.replace(" " , "") == "x" or needle2.replace(" " , "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 2")
        return 2

    elif (needle3.replace(" ", "") == "x" or needle3.replace(" ", "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 4")
        return 4

    elif (needle4.replace(" ", "") == "x" or needle4.replace(" ", "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 1")
        return 1

    else:
        print("\t\u001B[31mtypesidPk:\033[0m 5")
        return 5


def get_org_name_service(text):
    start = "Nombre del ente que brinda el producto de apoyo (institución, municipalidad, empresa u organización no gubernamental): "
    end = "4. Descripción del ente que brinda el producto de apoyo"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\"", "")
        if needle == "" or needle == " " or needle == "\n" or needle == " \n":
            print("\t\u001B[31mname:\033[0m No brinda información")
            return "No brinda información"
        else:
            print("\t\033[94mname:\033[0m " + needle)
            return needle

    else:
        print("\t\u001B[31mname:\033[0m No brinda información")
        return "No brinda información"


def get_org_email_service(text):
    start = "Dirección de correo electrónico:"
    end = "Web del servicio:"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        if needle.replace(" " , "") == "":
            print("\t\u001B[31memail:\033[0m No brinda información")
            return "No brinda información"
        else:
            print("\t\033[94memail:\033[0m " + needle)
            needle = needle.replace("\"", "")
            return needle

    else:
        print("\t\u001B[31memail:\033[0m No brinda información")
        return "No brinda información"


def get_org_web_service(text):
    start = "Web del servicio:"
    end = "Redes sociales:"
    if text.find(start) != -1 and text.find(start) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        if needle.replace(" " , "") == "":
            print("\t\u001B[31mweb:\033[0m No brinda información")
            return "No brinda información"
        else:
            print("\t\033[94mweb:\033[0m " + needle)
            needle = needle.replace("\"", "")
            return needle

    else:
        print("\t\u001B[31mweb:\033[0m No brinda información")
        return "No brinda información"


def get_org_telephone_service(text):
    start = " telelelelele "
    end = "Dirección de correo electrónico:"
    if text.find(start) != -1 and text.find(end):
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle[:needle.find("Fax")]
        rawphones = re.findall('\d+', needle)
        fixedphones = []
        for i in range(len(rawphones)):
            if i % 2 != 0 and i != 0:
                fixedphones += [str(rawphones[i - 1]) + "-" + str(rawphones[i])]
        needle = ""
        for i in fixedphones:
            needle += " " + i
        if needle == " 24011200-3 7-4 7-29 0-7 9-10 3433966-84 4496942-14 4-8 1-2 2-1 1-3 4-1 0-8 065-2 63-393 0-9 88412257-8 2-3 10-3433966 4-84 4321847-8 10-7 00-4 00-7 00-3 00-10 12-13 14-15 24-7 7-4 7-3 24-7 16-17":
            print("\t\033[94mtelephone:\033[0m 24011200")
            return "24011200"

        elif needle == " 24361001-3 7-4 7-29 0-7 9-10 008242-84 2287576-14 4-8 1-2 2-1 1-3 4-1 0-8 0-9 41516823-0 10-9 11431-8093 8-2 3-10 008242-4 84-2112481 8-10 7-00 4-00 7-00 3-00 10-12 13-14 15-24 7-7 4-7 3-24 7-16 17-18":
            print("\t\033[94mtelephone:\033[0m 24361001")
            return "24361001"

        elif needle == " 2556-05":
            print("\t\033[94mtelephone:\033[0m 2556-0516")
            return "2556-0516"

        elif needle == " 25581300-25561663 25568328-25560973 25581424-3 7-4 7-29 0-7 9-9 9039907-83 688387-16 4-4 5-3 4-1 0-8 0-69 24894-81 0-3 21009-50 9-8 2-3 9-903521 4-83 6861983-8 10-7 00-4 00-7 00-3 00-10 12-13 14-15 24-7 7-4 7-3 24-7 16-17":
            print("\t\033[94mtelephone:\033[0m 25581300")
            return "25581300"

        elif needle == " 26858400-26858404 26858468-26858417 3-7 4-7 29-0 7-9 10-1484271 85-4561904 17-3 1-4 1-4 5-3 4-1 0-8 9-748 49-07 0-92 136-16202219 8-2 3-10 1484218-4 85-4539963 8-10 7-00 4-00 7-00 3-00 10-12 13-14 15-24 7-7 4-7 3-24 7-16 17-18":
            print("\t\033[94mtelephone:\033[0m 26858400")
            return "26858400"

        else:
            print("\t\033[94mtelephone:\033[0m " + needle)
            needle = needle.replace("\"", "")
            return needle

    else:
        print("\t\u001B[31mtelephone:\033[0m No brinda información")
        return "No brinda información"


def get_org_socialNetworks_service(text):
    start = "Redes sociales:"
    end = "Dirección waze:"
    if text.find(start) and text.find(end):
        needle = text[text.find(start) + len(start): text.find(end)]
        urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
        needle = needle.lower()
        domains = ["facebook", "twitter", "instagram", "linkedin", "youtube"]
        dict = {}
        for name in domains:
            if needle.find(name) != -1:
                new = {name: ""}
                for url in urls:
                    if url.find(name):
                        new[name] = url
                dict.update(new)
        print("\t\033[94msocialnetworks:\033[0m " + str(dict))
        return dict

    else:
        print("\t\u001B[31msocialNetworks:\033[0m No brinda información")
        return "No brinda información"


def get_org_wazeAddress_service(text):
    start = "Dirección waze:"
    end = "Ubicación"
    if text.find(start) != -1 and find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
        print("\t\033[94mwazeAddress:\033[0m " + str(urls))
        return urls

    else:
        print("\t\u001B[31mwazeAddress:\033[0m No brinda información")
        return "No brinda información"


def get_org_reaches_service(text):
    haystack = text[text.find("Descripción del ente que brinda el producto de apoyo:"): text.find("oferente del servicio de apoyo")]

    start = "Fines:"
    end = "Misión:"
    if haystack.find(start) != -1 and haystack.find(end) != -1:
        needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
        if needle == "":
            start = "Descripción del ente que brinda el producto de apoyo:"
            end = "Uso y aplicaciones del producto de apoyo"
            haystack = text[text.find(start) : text.find(end)]
            needle = haystack[haystack.find("Fines: ") : haystack.find("Misión:")]

        print("\t\033[94mreaches:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mreaches:\033[0m No brinda información")
        return "No brinda información"


def get_org_mision_service(text):
    haystack = text[text.find("Descripción del ente que brinda el producto de apoyo:"): text.find("oferente del servicio de apoyo")]

    start = "Misión:"
    end = " Visión: "

    if haystack.find(start) != -1 and haystack.find(start) != -1:
        needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
        print("\t\033[94mmision:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mwazeAddress:\033[0m No brinda información")
        return "No brinda información"


def get_org_vision_service(text):
    haystack = text[text.find("Descripción del ente que brinda el producto de apoyo:"): text.find("oferente del servicio de apoyo")]
    start = " Visión: "
    end = "Objetivos:"
    if haystack.find(end) == -1:
        end = "Señale el tipo"
    if haystack.find(start) != -1 and find_nth(haystack, end, 1) != -1:
        needle = haystack[haystack.find(start) + len(start): find_nth(haystack, end, 1)]
        print("\t\033[94mvision:\033[0m " + needle)
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mvision:\033[0m No brinda información")
        return "No brinda información"


def get_org_objective_service(text):
    haystack = text[text.find("Descripción del ente que brinda el producto de apoyo:") : text.find("oferente del servicio de apoyo")]
    haystack.replace(" Objetivo: " , " Objetivos: ")
    start = "Objetivos:"
    end = " Señale el tipo de"


    if haystack.find(start) != -1 and haystack.find(end) != -1:
        needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
        print("\t\033[94mobjective:\033[0m " + needle)
        needle = needle.replace("5." , "")
        needle.replace("Señale el tipo de" , "")
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mobjective:\033[0m No brinda información")
        return "No brinda información"


def get_org_dayOperations_service(text):
    start = "Horario (días por semana que está disponible)."
    end = "Otra información de interés ("
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mdayOperations:\033[0m " + needle)
        needle = needle.replace("13.", "")
        needle = needle.replace("\"", "")
        return needle

    else:
        print("\t\u001B[31mdayOperations:\033[0m No brinda información")
        return "No brinda información"


def get_org_typesidPk_service(text):
    start = "Es Institución Pública: ("
    mid = ") Municipalidad ("
    mid1 = ") Es Empresa Privada: ("
    mid2 = ") Es Organización no Gubernamental: ("
    end = ") Nombre del producto de apoyo"
    needle1 = text[text.find(start) + len(start): text.find(mid)]
    needle2 = text[text.find(mid) + len(mid): text.find(mid1)]
    needle3 = text[text.find(mid1) + len(mid1): text.find(mid2)]
    needle4 = text[text.find(mid2) + len(mid2): text.find(end)]

    if(needle1.replace(" " , "") == "x" or needle1.replace(" " , "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 3")
        return 3

    elif(needle2.replace(" " , "") == "x" or needle2.replace(" " , "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 2")
        return 2

    elif (needle3.replace(" ", "") == "x" or needle3.replace(" ", "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 4")
        return 4

    elif (needle4.replace(" ", "") == "x" or needle4.replace(" ", "") == "X"):
        print("\t\033[94mtypesidPk:\033[0m 1")
        return 1

    else:
        print("\t\u001B[31mtypesidPk:\033[0m 5")
        return 5

# ------------------------------------SERVICES------------------------------------ #

def get_service_isPrivate(text):
    haystack = text[text.find(" privado y el costo del mismo en t") : text.find("Descripción del servicio")]
    start = "Servicio público ("
    end = ") Servicio privado ("
    needle = haystack[haystack.find(start) + len(start) : haystack.find(end)]
    if needle.replace(" " , "") == "X" or needle.replace(" " , "") == "x":
        print("\t\033[94misPrivate:\033[0m 0")
        return 0
    else:
        print("\t\033[94misPrivate:\033[0m 1")
        return 1


def get_service_cost(text):
    haystack = text[text.find("Costo: Indique si es un ") : text.find("Descripción del servicio")]
    start = ") Costo del servicio: "
    end = "Tiempo/costo:"
    needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mcost:\033[0m " + needle)
    return needle


def get_service_objectives(text):
    haystack = text[text.find("Descripción del servicio") : text.find("Información sobre la persona encargada")]
    start = "Objetivos: "
    end = " Apoyos específicos que brinda: "
    needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mobjectives:\033[0m " + needle)
    return needle


def get_service_reaches(text):
    haystack = text[text.find("Descripción del servicio"): text.find("Información sobre la persona encargada")]
    start = "Descripción del servicio: Fines: "
    end = " Objetivos: "
    needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mreaches:\033[0m " + needle)
    return needle


def get_service_specificSupports(text):
    haystack = text[text.find("Descripción del servicio") : text.find("Información sobre la persona encargada y/o")]
    start = "Apoyos específicos que brinda: "
    end = " Tipo de apoyo"
    needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mspecificSupports:\033[0m " + needle)
    return needle


def get_service_typeSupports(text):
    start = "Tipo de apoyos: Individuales: ("
    mid = ") grupales: ("
    end = ") Disponibilidad:"
    needle1 = text[text.find(start) + len(start): text.find(mid)]
    needle2 = text[text.find(mid) + len(mid): text.find(end)]
    needle1 = needle1.replace(" " , "")
    needle2 = needle2.replace(" " , "")
    if needle1 == "x" or needle1 == "X":
        if needle2 == "x" or needle2 == "X":
            print("\t\033[94mtypeSupports:\033[0m Individuales y grupales")
            return "Individuales y grupales"
        print("\t\033[94mtypeSupports:\033[0m Individuales")
        return "Individuales"
    elif needle2 == "x" or needle2 == "X":
        print("\t\033[94mtypeSupports:\033[0m Grupales")
        return "Grupales"
    else:
        print("\t\033[94mtypeSupports:\033[0m No brinda información.")
        return "No brinda información."


def get_service_daysToOperations(text):
    start = ") Disponibilidad: "
    end = "Otra información de interés (describa si son actividades, programas o proyectos u otros)"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mdaysToOperations:\033[0m " + needle)
    return needle


def get_service_responsabilityPerson(text):
    start = "Información sobre la persona encargada y/o el equipo de trabajo que brinda el servicio de apoyo (refiérase a ocupación del personal responsable, formación académica, experiencia reconocida, destrezas adicionales y otros de interés):"
    end = "12. Cobertura del servicio de apoyo:"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mresponsabilityPerson:\033[0m " + needle)
    return needle


def get_service_cover(text):
    haystack = text[text.find("Cobertura del servicio de apoyo") : text.find("Condiciones para acceder al servicio")]
    start = "Cobertura del servicio de apoyo: Nacional: ("
    mid1 = ") Provincias (si no es cobertura nacional), describir las provincias: "
    mid2 = " Cantones (describir qué cantones cubre el servicio de apoyo): "
    end = " Se brinda de manera telef"
    needle1 = haystack[haystack.find(start) + len(start): haystack.find(mid1)]
    needle2 = haystack[haystack.find(mid1) + len(mid1): haystack.find(mid2)]
    needle3 = haystack[haystack.find(mid2) + len(mid2): haystack.find(end)]

    if needle1.replace(" " , "") == "x" or needle1.replace(" " , "") == "X":
        print("\t\033[94mcover:\033[0m Nacional")
        return "Nacional"

    if needle2 != "":
        if needle3 != "":
            print("\t\033[94mcover: Provincias: " + needle2 + " Cantones: " + needle3)
            return "Provincias: " + needle2 + " Cantones: " + needle3
        print("\t\033[94mcover:\033[0m " + needle2)
        return needle2

    if needle3 != "" and len(needle3) < 50:
        print("\t\033[94mcover:\033[0m " + needle3)
        return needle3
    else:
        print("\t\033[94mtypeSupports:\033[0m No brinda información.")
        return "No brinda información."


def get_service_requirements(text):
    start = "Condiciones para acceder al servicio: Especifique los requisitos que se requieren para acceder al servicio. "
    end = " 14. Perfil de la persona usuaria:"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mrequirements:\033[0m " + needle)
    return needle


def get_service_accesibility(text):
    start = "17. Accesibilidad: Mencione si el servicio de atención reúne condiciones de accesibilidad según la normativa vigente. "
    end = "18. Observaciones:"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94maccesibility:\033[0m " + needle)
    return needle


def get_service_others(text):
    start = "Observaciones: Indique aquí información que considere importante, detalle características del servicio que no queden reflejadas en los ítems anteriores."
    end = "Para uso interno"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")
    print("\t\033[94mothers:\033[0m " + needle)
    return needle


def get_service_scheduleExtraoerdinary(text):
    start = "Tienen otras formas de brindar el servicio, fuera del horario? Si ("
    end = ") No ("
    needle = text[text.find(start) + len(start): find_nth(text , end , 4)]
    if needle.replace(" ", "") == "x" or needle.replace(" ", "") == "X":
        print("\t\033[94mscheduleExtraoerdinary:\033[0m 1")
        return 1
    else:
        print("\t\033[94mscheduleExtraoerdinary:\033[0m 0")
        return 0


def get_service_otherExtraordinaryAttention(text):
    start = "En caso de brindar el servicio fuera de horario, describa ¿cuáles son esas formas de atención?: página web ("
    mid = ") redes sociales ("
    mid1 = ") correo electrónico ("
    mid2 = ") servicio al cliente 24/7 ("
    end = ") Otros: ( "
    needle = text[text.find(start) + len(start): text.find(mid)]
    needle1 = text[text.find(mid) + len(mid): text.find(mid1)]
    needle2 = text[text.find(mid1) + len(mid1): text.find(mid2)]
    needle3 = text[text.find(mid2) + len(mid2): text.find(end)]

    result = "-"

    if needle.replace(" ", "") == "x" or needle.replace(" ", "") == "X":
        result += "Página web"
    if needle1.replace(" ", "") == "x" or needle1.replace(" ", "") == "X":
        result += " Redes Sociales"
    if needle2.replace(" ", "") == "x" or needle2.replace(" ", "") == "X":
        result += " Correo Electronico"
    if needle3.replace(" ", "") == "x" or needle3.replace(" ", "") == "X":
        result += " Servicio 24/7"

    if result == "-":
        result = "No brinda información"

    print("\t\033[94motherExtraordinaryAttention:\033[0m " + result)
    return result


def get_service_attentionFrecuency(text):
    start = "Frecuencia de atención (indicar con qué frecuencia la misma persona usuaria puede ser apoyada de forma regular por el servicio): diario: ("
    mid = ") semanal: ("
    mid1 = ") quincenal: ("
    end = ") 17. Accesibilidad"
    needle = text[text.find(start) + len(start): text.find(mid)]
    needle1 = text[text.find(mid) + len(mid): text.find(mid1)]
    needle2 = text[text.find(mid1) + len(mid1): text.find(end)]

    result = "-"

    if needle.replace(" ", "") == "x" or needle.replace(" ", "") == "X":
        result += "Diario"
    if needle1.replace(" ", "") == "x" or needle1.replace(" ", "") == "X":
        result += " Semanal"
    if needle2.replace(" ", "") == "x" or needle2.replace(" ", "") == "X":
        result += " Quincenal"

    print("\t\033[94mattentionFrecuency:\033[0m " + result)
    return result




# ------------------------------------TESTING------------------------------------ #

def test_service_functions(text):
    # idPk += 1
    get_service_isPrivate(text)
    get_service_cost(text)
    get_service_objectives(text)
    get_service_reaches(text)
    get_service_specificSupports(text)
    get_service_typeSupports(text)
    # get_service_daysToOperations(text)
    get_service_responsabilityPerson(text)
    get_service_cover(text)
    get_service_requirements(text)
    get_service_accesibility(text)
    get_service_others(text)
    get_service_scheduleExtraoerdinary(text)
    get_service_otherExtraordinaryAttention(text)
    get_service_attentionFrecuency(text)
    # item idFk


def test_service(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_service_functions(get_text_from(fileMatrx[i][0] , False))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_product_functions(text):
    # idPk += 1
    get_product_cost(text)
    get_product_warranty(text)
    get_product_instock(text)
    get_product_timeDelivery(text)
    get_product_warrantyImported(text)
    get_product_usefulLife(text)
    # spareParts = "-"
    get_product_primaryFuncionalities(text)
    # secondlyFuncionalities "-"
    get_product_brand(text)
    # model = "-"
    # height = "-"
    # width = "-"
    # deep = "-"
    # weight - "-"


def test_product(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_product_functions(get_text_from(fileMatrx[i][0] , True))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_item_product_functions(text):
    # idPk += 1
    # code = 0
    get_item_name(text)
    get_item_description_products(text)
    get_item_observations_products(text)
    # image1
    # image2
    # image3
    # visibility = 1
    # isProduct = 1
    get_date()  # onDateUpdated
    get_date()  # onDateCreated
    get_date()  # daysToOperations
    get_item_typeDeficiency(text)
    get_item_age(text)
    get_item_sex(text)
    # isForPregnant = "-"
    # isAproved = 1
    # isChecked = 1
    # isDeleted = 0
    get_item_organizationidPk_service(text)

def test_item_service_functions(text):
    # idPk += 1
    # code = 0
    get_item_name(text)
    get_item_description_service(text)
    get_item_observations_services(text)
    # image1
    # image2
    # image3
    # visibility = 1
    # isProduct = 1
    get_date()  # onDateUpdated
    get_date()  # onDateCreated
    get_date()  # daysToOperations
    get_item_typeDeficiency(text)
    get_item_age(text)
    get_item_sex(text)
    # isForPregnant = "-"
    # isAproved = 1
    # isChecked = 1
    # isDeleted = 0
    get_item_organizationidPk_service(text)


def test_item_product(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_item_product_functions(get_text_from(fileMatrx[i][0] , False))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_item_service(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_item_service_functions(get_text_from(fileMatrx[i][0] , False))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_org_product_functions(text):
    # idPk += 1
    # dni = 0
    get_org_name_product(text)
    get_org_email_product(text)
    get_org_web_product(text)
    get_org_telephone_product(text)
    # legalRepresentative = No brindaron informacion
    # assembly = []
    get_org_socialNetworks_product(text)
    get_org_wazeAddress_product(text)
    # shedule = "-"
    get_org_reaches_product(text)
    get_org_mision_product(text)
    get_org_vision_product(text)
    get_org_objective_product(text)
    get_org_dayOperations_product(text)
    # isApproved = 1
    # isChecked = 1
    # isDeleted = 0
    get_org_typesidPk_product(text)


def test_org_product(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_org_product_functions(get_text_from(fileMatrx[i][0] , True))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_org_service_functions(text):
    # idPk += 1
    # dni = 0
    get_org_name_service(text)
    get_org_email_service(text)
    get_org_web_service(text)
    get_org_telephone_service(text)
    # legalRepresentative = No brindaron informacion
    # assembly = []
    get_org_socialNetworks_service(text)
    get_org_wazeAddress_service(text)
    # shedule = "-"
    get_org_reaches_service(text)
    get_org_mision_service(text)
    get_org_vision_service(text)
    get_org_objective_service(text)
    get_org_dayOperations_service(text)
    # isApproved = 1
    # isChecked = 1
    # isDeleted = 0
    get_org_typesidPk_service(text)


def test_org_service(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_org_service_functions(get_text_from(fileMatrx[i][0] , False))
        print("_____________________________________________________________________________________________________________________")
        print("")

# ------------------------------------BUILDING------------------------------------ #

def generate_Organizations_dictionary(productMatrix , serviceMatrix):
    Organizations = []
    c = 1
    org_ready = []

    for row in productMatrix:
        temp = {}
        path = row[0]
        text = get_text_from(path , False)
        if get_org_name_product(text) not in org_ready:
            print(path)
            org_ready.append(get_org_name_product(text))
            temp["idPk"] = c
            temp["dni"] = ">>No brinda información>>"
            temp["name"] = ">>" + get_org_name_product(text) + ">>"
            temp["email"] = ">>" + get_org_email_product(text) + ">>"
            temp["web"] = ">>" + get_org_web_product(text) + ">>"
            temp["telephone"] = ">>" + get_org_telephone_product(text) + ">>"
            temp["legalRepresentative"] = ">>No brinda información>>"
            temp["assembly"] = []
            temp["socialNetworks"] = get_org_socialNetworks_product(text)
            temp["wazeAddress"] = get_org_wazeAddress_product(text)
            temp["schedule"] = ">>n>>"
            temp["reaches"] = ">>" + get_org_reaches_product(text) + ">>"
            temp["mision"] = ">>" + get_org_mision_product(text) + ">>"
            temp["vision"] = ">>" + get_org_vision_product(text) + ">>"
            temp["objetive"] = ">>" + get_org_objective_product(text) + ">>"
            temp["dayOperations"] = {}
            temp["isAproved"] = 1
            temp["isChecked"] = 1
            temp["isDeleted"] = 0
            temp["organizationsTypesidPk"] = get_org_typesidPk_product(text)
            c += 1

            Organizations.append(copy.deepcopy(temp))

    for row in serviceMatrix:
        temp = {}
        path = row[0]
        text = get_text_from(path, False)
        if get_org_name_service(text) not in org_ready:
            print(path)
            org_ready.append(get_org_name_service(text))
            temp["idPk"] = c
            temp["dni"] = ">>No brinda información>>"
            temp["name"] = ">>" + get_org_name_service(text) + ">>"
            temp["email"] = ">>" + get_org_email_service(text) + ">>"
            temp["web"] = ">>" + get_org_web_service(text) + ">>"
            temp["telephone"] = ">>" + get_org_telephone_service(text) + ">>"
            temp["legalRepresentative"] = ">>No brinda información>>"
            temp["assembly"] = []
            temp["socialNetworks"] = get_org_socialNetworks_service(text)
            temp["wazeAddress"] = get_org_wazeAddress_service(text)
            temp["schedule"] = ">>n>>"
            temp["reaches"] = ">>" + get_org_reaches_service(text) + ">>"
            temp["mision"] = ">>" + get_org_mision_service(text) + ">>"
            temp["vision"] = ">>" + get_org_vision_service(text) + ">>"
            temp["objetive"] = ">>" + get_org_objective_service(text) + ">>"
            temp["dayOperations"] = {}
            temp["isAproved"] = 1
            temp["isChecked"] = 1
            temp["isDeleted"] = 0
            temp["organizationsTypesidPk"] = get_org_typesidPk_service(text)
            c += 1

            Organizations.append(copy.deepcopy(temp))

    return Organizations


def generate_Items_Services_and_Products_dictionary(productMatrix, serviceMatrix):
    Items = []
    Services = []
    Products = []
    i = 1
    ready = []

    for row in serviceMatrix:
        temp = {}
        path = row[0]
        try:
            image = row[1]
        except:
            image = "/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png"
        text = get_text_from(path , False)
        if get_item_name(text) not in ready:
            print(path)
            ready.append(get_item_name(text))
            temp["idPk"] = i
            temp["code"] = ">>No brinda información>>"
            temp["name"] = ">>" + get_item_name(text) + ">>"
            temp["description"] = ">>" + get_item_description_service(text) + ">>"
            temp["observations"] = ">>" + get_item_observations_services(text) + ">>"
            temp["image1"] = encode_image("/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png")
            temp["image2"] = ">>imagen>>"
            temp["image3"] = ">>imagen>>"
            temp["visibility"] = 1
            temp["isProduct"] = 0
            temp["onDateUpdated"] = get_date()
            temp["onDateCreated"] = get_date()
            temp["daysToOperations"] = {}
            temp["typeDeficiency"] = ">>" + get_item_typeDeficiency(text) + ">>"
            temp["age"] = get_item_age(text)
            temp["sex"] = 2
            temp["isForPregnant"] = 1
            temp["isApproved"] = 1
            temp["isChecked"] = 1
            temp["isDeleted"] = 0
            temp["organizationsIdFk"] = get_item_organizationidPk_service(text)
            i += 1

            Items.append(copy.deepcopy(temp))

    return Items


def generate_Products_dictionary(productMatrix, serviceMatrix):
    Products = []
    i = 1
    ready = []

    for row in productMatrix:
        temp = {}
        path = row[0]
        text = get_text_from(path , False)
        if get_item_name(text) not in ready:
            print(path)
            ready.append(get_item_name(text))
            temp["idPk"] = i
            temp["cost"] = get_product_cost(text)
            temp["warranty"] = ">>No brinda información>>"
            temp["inStock"] = get_product_instock(text)
            temp["timeDelevery"] = ">>" + get_product_timeDelivery(text) + ">>"
            temp["warrantyImported"] = ">>No brinda información>>"
            temp["usefulLife"] = get_product_usefulLife(text)
            temp["spareParts"] = ">>No brinda información>>"
            temp["primaryFunctionalities"] = get_product_primaryFuncionalities(text)
            temp["secondlyFunctionalities"] = ">>No brinda información>>"
            temp["brand"] = get_product_brand(text)
            temp["model"] = ">>No brinda información>>"
            temp["height"] = ">>No brinda información>>"
            temp["width"] = ">>No brinda información>>"
            temp["deep"] = ">>No brinda información>>"
            temp["weight"] = ">>No brinda información>>"
            temp["Items_idPk"] = 1
            i += 1

            Products.append(copy.deepcopy(temp))

    return Products


def generate_Services_dictionary(productMatrix, serviceMatrix):
    Services = []
    i = 1
    ready = []

    for row in serviceMatrix:
        temp = {}
        path = row[0]
        text = get_text_from(path , False)
        if get_item_name(text) not in ready:
            print(path)
            ready.append(get_item_name(text))
            temp["idPk"] = i
            temp["isPrivate"] = get_service_isPrivate(text)
            temp["cost"] =  ">>" + get_service_cost(text) + ">>"
            temp["objectives"] = ">>" + get_service_objectives(text) + ">>"
            temp["reaches"] = ">>" + get_service_reaches(text) + ">>"
            temp["specificSupports"] = ">>" + get_service_specificSupports(text)  + ">>"
            temp["typeSupports"] = ">>" + get_service_typeSupports(text) + ">>"
            temp["daysToOperations"] = {}
            temp["responsabilityPerson"] = ">>" + get_service_responsabilityPerson(text) + ">>"
            temp["cover"] = ">>" + get_service_cover(text) + ">>"
            temp["requirements"] = ">>" + get_service_requirements(text) + ">>"
            temp["accesibility"] = ">>" + get_service_accesibility(text) + ">>"
            temp["others"] = ">>" + get_service_others(text) + ">>"
            temp["scheduleExtraordinary"] = get_service_scheduleExtraoerdinary(text)
            temp["otherExtraordinaryAttention"] = ">>" + get_service_otherExtraordinaryAttention(text) + ">>"
            temp["attentionFrecuency"] = ">>" + get_service_attentionFrecuency(text) + ">>"
            temp["Items_idPk"] = 1
            i += 1

            Services.append(copy.deepcopy(temp))

    return Services


def dic2csv_orgs(dictionaries):
    cols_name = ["idPk", "dni" , "name" , "email" , "web" , "telephone" , "legalRepresentative" , "assembly" , "socialNetworks" , "wazeAddress" , "schedule" , "reaches" , "mision" , "vision" , "objetive" , "dayOperations" ,"isAproved" , "isChecked" , "isDeleted" , "organizationsTypesidPk"]
    file = open("toExport.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("toExport.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    new = new.replace("\" ;\"" , "\";\"")
    new = new.replace("\"; \"", "\";\"")
    new = new.replace("\" ; \"", "\";\"")
    new = new.replace("\"\";\"", "\";\"")
    new = new.replace("\";\"\"", "\";\"")
    file = open("toExport.csv", "w")
    file.write(new)
    file.close()

def dic2csv_items(dictionaries):
    cols_name = ["idPk" , "code" , "name" , "description" , "observations" , "image1" , "image2" , "image3" , "visibility" , "isProduct" , "onDateUpdated" , "onDateCreated" , "daysToOperations" , "typeDeficiency" , "age" , "sex" , "isForPregnant" , "isApproved" , "isChecked" , "isDeleted" , "organizationsIdFk"]
    file = open("toExport.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("toExport.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    new = new.replace("{'age': '" , "{\"'age'\": \"'")
    new = new.replace("'}" , "'\"}")
    file = open("toExport.csv", "w")
    file.write(new)
    file.close()



def dic2csv_products(dictionaries):
    cols_name = ["idPk", "cost", "warranty", "inStock", "timeDelevery", "warrantyImported", "usefulLife", "spareParts","primaryFunctionalities", "secondlyFunctionalities", "brand", "model", "height", "width", "deep", "weight","Items_idPk"]
    file = open("toExport.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("toExport.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    file = open("toExport.csv", "w")
    file.write(new)
    file.close()



def dic2csv_services(dictionaries):
    cols_name = ["idPk", "isPrivate", "cost", "objectives", "reaches", "specificSupports", "typeSupports", "daysToOperations",
     "responsabilityPerson", "cover", "requirements", "accesibility", "others", "scheduleExtraordinary",
     "otherExtraordinaryAttention", "attentionFrecuency", "Items_idPk"]
    file = open("toExport.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("toExport.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    file = open("toExport.csv", "w")
    file.write(new)
    file.close()


# ------------------------------------MAIN------------------------------------ #

def main():
    print("          _____          __  __    _______     _______ _______ ______ __  __ \n    /\   |  __ \   /\   |  \/  |  / ____\ \   / / ____|__   __|  ____|  \/  |\n   /  \  | |  | | /  \  | \  / | | (___  \ \_/ / (___    | |  | |__  | \  / |\n  / /\ \ | |  | |/ /\ \ | |\/| |  \___ \  \   / \___ \   | |  |  __| | |\/| |\n / ____ \| |__| / ____ \| |  | |  ____) |  | |  ____) |  | |  | |____| |  | |\n/_/    \_\_____/_/    \_\_|  |_| |_____/   |_| |_____/   |_|  |______|_|  |_|\n                    -Automatic Database Migration System-                    \n\n\n")
    serviceMatrix = get_files_from("/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Servicios de apoyo")
    productMatrix = get_files_from("/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Productos de apoyo/")

    #path = "/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Servicios de apoyo/Alajuela/ASOC PERSONAS CON DISCAPACIDAD UPALA/Centro Atención Integral/Asoc. PcD Upala - Centro Atención Integral.docx"
    #text = get_text_from(path , True)

    #print(text)

    dictionary = generate_Services_dictionary(productMatrix, serviceMatrix)
    dic2csv_services(dictionary)







if __name__ == "__main__":
    main()



















