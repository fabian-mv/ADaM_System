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
    start = "Tiempo de duración del trámite de importación"
    end = " La garantía es igual"
    if text.find(start) == -1:
        start = "Tiempo de duración del trámite de fabricación"
    needle = text[text.find(start) + len(start): text.find(end)]
    needle = needle.replace(": " , "")
    needle = needle.replace(":", "")
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
    needle.replace("\"" , "")
    needle.replace("\'", "")
    print("\t\033[94mprimaryFuncionalities:\033[0m " + needle)
    return needle


def get_product_brand(text):
    start = "Marca(s):"
    if text.find(start) == -1:
        start = "Marca (s):"

    if text.find(start) == -1:
        print("\t\033[94mbrand:\033[0m No brinda información")
        return "No brinda información."
    end = " Garantía:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mbrand:\033[0m " + needle)
    return needle


def get_date():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def get_product_orgIdFk(text):
    names = {'53': 'Alquiler Médicos ByB - Servicio Sanitario Portatil', '43': 'Casa Hogar Comunitario', '40': 'Servicio alquiler o préstamo de Camas Hospitalarias.', '3': 'Terapia de Lenguaje', '78': ': Psicología', '10': 'Alquiler sillas de ruedas.', '84': 'Servicios Educativos', '74': ': Artes Plásticas', '20': 'Servicio de audiología en general con fabricación de audífonos.', '54': 'Alquiler Médicos ByB - Silla Baño', '86': 'Centro Diurno de Atención Integral', '48': 'Serv. Capacitación', '82': 'Serv. Asesoría Legal', '26': 'Apoyos Didácticos', '44': 'Serv. Apoyo Emocional', '23': 'Terapia Física y Rehabilitación', '17': 'Nutrición', '36': 'Centro educativo - Educación especial curricular.', '80': 'Serv. Apoyo Económico', '33': 'Audiometría', '65': 'Artes Industriales', '49': 'Serv. Educación Especial', '55': 'Alquiler Médicos ByB - Andaderas', '14': 'Centro Atención Integral', '88': 'Ser. alquiler camas ortopedicas', '46': 'Centro de atención integral', '61': 'Terapia Física.', '66': 'Educación Musical', '63': 'Hogar de cuido para personas con parálisis cerebral en situación de abandono', '58': 'Alquiler Médicos ByB - Muletas', '70': 'Terapia de lenguaje', '87': 'Servicios ocupacionales.', '19': 'Odontología', '71': ': Terapia Física', '81': 'Taller Ebanistería', '1': 'Serv. Educativo: La biblioteca posee un programa, con cursos mejoramiento de motora fina, junto con la Trabajadora Social que busca mejorar la calidad de vida de la familia.', '16': 'Terapia ocupacional', '38': 'Servicio alquiler o préstamo de sillas ruedas no ortopedicas.', '75': ': Educación Física', '47': 'Terapia del lenguaje, habla y voz', '34': 'Serv. Apoyo Legal', '62': 'Educación Especial', '72': ': Estimulación Temprana', '35': 'Centro de Atención Integral', '57': 'Alquiler Médicos ByB - Sillas Ruedas', '59': 'Animales Equinoterapia - Animales Equinoterapia Costa Rica.', '50': 'Serv. Gestión y canalización de fondos para proyecto de bien social.', '89': 'Serv. Ocupacionales de Recreo', '22': 'Enseñanza de Lesco', '79': ': Educación Especial', '12': 'Audiometrías', '30': 'Presupuesto para apoyar ONG’S que atienden personas con discapacidad en el Cantón.', '64': 'Educación para el Hogar', '56': 'Alquiler Médicos ByB - Cama Hospitalaria', '9': 'Terapia Física', '73': ': Música', '77': ': Artes Industriales', '32': 'Serv. Educativos.', '25': 'Adecuación Curricular No Significativa', '51': 'Capacitaciones a personas, entidades privadas o públicas en el cantón.', '13': 'Serv. Educativos', '42': 'Serv. Terapia Ocupacional', '15': 'Capacitaciones', '18': 'Trabajo Social', '39': 'Serv. Alquiler de Andaderas', '6': 'Ortopédia.', '5': 'Asesoría técnica sobre petición de ayudas o procedimientos estatales.', '45': 'Serv. Equinoterapia', '85': 'Servicios educativos.', '52': 'Formación Humana', '11': 'Terapia Ocupacional', '29': 'Serv. educativos', '8': 'Psiquiatría', '2': 'Psicología', '21': 'Estimulación Temprana', '4': 'Asesoría Emocional', '83': 'Apoyo Económico a las asociaciones vinculadas con el Tema de Discapacidad.', '24': 'Serv. Educativos (Manualidades para la independencia)', '68': 'Artes Plásticas', '60': 'Asistencia Médica Gratuita', '41': 'Serv. Alquiler de Muletas', '69': 'Terapia física', '31': 'Serv. Educativos: Manualidades.', '76': ': Terapía Lenguaje', '37': 'Servicio asistencia económica para pacientes en fase terminal', '27': 'Serv. Terapia Física', '7': 'Fisioterapia', '67': 'Educación Física', '28': 'Centro atención integral.'}
    needle = str(get_org_name_product(text))
    print(needle)
    for key, value in names.items():
        value = str(value)
        if value == needle:
            print("\t\033[94morganizationsIdFk:\033[0m " + key)
            return key

    print("\t\u001B[31morganizationsIdFk:\033[0m ERROR")
    return 100


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


# def get_item_name_service(text):
#     start = "de apoyo que se brinda "
#     if text.find(start) == -1:
#         start = "de apoyo como lo enuncia la entidad que lo brinda."
#         if text.find(start) == -1:
#             start = "de apoyo, como lo enuncia la entidad que lo brinda."
#     end = "Localización del servicio de apoyo:"
#     needle = text[text.find(start) + len(start): text.find(end)]
#     print("\t\033[94mName of service:\033[0m " + needle)
#     needle = needle.replace("\n", " ")
#     needle = needle.replace("\t", " ")
#     needle = re.sub(' +', ' ', needle)
#     needle = needle.rstrip()
#     needle = needle.lstrip()
#     needle = needle.replace("\'", "")
#     needle = needle.replace("'", "")
#     needle = needle.replace("\"", "")
#     return needle


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
    if needle != "":
        return needle

    else:
        return "No brinda información."


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
    if needle != "":
        return needle

    else:
        return "No brinda información."


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
    if needle != "":
        return needle

    else:
        return "No brinda información."


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
    if needle != "":
        return needle

    else:
        return "No brinda información."


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
    if needle != "":
        return needle

    else:
        return "No brinda información."


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
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
       # print("\t\033[94mname:\033[0m " + needle)
        if needle == "" or needle == " " or needle == "\n" or needle == " \n":
            print("\t\u001B[31mname:\033[0m No brinda información")
            return "No brinda información"
        else:
            if needle == "Hospital William Allen Taylor- CCSS" or needle == "Hospital William Allen Taylor, CCSS":
                needle = "Hospital William Allen Taylor - CCSS"

            if needle == "Chupis Ortopedica":
                needle = "Chupis Ortopédica"

            if needle == "No brinda información":
                needle = "Clínicas de la Audición"

            if needle == "Hospital San Rafael de Alajuela- CCSS":
                needle = "Hospital San Rafael de Alajuela - CCSS"

            return needle

    else:
        #print("\t\u001B[31mname:\033[0m No brinda información")
        return "No brinda información"


def get_org_email_product(text):
    start = "Dirección de correo electrónico:"
    end = "Web del servicio:"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
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
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
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
        return str(dict).replace("{'facebook': '" , "[{\"'facebook'\": \"").replace("'}" , "\"}]")

    else:
        print("\t\u001B[31msocialNetworks:\033[0m No brinda información")
        return [{}]


def get_org_wazeAddress_product(text):
    start = "Dirección waze:"
    end = "Ubicación"
    if text.find(start) != -1 and find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
        print("\t\033[94mwazeAddress:\033[0m " + str(urls))
        return str(urls).replace("['" , "[\"'").replace("']" , "'\"]")

    else:
        print("\t\u001B[31mwazeAddress:\033[0m No brinda información")
        return "No brinda información"


def get_org_reaches_product(text):
    start = "Fines:"
    end = "Misión:"
    if text.find(start) != -1 and  find_nth(text, end, 1) != -1:
        needle = text[text.find(start) + len(start): find_nth(text, end, 1)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        print("\t\033[94mreaches:\033[0m " + needle)
        return needle

    else:
        print("\t\u001B[31mreaches:\033[0m No brinda información")
        return "No brinda información"


def get_org_mision_product(text):
    start = "Misión:"
    end = " Visión: "
    if text.find(start) != -1 and text.find(start) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        print("\t\033[94mmision:\033[0m " + needle)
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
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        print("\t\033[94mvision:\033[0m " + needle)
        return needle

    else:
        print("\t\u001B[31mvision:\033[0m No brinda información")
        return "No brinda información"


def get_org_objective_product(text):
    start = " Objetivos: "
    end = " Señale el tipo de oferente del servicio de apoyo"
    if text.find(start) != -1 and text.find(end) != -1:
        needle = text[text.find(start) + len(start): text.find(end)]
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        needle = needle.replace("5." , "")
        print("\t\033[94mobjective:\033[0m " + needle)
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
        needle = needle.replace("\n", " ")  # removes all newline characters from text
        needle = needle.replace("\t", " ")  # replaces tabs with spaces
        needle = re.sub(' +', ' ', needle)  # removes all repeated whitespace from text
        needle = needle.rstrip()
        needle = needle.lstrip()
        needle = needle.replace("\'" , "")
        needle = needle.replace("'", "")
        needle = needle.replace("\"" , "")
        print("\t\033[94mdayOperations:\033[0m " + needle)
        needle = needle.replace("13.", "")
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
            if needle == "Hospital William Allen Taylor- CCSS" or needle == "Hospital William Allen Taylor, CCSS":
                needle = "Hospital William Allen Taylor - CCSS"

            if needle == "Chupis Ortopedica":
                needle = "Chupis Ortopédica"

            if needle == "No brinda información":
                needle = "Clínicas de la Audición"

            if needle == "Hospital San Rafael de Alajuela- CCSS":
                needle = "Hospital San Rafael de Alajuela - CCSS"

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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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
    if needle == "" or needle == "-":
        needle = "No brinda información."
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

    if needle == "" or needle == "-":
        needle = "No brinda información."

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

    if needle == "" or needle == "-":
        needle = "No brinda información."
    print("\t\033[94mattentionFrecuency:\033[0m " + result)
    return result


def get_service_classification(text):
    haystack = text[text.find("MIDEPLAN") : text.find("Indique si es un servicio público, privado")]

    print(haystack)

    needle_social = "Social y de Lucha contra la Pobreza: ("
    needle_ambiente = ") Ambiente, Energìa y Telecomunicaciones: ("
    needle_gubernamental = ") Coordinación Gubernamental: ("
    needle_salud = ") Salud: ("
    needle_financiero = ") Financiero: ("
    needle_educativo = ") Educativo: ("
    needle_productivo = ") Productivo: ("
    needle_monetario = ") Política Monetaria y Supervisión Financiera: ("
    needle_infraestructura = ") Infraestructura y Transporte: ("
    needle_delito = ") Seguridad Ciudadana y Prevención del Delito: ("
    needle_municipal = ") Municipal: ("
    needle_trabajo = ") Trabajo y Seguridad Social: ("
    needle_turismo = ") Turismo: ("
    needle_cultural = ") Cultural: ("
    needle_politica = ") Política Exterior: ("
    needle_comercio = ") Comercio Exterior: ("
    needle_tecnologia = ") Tecnología: ("

    end = ") Costo"

    social = haystack[haystack.find(needle_social) + len(needle_social): haystack.find(needle_ambiente)].replace(" " , "").replace("X" , "x")
    ambiente = haystack[haystack.find(needle_ambiente) + len(needle_ambiente): haystack.find(needle_gubernamental)].replace(" " , "").replace("X" , "x")
    gubernamental = haystack[haystack.find(needle_gubernamental) + len(needle_gubernamental): haystack.find(needle_salud)].replace(" " , "").replace("X" , "x")
    salud = haystack[haystack.find(needle_salud) + len(needle_salud): haystack.find(needle_financiero)].replace(" " , "").replace("X" , "x")
    financiero = haystack[haystack.find(needle_financiero) + len(needle_financiero): haystack.find(needle_educativo)].replace(" " , "").replace("X" , "x")
    educativo = haystack[haystack.find(needle_educativo) + len(needle_educativo): haystack.find(needle_productivo)].replace(" " , "").replace("X" , "x")
    productivo = haystack[haystack.find(needle_productivo) + len(needle_productivo): haystack.find(needle_monetario)].replace(" " , "").replace("X" , "x")
    monetario = haystack[haystack.find(needle_monetario) + len(needle_monetario): haystack.find(needle_infraestructura)].replace(" " , "").replace("X" , "x")
    infraestructura = haystack[haystack.find(needle_infraestructura) + len(needle_infraestructura): haystack.find(needle_delito)].replace(" " , "").replace("X" , "x")
    delito = haystack[haystack.find(needle_delito) + len(needle_delito): haystack.find(needle_municipal)].replace(" " , "").replace("X" , "x")
    municipal = haystack[haystack.find(needle_municipal) + len(needle_municipal): haystack.find(needle_trabajo)].replace(" " , "").replace("X" , "x")
    trabajo = haystack[haystack.find(needle_trabajo) + len(needle_trabajo): haystack.find(needle_turismo)].replace(" " , "").replace("X" , "x")
    turismo = haystack[haystack.find(needle_turismo) + len(needle_turismo): haystack.find(needle_cultural)].replace(" " , "").replace("X" , "x")
    cultural = haystack[haystack.find(needle_cultural) + len(needle_cultural): haystack.find(needle_politica)].replace(" " , "").replace("X" , "x")
    politica = haystack[haystack.find(needle_politica) + len(needle_politica): haystack.find(needle_comercio)].replace(" " , "").replace("X" , "x")
    comercio = haystack[haystack.find(needle_comercio) + len(needle_comercio): haystack.find(needle_tecnologia)].replace(" " , "").replace("X" , "x")
    tecnologia = haystack[haystack.find(needle_tecnologia) + len(needle_tecnologia): haystack.find(end)].replace(" " , "").replace("X" , "x")

    # print(social , ambiente , gubernamental , salud , financiero , educativo , productivo , monetario , infraestructura , delito , municipal , trabajo , turismo , cultural , politica , comercio , tecnologia)

    sectors = []

    if social == "x":
        sectors.append(1)
    if ambiente == "x":
        sectors.append(2)
    if gubernamental == "x":
        sectors.append(3)
    if salud == "x":
        sectors.append(4)
    if financiero == "x":
        sectors.append(5)
    if educativo == "x":
        sectors.append(6)
    if productivo == "x":
        sectors.append(7)
    if monetario == "x":
        sectors.append(8)
    if infraestructura == "x":
        sectors.append(9)
    if delito == "x":
        sectors.append(10)
    if municipal == "x":
        sectors.append(11)
    if trabajo == "x":
        sectors.append(12)
    if turismo == "x":
        sectors.append(13)
    if cultural == "x":
        sectors.append(14)
    if politica == "x":
        sectors.append(15)
    if comercio == "x":
        sectors.append(16)
    if tecnologia == "x":
        sectors.append(17)

    print(sectors)

    return sectors


def generate_sectorClassifications_line(text):
    line = ""
    names = {'1063': 'Almohada de aire', '259': 'Zapato Ortopédico', '95': 'Serv. Educación Especial', '798': 'Producto: Software escribir con leves movimientos de mouse -CENAREC-.', '179': 'Masajeador corporal', '294': 'VENDA ELÁSTICA PARA TOBILLO VENTILADA', '623': 'Prod. Maquina escribir braille perkins', '140': 'Serv. Asesoría Legal', '1022': 'Corset Lona lumbrosacro', '346': 'COJÍN CILINDRO', '612': 'Prod. Impresora Braille Juliet pro', '1100': 'Andadera Plegable Bariatrica', '1011': 'Prótesis de brazo', '250': 'Cojín lumbar', '687': 'Producto: Cuchara con desviación izquierda -CENAREC-.', '419': 'Tiflotecnología', '546': 'Prod. Balón soccer con campanas', '530': 'Prod. Cubiertas poly', '608': 'Prod. Reloj para aprender la hora', '25': 'Terapia Ocupacional', '773': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.', '944': 'Prod. Transmisor audio de TV', '619': 'Prod. Puntero gancho tipo rodillo', '99': 'Capacitaciones a personas, entidades privadas o públicas en el cantón.', '726': 'Producto apoyo: Adaptador Monitor Táctil -CENAREC-.', '1185': 'Venta producto de apoyo - Cama Hospitalaria Full Eléctrica', '388': 'Colchón de aire', '1021': 'Mano tipo garfio', '1027': 'Muleta canadiense.', '356': 'Silla Baño con respaldar', '1115': 'Compresas frio calor', '80': 'Audiometrías', '183': 'Masajeador facial', '912': 'Prótesis ante brazo', '371': 'Prod. Silla inodoro', '220': 'Férula antiespastica', '887': 'Prótesis ocular individualizada', '508': 'Producto: reloj despertador mesa con voz español numero grandes', '639': 'Prod. Inodoro portátil', '938': 'Audifono via osea', '813': 'Producto: Mesa y silla para trabajo -CENAREC-.', '319': 'Prod. Electrodo pals redondo 2 pulgadas', '954': 'Audífonos', '909': 'Quilla madera adulto', '698': 'Producto: Mouse tipo “joystick” -CENAREC-.', '125': 'Terapia de lenguaje', '1000': 'Férulas Polipropileno adulto', '719': 'Producto: Software Permite imprimir gráficos en relieve y Braille -CENAREC-.', '511': 'Producto: silla plegable de baño', '12': 'Psiquiatría', '1005': 'Quilla madera adulto', '848': 'Producto: Comunicador de 6 casillas con 5 niveles. -CENAREC-.', '767': 'Producto: Dispositivo que permite grabar un mensaje, aviso, noticia -CENAREC-.', '137': 'Centro Atención Integral', '353': 'Colchón de agua', '515': 'Producto: juego dominó piezas grandes', '1138': 'Venta producto de apoyo - Canula Nasal Adulto', '1099': 'Inmovilizador tobillo corto', '1039': 'Bandas de ejercicio', '818': 'Producto: Comunicador tipo Handheld de pantalla táct -CENAREC-.', '1085': 'Bolsa para agua fria', '1006': 'Quilla Carbono niño', '45': 'Serv. educativos', '666': 'Salvaescalera Homeglide', '883': 'Ferula ortoplast niño', '745': 'Producto: Cepillo de Dientes Adaptado -CENAREC-.', '507': 'Producto: regleta de aluminio para escribir', '174': 'Hombreras', '362': 'ANDADERA CON SENTADERA CON CANASTA', '958': 'Prod. Phone Clip', '23': 'Psiquiatría', '1112': 'Arnes para grua', '868': 'Producto: Destapador de botellas antideslizante -CENAREC-.', '943': 'Prod. Terapia ZEN', '558': 'Prod. Papel Braille', '377': 'Prod. Silla Ruedas con inodoro', '270': 'BASTON PLEGABLE', '664': 'Salvaescalera Elba', '1146': 'Producto de apoyo - Venta Compresor Oxígeno Visión Air', '735': 'Producto: Comunicador de 8 casillas -CENAREC-.', '450': 'Producto: reloj braille mujer seiko', '68': 'Serv. Alquiler de Andaderas', '257': 'Férulas de Mano para Túnel Carpal', '866': 'Producto: Software Emulador de Mouse -CENAREC-.', '646': 'Prod. Silla Baño con y sin respaldo', '103': 'Alquiler Médicos ByB - Andaderas', '1090': 'Tracción cervical', '46': 'Presupuesto para apoyar ONG’S que atienden personas con discapacidad en el Cantón.', '292': 'BOLA EJERCICIO 86 CM', '1134': 'Venta producto de apoyo - Colchón espuma impermeable 6 pulgadas', '236': 'Alquiler de Equipo Médico - Andaderas', '1117': 'Silla Baño sin respaldo', '895': 'Electrodos para marcapasos', '786': 'Producto: Mouse tipo Pulsador Casero -CENAREC-.', '980': 'Ferula laminado resina adulto', '384': 'Cama Ortopedica Manual', '1014': 'Cambio de socket', '167': 'Bastón con asiento', '918': 'Cambio de socket', '659': 'SILLA DE BAÑO CON AGARRADERAS', '1140': 'Venta producto de apoyo - Bastón de 1 punta apoyo', '841': 'Producto: Mouse para pie -CENAREC-.', '443': 'Producto: guia para firmar plastico regular', '940': 'Audifono Intra canal', '736': 'Producto: Computadora portatil táctil -CENAREC-.', '1007': 'Quilla madera niño', '27': 'Trabajo Social', '703': 'Producto: Bastón electrónico -CENAREC-.', '1029': 'Collar cervical tipo Thomas duro.', '130': ': Educación Física', '455': 'Producto: cuchara y tenedor con correa de vinil', '484': 'Producto: lupa pagina completa magnificadora 2x', '536': 'Prod. Juego Geométrico táctil', '296': 'Compresa fría', '662': '. Ascensor Acuático', '1151': 'Venta producto de apoyo - Elevador de Sanitario sin brazos', '569': 'Prod. Hover mounting kit', '718': 'Producto: Software Emulador teclado Virtual -CENAREC-.', '948': 'Prod. Baterías para Audífonos', '1080': 'Elevador de inodoro con brazos', '37': 'Estimulación Temprana', '51': 'Serv. Educativos.', '326': 'VENDA COBAN DUKAL 4 ADHESIVA PIE', '1122': 'Silla Baño con respaldo', '627': 'Prod. Papel Braillon', '258': 'Férulas de Mano para Túnel Carpal - Tendinitis', '271': 'BASTON DE 4 PUNTOS', '1178': 'Venta producto de apoyo - Tanque Oxigeno 1.699 L', '1149': 'Producto de apoyo - Alquiler Compresor Oxígeno', '286': 'Electrodo económico', '898': 'Protesis cardiacas biologica mitral', '438': 'Producto: Teclado letra grande', '1042': 'Codera para piel de oveja', '780': 'Producto: Antideslizante -CENAREC-.', '986': 'Lente intraocular', '394': 'Silla Ruedas 18 pulgadas', '696': 'Producto: Comunicador 7 mensajes -CENAREC-.', '479': 'Producto: set 3 piezas etiquetas braille', '173': 'Mascara de oxigeno', '75': 'Serv. Educativos', '210': 'Cuña para piernas', '568': 'Prod. Impresora Braille Trident', '520': 'Producto:', '609': 'Prod. Mouse Switch', '241': 'Alquiler Silla de ruedas no ortopedicas', '683': 'Producto: Monitores con pantalla táctil -CENAREC-.', '73': 'Terapia Ocupacional', '1145': 'Venta producto de apoyo - Producto: Andadera con rodines', '584': 'Prod. Teclado letras grandes', '10': 'Alquiler sillas de ruedas.', '1130': 'Prod. Alquiler de cama', '78': 'Terapia Física', '274': 'Corset de Jewett', '118': 'Hogar de cuido para personas con parálisis cerebral en situación de abandono', '702': 'Producto: Comunicador de tarjetas - CENAREC-.', '458': 'Producto: lápiz punzón escribir braille', '835': 'Producto: Kit para el cuidado diario -CENAREC-.', '409': 'Ortesis muñeca y dedo', '368': 'Bastón una punta decorado', '369': 'Prod. Silla de baño de transferencia', '180': 'Gradas 2 peldaños', '1046': 'Tobillera elastica', '973': 'Donación de equipo Técnico - Sillas Ruedas Estandar (uso diario)', '14': 'Audiometrías', '641': 'Prod. Silla Ruedas Ortopedica', '13': 'Ortopédia.', '1116': 'Cama Ortopedica Manual', '33': 'Terapia Física', '155': 'Fajas embarazadas', '638': 'Prod. Bidé', '583': 'Prod. Software grid 2', '232': 'Alquiler: Sillas Ruedas', '978': 'Ferula para mano antiespasmica', '301': 'BOLA EJERCICIO 75CM', '921': 'Guante cosmetico', '38': 'Enseñanza de Lesco', '534': 'Prod. Maquina escribir braille perkins next generation', '525': 'Producto: tablero juego damas en braille', '1015': 'Prótesis arriba rodilla', '684': 'Producto: Silla Ruedas Electrica -CENAREC-.', '342': 'COJÍN LUMBAR', '1182': 'Venta producto de apoyo - Esfigmomanometro Digital', '264': 'Férulas Polipropileno Especiales', '965': 'Ortesis Auditivas: Retro auricular', '970': 'Calculadora Parlante', '340': 'VENDA DE GASA 10 CM x 5 M LE ROY', '1201': 'Salvaescalera LG 2020', '79': 'Serv. Equinoterapia', '359': 'Bastón una punta de madera', '4': 'Asesoría Emocional', '554': 'Prod. Baston aluminio rigido', '865': 'Producto: Software Magnificador y lector de pantalla -CENAREC-.', '711': 'Producto: Software Mouse por barrido -CENAREC-.', '1191': 'Venta producto de apoyo - Inodoro Portatil 3 en 1', '61': 'Terapia Ocupacional', '1167': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica 16 pulgadas', '275': 'ELECTRODO WANDY ADHESIVO', '512': 'Producto: reloj deportivo vibración de luz', '157': 'Sistema drenaje urinario cama', '894': 'Ortesis cables flexibles', '471': 'Producto: bastón movilidad grafito y corcho - baja vision', '633': 'Prod. Bastón de 1 punta', '691': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '34': 'Servicio de audiología en general con fabricación de audífonos.', '328': 'Compresa fría', '308': 'ELECTRODO TYCO 2X2', '430': 'Producto: Lentes ultrasónicos', '751': 'Producto: Camera Mouse -CENAREC-.', '604': 'Prod. Protector pantalla Braille para celular', '238': 'Alquiler de Equipo Médico - Muletas', '963': 'Ortesis Auditivas: Audífonos Intra-canal', '178': 'zapato para yeso', '759': 'Producto: Mouse controlado por mov. ojos -CENAREC-.', '618': 'Prod. Impresora Braille Cyclone', '457': 'Producto: etiquetadora braille', '869': 'Producto: Cuaderno Electronico -CENAREC-.', '1081': 'Alcanzador', '523': 'Producto: audífonos stereo bellman', '796': 'Producto: Teclado con letras grandes y en color de alto contraste - CENAREC-.', '9': 'Terapia Física', '122': 'Educación Física', '681': 'Producto: Pulsador tipo Varilla -CENAREC-.', '502': 'Producto: máquina escribir clásica braille perkins', '932': 'Collar cervical filadelfia', '489': 'Producto: pizarra magnética con formas, letras y números', '761': 'Producto: Software Emulador de barrido -CENAREC-.', '972': 'Donación de equipo Técnico - Sillas Baño', '404': 'Ferula Muñeca', '84': 'Centro Atención Integral', '1033': 'Audifono tipo caja bolsillo', '124': 'Terapia física', '1070': 'Pesas para muñeca', '974': 'Donación de equipo Técnico - Rodilleras', '840': 'Producto: Funda tipo almohadilla para pulsador -CENAREC-.', '195': '', '549': 'Prod. Etiquetador con dial', '391': 'Bastón de una punta de apoyo', '476': 'Producto: reloj llavero con voz español', '959': 'Prod. Implante Coclear', '941': 'Audifono Intra auricular', '69': 'Servicio alquiler o préstamo de Camas Hospitalarias.', '312': 'COJÍN CUADRADO ANATÓMICO ENSUEÑO', '381': 'Prod. Muleta adulto', '803': 'Producto: Máquina para escritura en Braille estándar -CENAREC-.', '487': 'Producto: bastón movilidad de grafito color de lujo', '348': 'ELECTRODO VALUTRODE REDONDO 1.25', '70': 'Serv. Alquiler de Muletas', '997': 'Marcapaso binacameral', '1013': 'Cambio de encaje', '1082': 'Andadera Universal niño', '945': 'Prod. Manos Libres', '272': 'Cuña para Espalda', '161': 'Carretilla oxígeno', '572': 'Prod. Kit diagramación táctil', '108': 'Centro Atención Integral', '905': 'Férulas Polietileno adulto', '349': 'Mesa Puente', '849': 'Producto: Software lector de texto -CENAREC-.', '763': 'Producto: Software Emulador Mouse -CENAREC-', '198': 'Colchón ortopédico', '336': 'COJÍN DE GEL CUADRADO', '1086': 'Baston Ajustable', '768': 'Producto: Software Emulador Mouse -CENAREC-.', '324': 'ELECTRODO VALUTRODE CUADRADO 2X2', '822': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.', '1193': 'Venta producto de apoyo - Oximetro Digital', '1168': 'Alquiler producto de apoyo - Sillas Rueda Estándar 18 pulgadas', '1091': 'Inmovilizador de dedos', '979': 'Ferula ortoplast niño', '1096': 'Muslera elástica', '1028': 'Collar cervical tipo filadelfía.', '875': 'Producto: Conmutador tipo Pulsador -CENAREC-.', '387': '', '329': 'VENDA ELÁSTICA LE ROY 7,5 x 5MTS', '445': 'Producto: bascula peso con habla español', '422': 'Producto: impresora braille basic modelo DV 5', '266': 'Collar Cervical Blando', '345': 'Cojín cuadrado de espuma', '996': 'Protesis cardiacas biológica aortica', '723': 'Producto: Teclados de teclas grandes - CENAREC-.', '634': 'Prod. Elevador de sanitario con soportes', '806': 'Producto: Software Emulador Teclado Virtual -CENAREC-.', '1142': 'Venta producto de apoyo - Gigante para Suero', '539': 'Prod. Puntero gancho tipo puntero jumbo', '910': 'Quilla carbono niño', '550': 'Prod. Impresora Braille - Braillo 600', '671': 'Préstamo de equipo especial: Sillas Ruedas No ortopedica', '1057': 'Estabilizador rodilla', '100': 'Formación Humana', '380': 'Silla Ruedas para PC - 18 pulgadas', '946': 'Prod. Sistema FM', '655': 'COJIN AIRE GEL', '1058': 'muñequera y dedo pulgar', '1189': 'Venta producto de apoyo - Sillas baño con respaldar', '352': 'Andadera adulto aluminio con rodines', '968': 'Sistema de frecuencia modulada (juego de audífonos y micrófono)', '332': 'PINZA ADSON SIN DIENTES', '20': 'Terapia ocupacional', '147': 'Ser. alquiler camas ortopedicas', '947': 'Prod. Control para audífono', '151': 'Suspensorios Deportivo', '1137': 'Venta producto de apoyo - Canula Nasal Adulto', '701': 'Producto: Bastón Plegable -CENAREC-.', '370': 'Bastón 4 puntas - KX Medical', '219': 'Colchón de aire con compresor', '473': 'Producto: reloj hombre habla español', '504': 'Producto: reloj para hombre con habla español', '557': 'Prod. Reloj mujer con voz digital', '212': 'Cabestrillo', '742': 'Producto: Software Comunicación Sordo-Ceguera -CENAREC-.', '787': 'Producto: Corta Uñas Adaptado -CENAREC-.', '463': 'Producto: calculadora que habla español', '65': 'Centro educativo - Educación especial curricular.', '834': 'Producto: Conmutador electromiográfico -CENAREC-.', '144': 'Servicios educativos.', '743': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '1087': 'Bastón con asiento', '373': 'Muleta adulto JR', '276': 'LIGA THERA-BAND GRIS', '1035': 'Audifono tipo Retro auricular', '533': 'Prod. Grabador audio con software incluido', '578': 'Prod. Software Jaws', '628': 'Prod. Mesa Puente', '52': 'Terapia Ocupacional', '957': 'Prod. Softband', '563': 'Prod. Balon super suave espuma con cascabeles', '497': 'Producto: indicador nivel batería de líquidos', '133': ': Psicología', '728': 'Producto: Comunicador multinivel de 8 casillas -CENAREC-.', '464': 'Producto: Juego ajedrez para personas no videntes', '360': 'Silla baño con respaldo', '1009': 'Prótesis de pierna', '317': 'Electrodo carbono 5 cm', '427': 'Producto: bastón movilidad fibra vidrio', '1054': 'Mesa Puente', '821': 'Producto: Mesa con escotadura -CENAREC-.', '839': 'Producto: Comunicador de 32 casillas con barrido -CENAREC-.', '456': 'Producto: globo terraqueo con relieve', '1059': 'Dona Hule infable', '436': 'Producto: magnificador de imágenes alta definición', '514': 'Producto: paquete de papel imprimir braille', '805': 'Producto: Sistema de montaje para conmutadores -CENAREC-.', '188': 'Bota esguince grado 3', '851': 'Producto: Sistema de montaje para comunicadores -CENAREC-.', '412': 'SOPORTE ESCROTAL ATLÉTICO', '343': 'Cojin inflable cervical', '350': 'Silla Ruedas full ortopédica', '467': 'Producto: malla cómoda de cuerpo entero elevador pacientes', '112': 'Centro Atención Integral', '953': 'Prod. Deshumedecedor pastilla', '1188': 'Venta producto de apoyo - Sillas baño con respaldar', '610': 'Prod. Expert Mouse', '415': 'Ortesis muñeca derecho o izquierdo', '221': 'Ortesis hombro', '309': 'ELECTRODO WANDY CON ADHESIVO', '585': 'Prod. Bloque aprender braille money pocket', '1206': 'Silla Ruedas electrica SAT-FGO', '1150': 'Producto de apoyo - Alquiler Compresor Oxigeno New Life Elite', '987': 'Ortesis al tercio', '672': 'Préstamo de equipo especial: Camas Hospitalarias', '622': 'Prod. Teclado configurable para PC', '854': 'Producto: Software Emulador de mouse -CENAREC-.', '331': 'LIGA THERA-BAND AMARILLO', '913': 'Prótesis pierna', '597': 'Prod. Bastón rígido grafito', '89': 'Audiometrías', '385': 'Silla Ruedas con partes movibles', '983': 'Prótesis ocular individualizada', '375': 'Bastón 4 puntas - drive', '811': 'Producto: Software Emulador de Teclado Virtual -CENAREC-.', '1107': 'Almohada Cervical', '1066': 'Cuello inmovilizador', '706': 'Producto: Lupa de barra de 8 pulgadas -CENAREC-.', '1103': 'Cabestrillo', '1154': 'Venta producto de apoyo - Estetoscopio', '466': 'Producto: reloj caballero con voz español bicolor', '364': 'Colchón de aire con compresor', '437': 'Producto: atril manos libres', '93': 'Serv. Apoyo Emocional', '460': 'Producto: balón de campanas', '234': 'Alquiler de Equipo Médico - Cama Hospitalaria', '556': 'Prod. Bastón Plegable de aluminio', '176': 'Faja para torax', '284': 'LIGA THERA-BAND DORADO', '334': 'Compresa fría', '1209': 'Plataforma vertical SAT-GL', '967': 'Lupa con lámpara', '1153': 'Venta producto de apoyo - El Cobertor impermeable para colchón', '755': 'Producto: Pulsador que permite grabar un mensaje -CENAREC-.', '63': 'Terapia Física', '290': 'Bola de Gel', '42': 'Apoyos Didácticos', '196': 'Muñequera tunel carpal', '1163': 'Venta producto de apoyo - Sillas Rueda Full Ortopédica', '753': 'Producto: Impresora Braille -CENAREC-.', '423': 'Producto: identificador luz con voz español', '76': 'Serv. Terapia Ocupacional', '1164': 'Alquiler producto de apoyo - Sillas Rueda Full Ortopédica', '574': 'Prod. Mouse trackball', '28': 'Terapia de Lenguaje', '825': 'Producto: Carcasa de Teclado -CENAREC-.', '1127': 'Prod. Alquiler gigante suero', '154': 'Protector talón', '189': 'Bastón de 1 punta', '937': 'Audifono tipo caja bolsillo', '1180': 'Venta producto de apoyo - Pedal para Ejercicios', '881': 'Ferula para pie adulto', '303': 'ELECTRODO PREMIUN TAN REDONDO 2', '344': 'RODILLO DE MANO THERABAND ROJO', '142': 'Servicios Educativos', '277': 'MASILLA CANDO THERAPUTTY', '1195': 'Venta producto de apoyo - (BOLSA PARA RECOGER DESECHOS)', '393': 'Prod. Silla inodoro', '640': 'Prod. Estetoscopio', '925': 'Mano tipo garfio', '1094': 'Alquiler de andadera', '1148': 'Venta producto de apoyo - Alquiler Compresor Oxígeno Visión Air', '704': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '885': 'Ferula laminado resina niño', '50': 'Centro Atención Integral', '77': 'Serv. Apoyo Emocional', '547': 'Prod. Head Mouse', '310': 'COJÍN PARA PIERNAS', '748': 'Producto: Atril Ajustable -CENAREC-.', '603': 'Prod. Puntero Slip-on tipo marshmallow', '915': 'Prótesis brazo', '682': 'Producto: Comunicador de 3 casillas que se ajusta a la cadera -CENAREC-.', '605': 'Prod. Roller Mouse red', '267': 'Silla de Ruedas Standart', '776': 'Producto: Software Magnificador de pantalla para personas con baja visión -CENAREC-.', '1173': 'Venta producto de apoyo - Andadera Plegable de Aluminio', '1008': 'Prótesis de antebrazo', '1200': 'Muletas anfibias', '30': 'Terapia Ocupacional', '478': 'Producto: línea braille smart beetle teclado y pantalla braille ultra portatil', '243': 'Corset Toracolumbar', '148': 'Serv. Ocupacionales de Recreo', '242': 'Alquiler silla baño', '991': 'Electrodos para marcapasos', '1125': 'Prod. Sillas Ruedas', '163': 'Almohada tipo dona', '720': 'Producto: Utensilios de cocina -CENAREC-.', '82': 'Psiquiatría', '442': 'Producto: impresora braille everest modelo DV 5', '2': 'Psicología', '690': 'Comunicador de 7, 12 o 23 casillas, de diseño moderno, con 5 niveles. -CENAREC-.', '837': 'Producto: Software Lector de pantalla libre personas con baja visión -CENAREC-.', '509': 'Producto: punteras para bastón ambutech', '448': 'Producto: lupa escritorio de iluminación', '87': 'Terapia Física', '653': 'BIDEP DE ACERO', '831': 'Producto: Indicador de nivel de líquidos -CENAREC-.', '400': 'CAMA ORTOPÉDICA ELÉCTRICA CON BARANDAS Y COLCHÓN AMERICAN BANTEX', '152': 'Pesa arena', '1050': 'Tobillera neopreno', '58': 'Serv. Educativos', '901': 'Marcapaso binacameral', '644': 'Prod. Sillas de ruedas no ortopédicas', '893': 'Ortesis corta', '919': 'Protesis arriba rodilla', '744': 'Producto: Calculadora Visual -CENAREC-.', '695': 'Producto: Silla para posicionamiento -CENAREC-.', '543': 'Prod. Mini Balon con campanas', '621': 'Prod. Bastón puntero gancho tipo lapiz', '407': 'SoftPad', '855': 'Producto: Software Lector de pantalla para personas ciegas o con baja visión -CENAREC-.', '846': 'Producto: Control de radiofrecuencia -CENAREC-.', '396': 'Muleta Adulto', '579': 'Prod. Software traductor braille', '123': 'Artes Plásticas', '1064': 'Orinal masculino', '551': 'Prod. Guía para firma', '1017': 'Guante cosmetico', '150': 'Corrector clavícula', '778': 'Producto: Mouse tipo “joystick” para utilizar con el mentón -CENAREC-.', '734': 'Producto: Touchpad y mouse por teclas -CENAREC-.', '263': 'Férulas Polipropileno para mano.', '576': 'Prod. Marco aritmético y ábaco combinado', '201': 'Corrector postura', '297': 'Electrodo cuadrado azul', '209': 'Bastón de 4 puntos', '162': 'Riñon de acero', '218': 'Bolsa para enema', '175': 'Gigante 4 ganchos', '333': 'ELECTRODO VALUTRODE REDONDO 2.75', '829': 'Producto: Tabla con rodines - CENAREC-', '824': 'Producto: Puntero con agarrador manual -CENAREC-.', '339': 'Prod. ELECTRODO THERATRODE 2 x 2', '820': 'Producto: Focus - Display Braille -CENAREC-.', '570': 'Prod. Calculadora cientifica parlante', '465': 'Producto: juego cartas naipe en braille', '537': 'Prod. Impresora Braille jot a dot', '1135': 'Venta producto de apoyo - Bidet Plástico', '1162': 'Venta producto de apoyo - Sillas Rueda Estandar 18 pulgadas', '573': 'Prod. Software well clicker 2', '246': 'Estabilizador de Rodilla', '688': 'Lapiz escribe en papel termosensible -CENAREC-.', '269': 'BASTÓN DE 1 PUNTO', '392': 'BASTÓN 1 PUNTO ANTISHOCK CON FOCO', '470': 'Producto: lupa reglón 2x', '952': 'Prod. Deshumedecedor eléctrico', '383': 'Férula espinal rígida', '707': 'Producto: Software comunicación alternativa -CENAREC-.', '808': 'Producto: Grúa Hidráulica -CENAREC-.', '791': 'Producto: Borde para plato -CENAREC-.', '1041': 'Andadera Plegable', '203': 'Venda theraband', '314': 'Cojin Lumbar de malla', '876': 'Producto: Impresora Braille -CENAREC-.', '838': 'Producto: Grabadora con Pictograma -CENAREC-.', '472': 'Producto: lupa electronica bolsillo 7 pulgadas', '870': 'Producto: Cuaderno Electronico -CENAREC-.', '454': 'Producto: juego formas y colores', '172': 'Silla de baño', '18': 'Capacitaciones', '85': 'Centro de atención integral', '366': 'Bastón plegable azul, una punta', '177': 'Botella para orinar hombre', '47': 'Serv. Educativos: Manualidades.', '261': 'Férulas Polipropileno para brazo.', '600': 'Prod. Mouse Kid Trackball', '1036': 'Audifono tipo Intra canal', '224': 'Soporte codo', '817': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.', '505': 'Producto: rayo electronico personas baja visión', '737': 'Producto: Conmutador que emula el clic del mouse -CENAREC-.', '540': 'Prod. Guia actividades caja luz', '916': 'Zapato ortopedico bajo molde yeso adulto', '1076': 'Ferula muñeca', '262': 'Férulas Polipropileno PIE', '1040': 'Silla brazo tipo escritorio pies desmontables', '607': 'Prod. Impresora Braille - Braillo 600 sw', '187': 'Rodillera para meniscos', '960': 'Prod. Procesador de sonido', '171': 'Kinesiotape', '544': 'Prod. Impresora Braille - Braillo 600 sr', '411': 'Zapato para yeso', '984': 'Prótesis ocular', '1199': 'Silla Anfibia', '645': 'Prod. gigante suero', '917': 'Cambio de encaje', '200': 'Colchón de agua', '1020': 'Mano con guante cosmeticos', '988': 'Ortesis larga', '282': 'ELECTRODO PREMIUN BLANCO REDONDO 2', '845': 'Producto: Transmisor de alertas para timbre y teléfono -CENAREC-.', '1024': 'Corset Lona toracolumbar', '1158': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica 18 pulgadas', '774': 'Producto: Conmutador tipo pulsador -CENAREC-.', '936': 'Muleta axilar', '208': 'Faja industrial', '902': 'Marcapaso unicameral', '1157': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica 16 pulgadas', '903': 'Silla Ruedas Especializadas', '928': 'Corset lona toracolumbar', '624': 'Prod. Impresora Braille Juliet 120', '804': 'Producto: Computador Portátil Táctil -CENAREC-.', '1056': 'Muleta Universal', '548': 'Prod. Bastón grafito telescópico', '658': 'ESPALDERA POSTURAL', '792': 'Producto: Etiquetadora Braille -CENAREC-.', '306': 'Tens analgesico Drive', '1083': 'Inodoro Portatil 3 en 1', '790': 'Producto: Vaso adaptado para silla de ruedas -CENAREC-.', '146': 'Servicios ocupacionales.', '6': 'Ortopédia.', '1104': 'Mascarilla para nebulizar', '323': 'LIGA THERA-BAND NEGRO', '750': 'Producto: Software Controlador Mouse -CENAREC-.', '1061': 'Inmovilizador tobillo alto', '1019': 'Relleno anterior y corslette pierna', '582': 'Prod. Baston bola giratoria', '315': '', '1052': 'Elevador inodoro sin brazos', '553': 'Prod. Mouse Big track switch', '117': 'Educación Especial', '1207': 'Elevador tina', '630': 'Prod. Andaderas', '809': 'Producto: Lapicero Ergonómico -CENAREC-.', '676': 'Producto: Powerlink -CENAREC-.', '229': 'Bola de gel para mano', '647': 'Prod. Bastón de 4 puntas', '453': 'Producto: medidor de insulina', '278': 'LIGA THERA-BAND AZUL', '516': 'Producto: reloj despertador de mesa con voz español', '291': 'Electrodo pals cuadrado 2 x 2', '327': 'ELECTRODO THERATRODE 1.5 X 3.5', '1114': 'Muleta Antebrazo', '3': 'Terapia de Lenguaje', '1032': 'Muleta axilar.', '766': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.', '950': 'Prod. Audifono para móvil', '528': 'Producto: reloj braille para hombre seiko', '956': 'Prod. Sistema BAHA Attract', '795': 'Producto: Software Programa de reconocimiento de voz - CENAREC-.', '850': 'Producto: Silla Ruedas simple -CENAREC-.', '228': 'Muletas', '225': 'Soporte rotuliano', '513': 'Producto: rompecabezas de mascotas con sonidos', '555': 'Prod. Teclado para computador Big Blu', '121': 'Educación Musical', '1152': 'Venta producto de apoyo - Elevador de Sanitario con brazos', '493': 'Producto: bastón grafito baja visión o no videntes', '810': 'Producto: Vaso con tapa y pajilla -CENAREC-.', '1205': 'Salvaescalera HL350', '853': 'Producto: Conmutador por luz infra-roja -CENAREC-.', '754': 'Producto: Sistema de montaje para conmutadores -CENAREC-.', '245': 'SILLA DE RUEDAS PARA Parálisis Cerebral', '21': 'Terapia Física', '105': 'Alquiler Médicos ByB - Sillas Ruedas', '496': 'Producto: teléfono inalámbrico con voz español', '230': 'Alquiler: Cama Hospitalaria', '860': 'Producto: Videoteléfono -CENAREC-.', '575': 'Prod. Software Boardmaker', '1003': 'Férulas Polipropileno niño', '182': 'Muñequera para esguince tradicional', '390': 'Prod. Silla inodoro', '762': 'Producto: Software Comunicación Aumentativa -CENAREC-.', '730': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '139': 'Taller Ebanistería', '632': 'Prod. gigante suero', '993': 'Protesis cardiacas biológica mec. mitrales', '251': 'ANDADERAS', '858': 'Producto: Mouse Roller Trackball -CENAREC-.', '713': 'Cuña ajustable -CENAREC-.', '692': 'Producto: Calzador de medias -CENAREC-.', '981': 'Ferula laminado resina niño', '657': 'PROTESIS PARA ARRIBA DE RODILLA', '367': 'Silla Baño Plástica', '129': ': Artes Plásticas', '862': 'Tenedor adaptado -CENAREC-.', '815': 'Producto: Mouse adaptado para conectar conmutadores -CENAREC-.', '424': 'Producto: lampara inteligente luz led', '1118': 'Silla Ruedas Reclinable escritorios pies elevables', '741': 'Producto: Pulsador Graba Mensaje audio -CENAREC-.', '113': 'Serv. Educativos', '1105': 'Barandal para inodoro', '708': 'Producto: Comunicador de 4 casillas -CENAREC-.', '650': 'SILLA DE RUEDAS DE 18 PULGADAS', '62': 'Centro de Atención Integral', '775': 'Producto: Computador operada mov. ojos -CENAREC-.', '830': 'Productos de apoyo: Pantalla Táctil Infrarroja -CENAREC-.', '770': 'Producto: Comunicador de 8 casillas con barrido -CENAREC-.', '341': 'BOLSA DE AGUA CALIENTE', '1065': 'Bastón Plegable', '599': 'Prod. Bastón 4 piernas de soporte', '1194': 'Alquiler producto de apoyo - Oximetro Digital', '231': 'Alquiler: Andaderas', '1166': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica 18 pulgadas', '1111': 'Concentradores de oxigeno', '764': 'Producto: Cubiertos adaptados con material moldeable -CENAREC-.', '1098': 'Gigante suero', '1047': 'Dona Espuma', '857': 'Producto: Mouse Roller Trackball -CENAREC-.', '414': 'Prod. Tobillera sin talón 2 vías', '779': 'Producto: Ayuda Táctil -CENAREC-.', '731': 'Producto: Cuchara y tenedor adaptados en estilo puño universal -CENAREC-.', '199': 'Plantillas de gel para pie', '586': 'Prod. Vara para medir para baja visión', '614': 'Prod. Baston gancho tipo marshmallow', '1084': 'silla brazo fijo, pies elevables', '357': 'Elevador de sanitario sin soportes', '989': 'Ortesis corta', '1181': 'Venta producto de apoyo - Esfigmomanometro Manual', '492': 'Producto: balanza de cocina con voz', '705': 'Producto: Escanea y lee cualquier libro o documento impreso -CENAREC-.', '57': 'Centro Atención Integral', '307': 'Electrodo pals', '1043': 'Muslera neopreno', '580': 'Prod. Mini Touchpad teclado', '434': 'Producto: bolsa lona apertura pacientes', '222': 'Gigante dos ganchos', '1093': 'Baston 4 puntos', '213': 'Corset toraco lumbar', '1075': 'Escalerilla 2 peldaños', '725': 'Producto: Conmutador Pulsador -CENAREC-.', '794': 'Producto: Puntero de cabeza -CENAREC-.', '386': 'Silla Baño con agarraderas', '896': 'Prótesis cardiacas mec. aórticas', '1156': 'Alquiler producto de apoyo - Mesa Puente Alimentos', '552': 'Baston aluminio identificacion plegable', '149': 'Faja sacrolumbar', '1049': 'Andadera con ruedas', '1172': 'Venta producto de apoyo - Barra Apoyo 24 pulgadas', '480': 'Producto: cuchara y tenedor personas con deficiencia cognitiva', '715': 'Producto: Comunicador de 2 casillas -CENAREC-.', '295': 'VENDA ELÁSTICA MEDLINE 2', '91': 'Ortopédia.', '1110': 'Talonera para piel de oveja', '1010': 'Prótesis de muslo', '899': 'Cateter balon intraaortico', '625': 'Prod. Bastón rígido fibra vidrio para niño', '519': 'Producto: medidor glucosa con voz en español', '602': 'Prod. Mouse Swiftpoint', '880': 'Ferula para pie niño', '926': 'Corset lona Lumbrosacro', '39': 'Terapia Física y Rehabilitación', '527': 'Producto: guía escritura tamaño carta', '71': 'Serv. Terapia Ocupacional', '432': 'Producto: cinta para medir en pulgadas baja visión', '1068': 'Rodillera con bisagras', '966': 'Ortesis Auditivas: Audífonos vía osea', '40': 'Serv. Educativos (Manualidades para la independencia)', '560': 'Prod. Software traduce braille', '832': 'Producto: Interfaz para baterías -CENAREC-.', '566': 'Prod. Maquina escribir braille - perkins', '217': 'Muletas canadienses', '337': 'COJÍN COXIS', '807': 'Producto: Conmutador con sensor de parpadeo de fibra óptica -CENAREC-.', '143': 'Servicios Educativos', '897': 'Prótesis cardiacas mec. mitrales', '727': 'Producto: Plato convencional adaptado con ventosas -CENAREC-.', '322': 'ELECTRODO VALUTRODE RECTANGULAR 2X4', '595': 'Prod. Set Geométrico en braille', '440': 'Producto: bastón movilidad aluminio hecho en CR', '429': 'Producto: reloj para mujer, con voz en español', '649': 'Prod. Muletas', '90': 'Psiquiatría', '717': 'Producto: Hojas Magnificadores -CENAREC-.', '483': 'Producto: juego de mesa tactil', '285': 'BOLSA DE AGUA CALIENTE PARA ENEMA', '313': 'VENDA ELÁSTICA 6 MEDLINE', '598': 'Prod. Bastón gancho metal deslizante', '185': 'Silla ruedas tipo escritorio', '43': 'Serv. Terapia Física', '239': 'Alquiler de Equipo Médico - Servicio Sanitario Portatil', '908': 'Quilla carbono adulto', '859': 'Producto: Mouse Trackball gigante -CENAREC-.', '330': 'ELECTRODO WANDY CON ADHESIVO', '202': 'Rodillera estabilizadora', '474': 'Producto: Grabadora audio digital voz clasica', '1072': 'Carretilla para oxigeno', '1088': 'Sillas Ruedas tipo inodoro', '134': ': Educación Especial', '1108': 'Baranda para cama', '49': 'Terapia Física', '769': 'Producto apoyo: Adaptación Lapicero -CENAREC-.', '378': 'Branadal para inodoro', '721': 'Producto: Calculadora teclas grandes -CENAREC-.', '299': 'Electrodo carbono 4 cm', '494': 'Producto: reloj para mujer con sintetizador de voz', '485': 'Producto: elevador manual pacientes', '877': 'Producto: Impresora Braille Enablin -CENAREC-.', '955': 'Prod. TV Streamer (transmisor)', '686': 'Producto: Mouse controlado mov. ojos -CENAREC-.', '714': 'Producto: Software Controlador Mouse -CENAREC-.', '41': 'Adecuación Curricular No Significativa', '538': 'Prod. Bastón soporte ajustable', '1175': 'Venta producto de apoyo - Barra Apoyo para baño', '36': 'Terapia de Lenguaje', '1190': 'Venta producto de apoyo - Muletas', '475': 'Producto: lampara inteligente luz dia r10 recargable', '449': 'Producto: cinta métrica con habla en español', '1128': 'Prod. Mesa Puente', '451': 'Producto: regletas plasticas escribir braille', '300': 'ELECTRODO TYCO 2', '382': 'Bidé plástico', '1037': 'Audifono tipo Intra auricular', '447': 'Producto: reloj cuadrado para caballero, con voz español', '1159': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica', '141': 'Apoyo Económico a las asociaciones vinculadas con el Tema de Discapacidad.', '951': 'Prod. Manos libres', '268': 'Corrector de Postura', '758': 'Producto: Conmutador Pulsador -CENAREC-.', '168': 'almohada antironquidos', '305': 'LIGA CANDO ROJO', '109': 'Centro Atención Integral', '685': 'Producto: Comunicador multinivel de 128 casillas -CENAREC-.', '260': 'Faja Lumbar (corset Lumbar)', '1131': 'Prod. Equipo oxigeno', '942': 'Prod. Tinnitool', '166': 'Bolsa orina para pierna', '1132': 'Alquiler de andadera', '884': 'Ferula laminado resina adulto', '248': 'CABESTRILLO', '32': 'Terapia Física', '29': 'Odontología', '930': 'Bastón', '226': 'Bide acero', '96': 'Centro Atención Integral', '826': 'Producto: Carcasa de Teclado -CENAREC-.', '1095': 'Pedal de ejercicio', '777': 'Dispositivo para colocar cilindros y botellas -CENAREC-.', '19': 'Terapia Física', '354': 'Prod. Trapecio Lumex', '361': 'Silla Ruedas - 18 pulgadas', '233': 'Alquiler: Muletas', '1073': 'Silla Baño especial', '1060': 'Silla Baño Obesos', '679': 'Producto: Mouse adaptado para conectar conmutadores -CENAREC-.', '789': 'Producto: Software Convierte la imagen de un texto -CENAREC-.', '1161': 'Venta producto de apoyo - Sillas Rueda Estandar 24 pulgadas', '836': 'Producto: Magnificador de pantalla para personas con baja visión -CENAREC-.', '55': 'Audiometría', '249': 'Muñequeras de soporte', '413': 'Prod. Faja Costal Mujer', '86': 'Centro de atención integral', '823': 'Productos de apoyo - CENAREC-. Abotonador', '1186': 'Venta producto de apoyo - Grúa Transporte Pacientes', '358': 'Bastón con sentadero', '1062': 'Bidet', '469': 'Producto: mouse ergonomico para PcD', '1120': 'Inmovilizador muñeca y antebrazo', '431': 'Producto: bastón movilidad aluminio', '397': 'Elevador de sanitario con soportes', '746': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.', '1187': 'Alquiler producto de apoyo - Grúa Transporte Pacientes', '223': 'Soporte cadera', '1198': 'Silla Salvaescalera PLA', '995': 'Cateter balon intraaortico', '97': 'Serv. Educación Especial', '565': 'Prod. Mini teclado', '164': 'Férula dedos', '1034': 'Audifono tipo vía osea', '675': 'Producto: Conmutador con sensor de proximidad -CENAREC-.', '827': 'Producto: Software de comunicación -CENAREC-.', '594': 'Prod. Material etiquetas braille', '190': 'almohada para dar de mamar', '506': 'Producto: lapicero en negrita', '365': 'Bastón 4 puntas', '635': 'Prod. Colchón de aire con compresor', '927': 'Corset Jewett', '111': 'Serv. Educativos', '567': 'Prod. Impresora etiquetas de medicamentos en Braille', '561': 'Prod. Duplicador Braille y táctil Maxi-form Impresora', '116': 'Terapia Física.', '749': 'Producto: Software emulador de Mouse -CENAREC-.', '252': 'ANDADERAS', '802': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.', '351': 'Bastón de 3 puntas', '1121': 'Balones terapéuticos', '562': 'Prod. Magnificador tipo bolsillo', '120': 'Artes Industriales', '398': 'Silla Ruedas con partes movibles', '254': 'Cojín coxis', '298': 'Tens anagelsico Drive', '904': 'Ferulas Polipropileno adulto', '814': 'Producto: Atril Madera -CENAREC-.', '1069': 'Sillas ruedas y andadera con ruedas', '132': ': Artes Industriales', '420': 'Tiflotecnología', '756': 'Producto: Sistema de montaje para conmutadores y otros dispositivos -CENAREC-.', '526': 'Producto: calculadora con voz en español', '1136': 'Venta producto de apoyo - Bastón de 4 puntos apoyo', '1176': 'Venta producto de apoyo - Nebulizador Adulto', '1016': 'Prótesis provisional abajo rodilla', '977': 'Ferula pie adulto', '874': 'Producto: Traductor de Braille a español (y otros idiomas) -CENAREC-.', '652': 'TOBILLERA DE BARRAS LATERALES', '503': 'Producto: reloj braille bolsillo para caballero', '403': 'Rodillera con regulación lateral', '389': 'Bastón una punta floreado', '975': 'Donación de equipo Técnico - Sillas Baño', '1124': 'Prod. Barra Cromada 18 pulgadas', '481': 'Producto: grabadora audio digital olympus', '106': 'Alquiler Médicos ByB - Muletas', '1055': 'Rodillera elastica', '1004': 'Quilla Carbono adulto', '216': 'Muslera', '433': 'Producto: alta voz manos libres', '617': 'Prod. Bastón guia plegable', '772': 'Producto: Software Lector de pantalla para personas ciegas o con baja visión -CENAREC-.', '372': 'Bastón una punta no vidente', '782': 'Vaso con tapa -CENAREC-.', '428': 'Producto: bastón de apoyo ajustable', '159': 'Tobillera', '26': 'Nutrición', '1002': 'Férulas Polietileno niño', '1170': 'Venta producto de apoyo - Vaso Humidificador', '522': 'Producto: rompecabezas de numeros en relieve y braille', '613': 'Prod. Cuadro álgebra táctil', '486': 'Producto: máquina inteligente braille con video perkins', '872': 'Producto: Escaner de palabras -CENAREC-.', '1139': 'Venta producto de apoyo - Camilla para Masajes', '1001': 'Férulas Polietileno adulto', '760': 'Producto: Comunicador Múltiple -CENAREC-.', '1113': 'Vaso humificador', '204': 'Bide plástico', '631': 'Prod. Sillas de ruedas no ortopédicas', '1119': 'Grúa levanta personas', '1044': 'Cama Ortopedica Electrica', '636': 'Prod. Mesa Puente', '1129': 'Prod. Grúa Hidráulica', '416': 'Tiflotecnología - Papel para Imprimir Braille', '247': 'Almohada Ortopédica', '1179': 'Venta producto de apoyo - Tanque Oxigeno 685 L', '408': 'Rodillera con barras laterales, tallas: s, m', '461': 'Producto: rompecabezas instrumentas sonidos', '501': 'Producto: guia lectura para firmar', '279': 'ELECTRODO WANDY CON ADHESIVO', '781': 'Producto: Generador de comunicadores de 7 niveles -CENAREC-.', '11': 'Terapia Ocupacional', '131': ': Terapía Lenguaje', '1109': 'Andaderas con 4 ruedas', '873': 'Producto: Touchpad mouse -CENAREC-.', '935': 'Collar Cervical Blando', '934': 'Andadera', '911': 'Quilla madera niño', '606': 'Papel Swell Touch', '107': 'Terapia Ocupacional', '281': 'VENDA COBAN DUKAL 3 ADHESIVA', '1165': 'Alquiler producto de apoyo - Sillas Rueda Estándar 20 pulgadas', '1045': 'Muñequera', '949': 'Prod. Manos libres inalambrico', '22': 'Terapia de Lenguaje', '637': 'Prod. Cama ortopedica', '678': 'Producto: Beberito con tapa -CENAREC-.', '283': 'Prod. Liga Theraband roja', '531': 'Prod. Puntero Slip-on Bola', '1106': 'Bastón de punto fijo', '160': 'Cuellos cervicales blando', '982': 'Ferula ortoplast adulto', '1053': 'Cuello cervical de espuma', '102': 'Alquiler Médicos ByB - Silla Baño', '651': 'FAJA POSOPERATORIA S/M CONFORTA MEDICA.', '7': 'Fisioterapia', '521': 'Producto: bastón movilidad grafito y hule baja vision', '165': 'Compresas gel reusable', '757': 'Producto: Gateador -CENAREC-.', '1': 'Serv. Educativo: La biblioteca posee un programa, con cursos mejoramiento de motora fina, junto con la Trabajadora Social que busca mejorar la calidad de vida de la familia.', '94': 'Serv. Capacitación', '170': 'Silla para evacuar', '289': 'PASTA CONDUCTORA TEN20', '401': 'Silla Ruedas 18 pulgadas', '135': 'Serv. Apoyo Económico', '72': 'Casa Hogar Comunitario', '44': 'Centro atención integral.', '889': 'Prótesis Mamaría', '395': 'Silla de baño', '1133': 'Venta producto de apoyo - Colchón espuma 5 pulgadas', '920': 'Prótesis provisional abajo rodilla', '273': 'Arnés de Soporte en la silla de Ruedas para pacientes con PC.', '961': 'Prod. Mini micrófono', '145': 'Centro Diurno de Atención Integral', '435': 'Producto: calculadora científica con habla español', '426': 'Producto: bolsa fuerte para elevador pacientes', '399': 'ANDADERA C: SENTADERO KX', '321': 'ELECTRODO ULTRASTIM', '8': 'Psiquiatría', '1097': 'Almohada ortopedica', '892': 'Ortesis larga', '542': 'Prod. Teclado Learning Board', '1169': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica', '207': 'Cuña para espalda', '379': 'Silla Ruedas 20 pulgadas', '83': 'Ortopédia.', '169': 'Taloneras', '16': 'Centro Atención Integral', '844': 'Producto: APP para Iphone -CENAREC-.', '184': 'Medias terapeuticas para varices', '347': 'VENDA ADHESIVA DE COLORES 3', '801': 'Producto: Software Lectura de textos -CENAREC-.', '482': 'Producto: tazas de medida cocina con marcas braille', '722': 'Producto: Software Magnificador y lector de pantalla -CENAREC-.', '670': 'Salvaescalera Bisón', '288': 'BOLA TERAPÉUTICA PARA MANO PEQUEÑA', '104': 'Alquiler Médicos ByB - Cama Hospitalaria', '1155': 'Venta producto de apoyo - Mesa Puente Alimentos', '1174': 'Venta producto de apoyo - Arnes de Grúa', '648': 'Prod. Silla Ruedas con partes movibles', '998': 'Marcapaso unicameral', '1101': 'silla ruedas para solo transporte', '665': 'Salvaescalera Flow 2', '992': 'Protesis cardiacas biológica mec. aortica', '1204': 'Salvaescalera HL320', '587': 'Prod. Impresora y software para imprimir formas en braille', '468': 'Producto: Lapicero ergonómico PcD en la mano', '35': 'Terapia ocupacional', '114': 'Animales Equinoterapia - Animales Equinoterapia Costa Rica.', '53': 'Terapia Física', '88': 'Fisioterapia', '1160': 'Venta producto de apoyo - Sillas Rueda Estandar 20 pulgadas', '660': 'Ascensor Ecovimec', '1184': 'Venta producto de apoyo - Cama Hospitalaria Manual', '320': 'VENDA ELÁSTICA 4', '962': 'Ortesis Auditivas: Audífonos de Caja o Bolsillo', '1192': 'Venta producto de apoyo - Inodoro Portatil con rodines', '56': 'Terapia Ocupacional', '418': 'Tiflotecnología', '452': 'Producto: guia firma regular', '541': 'Prod. Mouse Ergo Trackball', '405': 'SOPORTE ELÁSTICO REFORZADO PARA TOBILLO', '444': 'Producto: reloj circular caballero voz español', '1171': 'Venta producto de apoyo - Barra Apoyo 32 pulgadas', '969': 'Teclado “Línea Braille”', '136': 'Terapia Ocupacional', '498': 'Producto: reloj braille caballero', '316': 'Cojín Lumbar', '101': 'Alquiler Médicos ByB - Servicio Sanitario Portatil', '181': 'Estetoscopio', '1183': 'Venta producto de apoyo - Cama Hospitalaria Semi Eléctrica', '828': 'Producto: Magnificador portátil -CENAREC-.', '206': 'Collar philadelphia', '459': 'Producto: medidor de presión arterial', '847': 'Producto: Reloj Digital con Sintesis y reconocimiento de voz-CENAREC-.', '564': 'Prod. Magnificador Onyx PC', '890': 'Lente intraocular', '335': 'VENDA ELÁSTICA 2 LE ROY 5CM x5MTS', '1031': 'Collar cervical blando.', '964': 'Ortesis Auditivas: Audífonos Intra-auricular', '293': 'COJIN DE ESPUMA Y GEL', '490': 'Producto: reloj ovalado metal para hombre 4 alarmas con habla español', '863': 'Tijeras Adaptadas -CENAREC-.', '740': 'Producto: Software permite crear, editar e imprimir plantillas -CENAREC-.', '571': 'Prod. Teclado Maxim', '709': 'Producto: Software Magnificador tipo lupa multiplataforma -CENAREC-.', '1074': 'Silla Baño Transferencia', '355': 'Gigante de suero', '971': 'Diccionario de Sinónimos', '785': 'Producto: Sistema de montaje para conmutadores y comunicadores livianos -CENAREC-.', '15': 'Serv. Educativos', '871': 'Producto Apoyo: Andadera con asiento y canasta -CENAREC-.', '81': 'Fisioterapia', '1071': 'Oximetro de pulso', '256': 'MULETAS', '127': ': Estimulación Temprana', '126': ': Terapia Física', '529': 'Producto: ábaco personas no videntes', '677': 'Producto: Pulsador con grabación de secuencias de mensajes -CENAREC-.', '783': 'Producto: Magnificador giratorio -CENAREC-.', '311': 'VENDA ELÁSTICA DE COLORES 2', '596': 'Prod. Puntero rover free wheeling', '654': 'INMOBILIZADOR DE DEDO PULGAR MUÑECA.', '739': 'Producto: Material Antideslizante -CENAREC-.', '900': 'Protesis cardiacas biológica aortica', '793': 'Producto: Mueble de posicionamiento supino -CENAREC-.', '907': 'Ferulas Polipropileno niño', '318': 'ELECTRODO WANDY CON ADHESIVO', '59': 'Serv. Terapia Física', '788': 'Producto: Dispositivo limpiarse al usar el inodoro -CENAREC-.', '66': 'Servicio asistencia económica para pacientes en fase terminal', '1203': 'Salvaescalera OP', '1077': 'Almohada para CPAC', '581': 'Prod. Bastón gancho cerámica', '669': 'Salvaescalera Homeglide extra', '110': 'Serv. Educativos', '697': 'Producto: Mouse tipo “joystick” -CENAREC-.', '747': 'Producto: Conmutador doble para lengua, mentón o mejilla -CENAREC-.', '1196': 'Silla Salvaescalera BSK', '784': 'Conmutador de tipo pulsador -CENAREC-.', '425': 'Producto: Reloj para mujer con voz en español y pantalla para baja visión, banda de caucho', '668': 'Salvaescalera Capri', '1030': 'Andadera especializada según direcciones técnicas.', '924': 'mano con guante cosmetico', '663': 'Salvaescalera Platinium', '673': 'Producto: Generador de comunicadores -CENAREC-.', '642': 'Prod. Andaderas', '1026': 'Bastón especializada según direcciones técnicas.', '31': 'Psicología', '287': 'Anillo rotuliano', '601': 'Prod. Puntero gancho alto kilometraje', '138': 'Serv. Educativos', '128': ': Música', '812': 'Producto: Software Emulador de Teclado Virtual -CENAREC-.', '693': 'Producto: Sistema de montaje para comunicadores -CENAREC-.', '119': 'Educación para el Hogar', '1144': 'Venta producto de apoyo - Aspirador de Flemas', '227': 'Almohada termica', '98': 'Serv. Gestión y canalización de fondos para proyecto de bien social.', '158': 'Antifaz para dormir', '559': 'Prod. Impresora Braille - Braillo 300', '1102': 'Bolsas para agua caliente', '592': 'Prod. Baston plegable fibra vidrio', '616': 'Prod. Bloque bolsillo para aprender braille', '589': 'Prod. Mouse Adaptado con switch', '1048': 'Silla Baño con respaldo asiento en U', '1023': 'Corset Jewett', '867': 'Producto: Teclado de conceptos con conexión USB - CENAREC-.', '593': 'Prod. Mouse Slimblade trackball', '588': 'Prod. Bandeja actividades', '886': 'Ferula ortoplast adulto', '417': 'Tiflotecnología', '156': 'Termometro axilar digital', '882': 'Ferula para mano antiespasmica', '1067': 'Barra Cromada 32 pulgadas', '842': 'Producto: Mueble de posicionamiento prono -CENAREC-.', '535': 'Prod. Handshoe mouse', '495': 'Producto: rompecabezas animales de granja en braille', '421': 'Tiflotecnología', '716': 'Producto: Comunicador multinivel de 32 casillas -CENAREC-.', '402': 'Ortesis de hombro - talla: s, m, l', '816': 'Producto: Reloj braille -CENAREC-.', '477': 'Producto: cargador portátil energía solar', '193': 'Máscara Nebulizador pediatrico', '861': 'Producto: Dispositivo para lectura automática -CENAREC-.', '1143': 'Alquiler Gigante para Suero', '374': 'Silla de baño sin respaldo', '629': 'Prod. Cama ortopedica', '590': 'Prod. Bastón plegable para soporte', '1092': 'Silla Ruedas sencilla', '1208': 'Plataforma vertical STA-FLE', '215': 'Cojin lumbar', '532': 'Prod. Material desarrollo motora fina', '510': 'Producto: reloj braille para mujer', '211': 'Glucometros digitales', '1126': 'Prod. Muleta Universal', '976': 'Ferula pie niño', '680': 'Producto: Magnificador portátil -CENAREC-.', '906': 'Ferulas Polietileno niño', '931': 'Muleta canadiense', '439': 'Producto: lupa con luz LED 2 en 1', '712': 'Producto: Sintetizador de voz con Teclado Portátil Braille tipo Perkins -CENAREC-.', '1018': 'Zapato ortopedico bajo molde yeso niño', '205': 'Andadera con asiento', '517': 'Producto: lupa electronica hd de bolsillo', '524': 'Producto: guia para firmar con lupa', '1089': 'Inodoro Portatil 3 en 1 con ruedas', '797': 'Producto Apoyo: Andadera -CENAREC-.', '74': 'Centro Atención Integral', '923': 'Relleno anterior y corslette pierna', '240': 'Alquiler camas ortopedicas', '689': 'Producto: Despertador vibratorio Hal-Hen -CENAREC-.', '462': 'Producto: reloj para caballero con sintetizador de voz', '611': 'Prod. Prod. Material desarrollo de habilidades', '591': 'Prod. Impresora Braille Box', '499': 'Producto: elevador eléctrico pacientes', '325': 'FÉRULA DE DEDO ALUMINIO', '929': 'Corset Milwalke', '194': 'almohada ortopedica', '626': 'Prod. Teclado Portátil', '304': 'COLCHONETA KINDER Y GIMNASIO VINIL', '488': 'Producto: lupa de mano con luz integrada', '54': 'Fisioterapia', '771': 'Producto: Software juego interactivos par Personas con Autismo -CENAREC-.', '729': 'Producto: Mesa Reclinable -CENAREC-.', '518': 'Producto: magnificador de imágenes portatil 1.5x - 25x', '244': 'Collar de Thomas', '843': 'Producto: Magnificador digital de bolsillo -CENAREC-.', '17': 'Terapia Física', '799': 'Producto: Conmutador con sensor de movimientos musculares -CENAREC-.', '914': 'Prótesis muslo', '864': 'Producto: Software Emulador de mouse -CENAREC-.', '48': 'Terapia de Lenguaje', '710': 'Comunicador con 7 casillas -CENAREC-.', '235': 'Alquiler de Equipo Médico - Silla Baño', '856': 'Conmutador para apretar -CENAREC-.', '491': 'Producto: set geometria tactiles y alto contraste', '24': 'Psicología', '879': 'Producto: Teclado de colores - CENAREC-.', '990': 'Ortesis cables flexibles articulados (par)', '999': 'Silla Ruedas Especializadas', '376': 'Bastón de una punta, diferentes colores', '186': 'Barra para baño', '1051': 'Barra Cromada 24 pulgadas', '255': 'Botas Inmovilizadoras con Aire. (Férula Tipo Walker)', '888': 'Prótesis ocular', '620': 'Prod. Puntero Slip-on tipo lápiz', '153': 'Fajas inguinales', '1079': 'Ejercitador de mano', '406': 'SOPORTE ESCROTAL ATLÉTICO', '237': 'Alquiler de Equipo Médico - Silla de Ruedas', '752': 'Producto: conmutador juguetes -CENAREC-.', '67': 'Servicio alquiler o préstamo de sillas ruedas no ortopedicas.', '733': 'Producto: Software permite creación y personalización actividades didácticas - CENAREC-.', '922': 'Zapato ortopedico bajo molde yeso niño', '643': 'Prod. Colchón de agua', '446': 'Producto: rompecabezas de formas y colores', '338': 'LIGA THERA-BAND VERDE', '60': 'Serv. Apoyo Legal', '5': 'Asesoría técnica sobre petición de ayudas o procedimientos estatales.', '1078': 'Silla Brazo Fijo pies desmontable', '302': 'COMPRESA FRÍO CALOR PARA CERVICAL Y HOMBROS', '700': 'Producto: Software Emulador de Mouse -CENAREC-.', '852': 'Producto: Software Emulador que permite escribir Windows -CENAREC-.', '191': 'Pantorrillera', '500': 'Producto: juego dominó piezas grandes diseño animales', '214': 'Protector de gel para dedo pulgar', '1123': 'Rodillera con rotula', '800': 'Producto: Conmutador inalámbrico de tipo pulsador -CENAREC-.', '765': 'Producto: Software Emulador Mouse -CENAREC-.', '363': 'Silla transporte 19 pulgadas color azul', '994': 'Protesis cardiacas biológica mitral', '985': 'Prótesis Mamaría', '64': 'Serv. Educativos', '694': 'Producto: Mouse con laser -CENAREC-.', '674': 'Producto apoyo: Alimentador Electrónico -CENAREC-.', '1025': 'Corset Milwalke', '667': 'Salvaescalera Ischia', '699': 'Producto: Monitor inalámbrico para bebés -CENAREC-.', '92': 'Terapia del lenguaje, habla y voz', '253': 'ANDADERAS', '939': 'Audifono Retro auricular', '878': 'Producto: Reloj digital parlante -CENAREC-.', '1147': 'Producto de apoyo - Venta Compresor Oxigeno New Life Elite', '197': 'Canula de oxigeno nasal', '738': 'Producto: Impresora Braille -CENAREC-.', '1202': 'Salvaescalera', '1038': 'Estabilizador universal pulgar', '280': 'COJÍN DE ESPUMA', '833': 'Producto: Software Conversor texto a audio -CENAREC-.', '1197': 'Silla Salvaescalera A180', '265': 'Estabilizador de Tobillo', '410': 'Prod. Faja Costal', '545': 'Prod. Calendario aula', '115': 'Asistencia Médica Gratuita', '819': 'Producto: Conmutador de tipo pulsador con conector USB -CENAREC-.', '891': 'Ortesis al tercio', '192': 'Bola para terapia diferentes tamaños', '1012': 'Zapato ortopedico bajo molde yeso adulto', '1177': 'Venta producto de apoyo - Nebulizador Niño', '724': 'Producto: Editor de textos Braille - CENAREC-.', '441': 'Producto: reloj para mujer diseño elegante con voz español y bicolor', '732': 'Producto: Perilla Universal -CENAREC-.', '656': 'CORSE JEWET', '615': 'Prod. Reloj Parlante y braille, oro, para hombre', '577': 'Prod. Bastón plegable de grafito', '1141': 'Venta producto de apoyo - Bidet Acero', '933': 'Collar duro tipo thomas', '661': 'Ascensor Celsus'}

    item_name = get_item_name(text)

    classifications = get_service_classification(text)

    for key, value in names.items():
        value = str(value)
        if value == item_name:
            print("-VALUE HIT-")
            if classifications != []:
                for classification in classifications:
                    line = str(line + str(key) + "|" + str(classification) + "+")

            else:
                line = str(line + str(key) + "|18+")

    print(line)
    return line


def generate_classification_superString(serviceMatrix):
    superString = ""
    for i in range(len(serviceMatrix)):
        path = serviceMatrix[i][0]
        # print(path)
        text = get_text_from(path , False)

        superString = superString + generate_sectorClassifications_line(text)


    print(superString)
    return superString


def get_service_orgIdFk(text):
    names = {'53': 'Alquiler Médicos ByB - Servicio Sanitario Portatil', '43': 'Casa Hogar Comunitario', '40': 'Servicio alquiler o préstamo de Camas Hospitalarias.', '3': 'Terapia de Lenguaje', '78': ': Psicología', '10': 'Alquiler sillas de ruedas.', '84': 'Servicios Educativos', '74': ': Artes Plásticas', '20': 'Servicio de audiología en general con fabricación de audífonos.', '54': 'Alquiler Médicos ByB - Silla Baño', '86': 'Centro Diurno de Atención Integral', '48': 'Serv. Capacitación', '82': 'Serv. Asesoría Legal', '26': 'Apoyos Didácticos', '44': 'Serv. Apoyo Emocional', '23': 'Terapia Física y Rehabilitación', '17': 'Nutrición', '36': 'Centro educativo - Educación especial curricular.', '80': 'Serv. Apoyo Económico', '33': 'Audiometría', '65': 'Artes Industriales', '49': 'Serv. Educación Especial', '55': 'Alquiler Médicos ByB - Andaderas', '14': 'Centro Atención Integral', '88': 'Ser. alquiler camas ortopedicas', '46': 'Centro de atención integral', '61': 'Terapia Física.', '66': 'Educación Musical', '63': 'Hogar de cuido para personas con parálisis cerebral en situación de abandono', '58': 'Alquiler Médicos ByB - Muletas', '70': 'Terapia de lenguaje', '87': 'Servicios ocupacionales.', '19': 'Odontología', '71': ': Terapia Física', '81': 'Taller Ebanistería', '1': 'Serv. Educativo: La biblioteca posee un programa, con cursos mejoramiento de motora fina, junto con la Trabajadora Social que busca mejorar la calidad de vida de la familia.', '16': 'Terapia ocupacional', '38': 'Servicio alquiler o préstamo de sillas ruedas no ortopedicas.', '75': ': Educación Física', '47': 'Terapia del lenguaje, habla y voz', '34': 'Serv. Apoyo Legal', '62': 'Educación Especial', '72': ': Estimulación Temprana', '35': 'Centro de Atención Integral', '57': 'Alquiler Médicos ByB - Sillas Ruedas', '59': 'Animales Equinoterapia - Animales Equinoterapia Costa Rica.', '50': 'Serv. Gestión y canalización de fondos para proyecto de bien social.', '89': 'Serv. Ocupacionales de Recreo', '22': 'Enseñanza de Lesco', '79': ': Educación Especial', '12': 'Audiometrías', '30': 'Presupuesto para apoyar ONG’S que atienden personas con discapacidad en el Cantón.', '64': 'Educación para el Hogar', '56': 'Alquiler Médicos ByB - Cama Hospitalaria', '9': 'Terapia Física', '73': ': Música', '77': ': Artes Industriales', '32': 'Serv. Educativos.', '25': 'Adecuación Curricular No Significativa', '51': 'Capacitaciones a personas, entidades privadas o públicas en el cantón.', '13': 'Serv. Educativos', '42': 'Serv. Terapia Ocupacional', '15': 'Capacitaciones', '18': 'Trabajo Social', '39': 'Serv. Alquiler de Andaderas', '6': 'Ortopédia.', '5': 'Asesoría técnica sobre petición de ayudas o procedimientos estatales.', '45': 'Serv. Equinoterapia', '85': 'Servicios educativos.', '52': 'Formación Humana', '11': 'Terapia Ocupacional', '29': 'Serv. educativos', '8': 'Psiquiatría', '2': 'Psicología', '21': 'Estimulación Temprana', '4': 'Asesoría Emocional', '83': 'Apoyo Económico a las asociaciones vinculadas con el Tema de Discapacidad.', '24': 'Serv. Educativos (Manualidades para la independencia)', '68': 'Artes Plásticas', '60': 'Asistencia Médica Gratuita', '41': 'Serv. Alquiler de Muletas', '69': 'Terapia física', '31': 'Serv. Educativos: Manualidades.', '76': ': Terapía Lenguaje', '37': 'Servicio asistencia económica para pacientes en fase terminal', '27': 'Serv. Terapia Física', '7': 'Fisioterapia', '67': 'Educación Física', '28': 'Centro atención integral.'}
    needle = str(get_item_name(text))
    print(needle)
    for key, value in names.items():
        value = str(value)
        if value == needle:
            print("\t\033[94morganizationsIdFk:\033[0m " + key)
            return key

    print("\t\u001B[31morganizationsIdFk:\033[0m ERROR")
    return 100


# ------------------------------------REGIONS------------------------------------ #

def get_region_product(text): # TODO esta es la vara mas ineficiente del mundo
    if text.find("Localización del servicio de apoyo") == -1:
        haystack = text[text.find("Indique los siguientes datos del lugar donde se ubica"): text.find("Redes sociales")]
    else:
        haystack = text[text.find("Localización del servicio de apoyo") : text.find("Redes sociales")]
    start = "Provincia:"
    mid = "Cantón:"
    mid2 = "Distrito:"
    end = "Dirección exacta"

    provincia = haystack[haystack.find(start) + len(start): haystack.find(mid)]
    canton = haystack[haystack.find(mid) + len(mid): haystack.find(mid2)]
    distrito = haystack[haystack.find(mid2) + len(mid2): haystack.find(end)]

    provincia = provincia.replace("\n", " ")
    provincia = provincia.replace("\t", " ")
    provincia = re.sub(' +', ' ', provincia)
    provincia = provincia.rstrip()
    provincia = provincia.lstrip()
    provincia = provincia.replace("\'", "")
    provincia = provincia.replace("'", "")
    provincia = provincia.replace("\"", "")
    provincia = provincia.replace(".", "")
    if provincia == "":
        provincia = "No brinda información."

    canton = canton.replace("\n", " ")
    canton = canton.replace("\t", " ")
    canton = re.sub(' +', ' ', canton)
    canton = canton.rstrip()
    canton = canton.lstrip()
    canton = canton.replace("\'", "")
    canton = canton.replace("'", "")
    canton = canton.replace("\"", "")
    canton = canton.replace(".", "")
    if canton == "":
        canton = "No brinda información."

    distrito = distrito.replace("\n", " ")
    distrito = distrito.replace("\t", " ")
    distrito = re.sub(' +', ' ', distrito)
    distrito = distrito.rstrip()
    distrito = distrito.lstrip()
    distrito = distrito.replace("\'", "")
    distrito = distrito.replace("'", "")
    distrito = distrito.replace("\"", "")
    distrito = distrito.replace(".", "")
    if distrito == "":
        distrito = "No brinda información."

    if haystack.find(start) == -1:
        provincia = "No brinda información."

    if haystack.find(mid) == -1:
        canton = "No brinda información."

    if haystack.find(mid2) == -1:
        distrito = "No brinda información."

    print("\t\033[94mProvincia:\033[0m " + provincia + " \033[94mCantón:\033[0m " + canton + " \033[94mDistrito:\033[0m " + distrito)
    return str(provincia + "|" + canton + "|" + distrito)


def get_region_service(text): # TODO esta es la vara mas ineficiente del mundo
    haystack = ""
    if text.find("Localización del servicio de apoyo") == -1:
        haystack = text[text.find("Indique los siguientes datos del lugar donde se ubica"): text.find("Redes sociales")]
    else:
        haystack = text[text.find("Localización del servicio de apoyo") : text.find("Redes sociales")]



    start = "Provincia:"
    mid = "Cantón:"
    mid2 = "Distrito:"
    end = "Dirección exacta"

    provincia = haystack[haystack.find(start) + len(start): haystack.find(mid)]
    canton = haystack[haystack.find(mid) + len(mid): haystack.find(mid2)]
    distrito = haystack[haystack.find(mid2) + len(mid2): haystack.find(end)]

    provincia = provincia.replace("\n", " ")
    provincia = provincia.replace("\t", " ")
    provincia = re.sub(' +', ' ', provincia)
    provincia = provincia.rstrip()
    provincia = provincia.lstrip()
    provincia = provincia.replace("\'", "")
    provincia = provincia.replace("'", "")
    provincia = provincia.replace("\"", "")
    provincia = provincia.replace(".", "")
    if provincia == "" or provincia == "-":
        provincia = "No brinda información."

    canton = canton.replace("\n", " ")
    canton = canton.replace("\t", " ")
    canton = re.sub(' +', ' ', canton)
    canton = canton.rstrip()
    canton = canton.lstrip()
    canton = canton.replace("\'", "")
    canton = canton.replace("'", "")
    canton = canton.replace("\"", "")
    canton = canton.replace(".", "")
    if canton == "" or canton == "-":
        canton = "No brinda información."

    distrito = distrito.replace("\n", " ")
    distrito = distrito.replace("\t", " ")
    distrito = re.sub(' +', ' ', distrito)
    distrito = distrito.rstrip()
    distrito = distrito.lstrip()
    distrito = distrito.replace("\'", "")
    distrito = distrito.replace("'", "")
    distrito = distrito.replace("\"", "")
    distrito = distrito.replace(".", "")
    if distrito == "" or distrito == "-":
        distrito = "No brinda información."

    if haystack.find(start) == -1:
        provincia = "No brinda información."

    if haystack.find(mid) == -1:
        canton = "No brinda información."

    if haystack.find(mid2) == -1:
        distrito = "No brinda información."

        print(
            "\t\033[94mProvincia:\033[0m " + provincia + " \033[94mCantón:\033[0m " + canton + " \033[94mDistrito:\033[0m " + distrito)
    return str(provincia + "|" + canton + "|" + distrito)


def build_region_product(text):
    return get_org_name_product(text) + "|" + get_region_product(text)


def build_region_service(text):
    return get_org_name_service(text) + "|" + get_region_service(text)


def generate_region_superString(serviceMatrix , productMatrix):
    superString = ""
    ready = []
    for i in range(len(serviceMatrix)):
        path = serviceMatrix[i][0]
        print(path)
        text = get_text_from(path , False)
        orgName = get_org_name_service(text)

        if orgName not in ready:
            superString = superString + str(build_region_service(text) + "+")
            ready = ready + [orgName]

    for i in range(len(productMatrix)):
        path = productMatrix[i][0]
        print(path)
        text = get_text_from(path , False)
        orgName = get_org_name_product(text)

        if orgName not in ready:
            superString = superString + str(build_region_product(text) + "+")
            ready = ready + [orgName]

    print(superString)
    return superString


def check_iso_products(productMatrix):
    needleClase = ": Clase: "
    needleSubclase = " Subclase: "
    end = " Productos de apoyo para "
    superString = ""
    for i in range(len(productMatrix)):
        path = productMatrix[i][0]
        text = get_text_from(path , False)
        haystack = text[text.find("ISO 9999:2011") + 13:]
        clase = haystack[haystack.find(needleClase) + len(needleClase): haystack.find(needleSubclase)][:3]
        subclase = haystack[haystack.find(needleSubclase) + len(needleSubclase):][:4]
        classText = haystack[haystack.find(": Clase: ") + 12 : haystack.find(" Subclase: ")]
        subtext = haystack[haystack.find(" Subclase: ") + 14 :]
        # print("\033[94mISO 9999:\033[0m\n\tclase: " + clase + "\tclass text: " + classText + "\tsubclase: " + subclase[:2] + "\tdivision: " + subclase[2:] + "\tsubtext: " + subtext)
        print(haystack)


# ------------------------------------ADDRESS------------------------------------ #

def get_address(text): # TODO esta es la vara mas ineficiente del mundo
    haystack = ""
    if text.find("Localización del servicio de apoyo") == -1:
        haystack = text[text.find("Indique los siguientes datos del lugar donde se ubica"): text.find("Redes sociales")]
    else:
        haystack = text[text.find("Localización del servicio de apoyo") : text.find("Redes sociales")]

    start = "Dirección exacta:"
    end = "telelelelele"

    needle = haystack[haystack.find(start) + len(start): haystack.find(end)]
    needle = needle.replace("\n", " ")
    needle = needle.replace("\t", " ")
    needle = re.sub(' +', ' ', needle)
    needle = needle.rstrip()
    needle = needle.lstrip()
    needle = needle.replace("\'", "")
    needle = needle.replace("'", "")
    needle = needle.replace("\"", "")

    if haystack.find(start) == -1:
        needle = "No brinda información."

    print("\t\033[94mAddress:\033[0m " + needle)
    return str(needle)


def build_address_product(text):
    return get_org_name_product(text) + "|" + get_address(text)


def build_address_service(text):
    return get_org_name_service(text) + "|" + get_address(text)


def generate_address_superString(serviceMatrix , productMatrix):
    superString = ""
    ready = []
    for i in range(len(serviceMatrix)):
        text = get_text_from(serviceMatrix[i][0] , False)
        orgName = get_org_name_service(text)

        if orgName not in ready:
            superString = superString + str(build_address_service(text) + "+")
            ready = ready + [orgName]

    for i in range(len(productMatrix)):
        text = get_text_from(productMatrix[i][0], False)
        orgName = get_org_name_product(text)

        if orgName not in ready:
            superString = superString + str(build_address_product(text) + "+")
            ready = ready + [orgName]

    print(superString)
    return superString


# ------------------------------------ GROUPS ------------------------------------ #

def get_product_group(text):
    haystack = text[text.find("Uso y aplicaciones del producto de apoyo") + 40 : text.find("ISO 9999")].replace(":" , "")

    print(haystack)

    needle_movilidad = "Es apoyo para la movilidad ("
    needle_educativo = ") Entorno educativo ("
    needle_recreacion = "Recreación ("
    needle_deporte = ") Deporte ("
    needle_salud = ") Salud ("
    needle_laboral = ") Laboral ("
    needle_actividades = ") Para actividades de la vida diaria básicas o Instrumentales ("
    needle_varios = ") Otros: ("
    end = ") (indicar información que permita"

    movilidad = haystack[haystack.find(needle_movilidad) + len(needle_movilidad) : haystack.find(needle_educativo)].replace("X" , "x").replace(" " , "")
    educativo = haystack[haystack.find(needle_educativo) + len(needle_educativo) : haystack.find(needle_recreacion)].replace("X" , "x").replace(" " , "")
    recreacion = haystack[haystack.find(needle_recreacion) + len(needle_recreacion) : haystack.find(needle_deporte)].replace("X" , "x").replace(" " , "")
    deporte = haystack[haystack.find(needle_deporte) + len(needle_deporte) : haystack.find(needle_salud)].replace("X" , "x").replace(" " , "")
    salud = haystack[haystack.find(needle_salud) + len(needle_salud) : haystack.find(needle_laboral)].replace("X" , "x").replace(" " , "")
    laboral = haystack[haystack.find(needle_laboral) + len(needle_laboral) : haystack.find(needle_actividades)].replace("X" , "x").replace(" " , "")
    actividades = haystack[haystack.find(needle_actividades) + len(needle_actividades) : haystack.find(needle_varios)].replace("X" , "x").replace(" " , "")
    varios = haystack[haystack.find(needle_varios) + len(needle_varios): haystack.find(end)].replace("X" , "x").replace(" " , "")

    # print(movilidad , educativo , recreacion , deporte , salud , laboral , actividades , varios)
    groups = []

    if movilidad == "x":
        groups.append(7)

    if educativo == "x":
        groups.append(11)

    if recreacion == "x":
        groups.append(9)

    if deporte == "x":
        groups.append(10)

    if salud == "x":
        groups.append(4)

    if laboral == "x":
        groups.append(6)

    if actividades == "x":
        groups.append(1)
        groups.append(2)
        groups.append(3)

    if varios == "x" or varios == "":
        groups.append(13)

    return groups


def generate_group_line(text):
    line = ""
    names = {'1063': 'Almohada de aire', '259': 'Zapato Ortopédico', '95': 'Serv. Educación Especial',
             '798': 'Producto: Software escribir con leves movimientos de mouse -CENAREC-.',
             '179': 'Masajeador corporal', '294': 'VENDA ELÁSTICA PARA TOBILLO VENTILADA',
             '623': 'Prod. Maquina escribir braille perkins', '140': 'Serv. Asesoría Legal',
             '1022': 'Corset Lona lumbrosacro', '346': 'COJÍN CILINDRO',
             '612': 'Prod. Impresora Braille Juliet pro', '1100': 'Andadera Plegable Bariatrica',
             '1011': 'Prótesis de brazo', '250': 'Cojín lumbar',
             '687': 'Producto: Cuchara con desviación izquierda -CENAREC-.', '419': 'Tiflotecnología',
             '546': 'Prod. Balón soccer con campanas', '530': 'Prod. Cubiertas poly',
             '608': 'Prod. Reloj para aprender la hora', '25': 'Terapia Ocupacional',
             '773': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.',
             '944': 'Prod. Transmisor audio de TV', '619': 'Prod. Puntero gancho tipo rodillo',
             '99': 'Capacitaciones a personas, entidades privadas o públicas en el cantón.',
             '726': 'Producto apoyo: Adaptador Monitor Táctil -CENAREC-.',
             '1185': 'Venta producto de apoyo - Cama Hospitalaria Full Eléctrica', '388': 'Colchón de aire',
             '1021': 'Mano tipo garfio', '1027': 'Muleta canadiense.', '356': 'Silla Baño con respaldar',
             '1115': 'Compresas frio calor', '80': 'Audiometrías', '183': 'Masajeador facial',
             '912': 'Prótesis ante brazo', '371': 'Prod. Silla inodoro', '220': 'Férula antiespastica',
             '887': 'Prótesis ocular individualizada',
             '508': 'Producto: reloj despertador mesa con voz español numero grandes',
             '639': 'Prod. Inodoro portátil', '938': 'Audifono via osea',
             '813': 'Producto: Mesa y silla para trabajo -CENAREC-.',
             '319': 'Prod. Electrodo pals redondo 2 pulgadas', '954': 'Audífonos', '909': 'Quilla madera adulto',
             '698': 'Producto: Mouse tipo “joystick” -CENAREC-.', '125': 'Terapia de lenguaje',
             '1000': 'Férulas Polipropileno adulto',
             '719': 'Producto: Software Permite imprimir gráficos en relieve y Braille -CENAREC-.',
             '511': 'Producto: silla plegable de baño', '12': 'Psiquiatría', '1005': 'Quilla madera adulto',
             '848': 'Producto: Comunicador de 6 casillas con 5 niveles. -CENAREC-.',
             '767': 'Producto: Dispositivo que permite grabar un mensaje, aviso, noticia -CENAREC-.',
             '137': 'Centro Atención Integral', '353': 'Colchón de agua',
             '515': 'Producto: juego dominó piezas grandes',
             '1138': 'Venta producto de apoyo - Canula Nasal Adulto', '1099': 'Inmovilizador tobillo corto',
             '1039': 'Bandas de ejercicio',
             '818': 'Producto: Comunicador tipo Handheld de pantalla táct -CENAREC-.',
             '1085': 'Bolsa para agua fria', '1006': 'Quilla Carbono niño', '45': 'Serv. educativos',
             '666': 'Salvaescalera Homeglide', '883': 'Ferula ortoplast niño',
             '745': 'Producto: Cepillo de Dientes Adaptado -CENAREC-.',
             '507': 'Producto: regleta de aluminio para escribir', '174': 'Hombreras',
             '362': 'ANDADERA CON SENTADERA CON CANASTA', '958': 'Prod. Phone Clip', '23': 'Psiquiatría',
             '1112': 'Arnes para grua', '868': 'Producto: Destapador de botellas antideslizante -CENAREC-.',
             '943': 'Prod. Terapia ZEN', '558': 'Prod. Papel Braille', '377': 'Prod. Silla Ruedas con inodoro',
             '270': 'BASTON PLEGABLE', '664': 'Salvaescalera Elba',
             '1146': 'Producto de apoyo - Venta Compresor Oxígeno Visión Air',
             '735': 'Producto: Comunicador de 8 casillas -CENAREC-.', '450': 'Producto: reloj braille mujer seiko',
             '68': 'Serv. Alquiler de Andaderas', '257': 'Férulas de Mano para Túnel Carpal',
             '866': 'Producto: Software Emulador de Mouse -CENAREC-.', '646': 'Prod. Silla Baño con y sin respaldo',
             '103': 'Alquiler Médicos ByB - Andaderas', '1090': 'Tracción cervical',
             '46': 'Presupuesto para apoyar ONG’S que atienden personas con discapacidad en el Cantón.',
             '292': 'BOLA EJERCICIO 86 CM',
             '1134': 'Venta producto de apoyo - Colchón espuma impermeable 6 pulgadas',
             '236': 'Alquiler de Equipo Médico - Andaderas', '1117': 'Silla Baño sin respaldo',
             '895': 'Electrodos para marcapasos', '786': 'Producto: Mouse tipo Pulsador Casero -CENAREC-.',
             '980': 'Ferula laminado resina adulto', '384': 'Cama Ortopedica Manual', '1014': 'Cambio de socket',
             '167': 'Bastón con asiento', '918': 'Cambio de socket', '659': 'SILLA DE BAÑO CON AGARRADERAS',
             '1140': 'Venta producto de apoyo - Bastón de 1 punta apoyo',
             '841': 'Producto: Mouse para pie -CENAREC-.', '443': 'Producto: guia para firmar plastico regular',
             '940': 'Audifono Intra canal', '736': 'Producto: Computadora portatil táctil -CENAREC-.',
             '1007': 'Quilla madera niño', '27': 'Trabajo Social', '703': 'Producto: Bastón electrónico -CENAREC-.',
             '1029': 'Collar cervical tipo Thomas duro.', '130': ': Educación Física',
             '455': 'Producto: cuchara y tenedor con correa de vinil',
             '484': 'Producto: lupa pagina completa magnificadora 2x', '536': 'Prod. Juego Geométrico táctil',
             '296': 'Compresa fría', '662': '. Ascensor Acuático',
             '1151': 'Venta producto de apoyo - Elevador de Sanitario sin brazos',
             '569': 'Prod. Hover mounting kit', '718': 'Producto: Software Emulador teclado Virtual -CENAREC-.',
             '948': 'Prod. Baterías para Audífonos', '1080': 'Elevador de inodoro con brazos',
             '37': 'Estimulación Temprana', '51': 'Serv. Educativos.', '326': 'VENDA COBAN DUKAL 4 ADHESIVA PIE',
             '1122': 'Silla Baño con respaldo', '627': 'Prod. Papel Braillon',
             '258': 'Férulas de Mano para Túnel Carpal - Tendinitis', '271': 'BASTON DE 4 PUNTOS',
             '1178': 'Venta producto de apoyo - Tanque Oxigeno 1.699 L',
             '1149': 'Producto de apoyo - Alquiler Compresor Oxígeno', '286': 'Electrodo económico',
             '898': 'Protesis cardiacas biologica mitral', '438': 'Producto: Teclado letra grande',
             '1042': 'Codera para piel de oveja', '780': 'Producto: Antideslizante -CENAREC-.',
             '986': 'Lente intraocular', '394': 'Silla Ruedas 18 pulgadas',
             '696': 'Producto: Comunicador 7 mensajes -CENAREC-.',
             '479': 'Producto: set 3 piezas etiquetas braille', '173': 'Mascara de oxigeno',
             '75': 'Serv. Educativos', '210': 'Cuña para piernas', '568': 'Prod. Impresora Braille Trident',
             '520': 'Producto:', '609': 'Prod. Mouse Switch', '241': 'Alquiler Silla de ruedas no ortopedicas',
             '683': 'Producto: Monitores con pantalla táctil -CENAREC-.', '73': 'Terapia Ocupacional',
             '1145': 'Venta producto de apoyo - Producto: Andadera con rodines',
             '584': 'Prod. Teclado letras grandes', '10': 'Alquiler sillas de ruedas.',
             '1130': 'Prod. Alquiler de cama', '78': 'Terapia Física', '274': 'Corset de Jewett',
             '118': 'Hogar de cuido para personas con parálisis cerebral en situación de abandono',
             '702': 'Producto: Comunicador de tarjetas - CENAREC-.',
             '458': 'Producto: lápiz punzón escribir braille',
             '835': 'Producto: Kit para el cuidado diario -CENAREC-.', '409': 'Ortesis muñeca y dedo',
             '368': 'Bastón una punta decorado', '369': 'Prod. Silla de baño de transferencia',
             '180': 'Gradas 2 peldaños', '1046': 'Tobillera elastica',
             '973': 'Donación de equipo Técnico - Sillas Ruedas Estandar (uso diario)', '14': 'Audiometrías',
             '641': 'Prod. Silla Ruedas Ortopedica', '13': 'Ortopédia.', '1116': 'Cama Ortopedica Manual',
             '33': 'Terapia Física', '155': 'Fajas embarazadas', '638': 'Prod. Bidé',
             '583': 'Prod. Software grid 2', '232': 'Alquiler: Sillas Ruedas',
             '978': 'Ferula para mano antiespasmica', '301': 'BOLA EJERCICIO 75CM', '921': 'Guante cosmetico',
             '38': 'Enseñanza de Lesco', '534': 'Prod. Maquina escribir braille perkins next generation',
             '525': 'Producto: tablero juego damas en braille', '1015': 'Prótesis arriba rodilla',
             '684': 'Producto: Silla Ruedas Electrica -CENAREC-.', '342': 'COJÍN LUMBAR',
             '1182': 'Venta producto de apoyo - Esfigmomanometro Digital',
             '264': 'Férulas Polipropileno Especiales', '965': 'Ortesis Auditivas: Retro auricular',
             '970': 'Calculadora Parlante', '340': 'VENDA DE GASA 10 CM x 5 M LE ROY',
             '1201': 'Salvaescalera LG 2020', '79': 'Serv. Equinoterapia', '359': 'Bastón una punta de madera',
             '4': 'Asesoría Emocional', '554': 'Prod. Baston aluminio rigido',
             '865': 'Producto: Software Magnificador y lector de pantalla -CENAREC-.',
             '711': 'Producto: Software Mouse por barrido -CENAREC-.',
             '1191': 'Venta producto de apoyo - Inodoro Portatil 3 en 1', '61': 'Terapia Ocupacional',
             '1167': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica 16 pulgadas',
             '275': 'ELECTRODO WANDY ADHESIVO', '512': 'Producto: reloj deportivo vibración de luz',
             '157': 'Sistema drenaje urinario cama', '894': 'Ortesis cables flexibles',
             '471': 'Producto: bastón movilidad grafito y corcho - baja vision', '633': 'Prod. Bastón de 1 punta',
             '691': 'Producto: Conmutador de tipo pulsador -CENAREC-.',
             '34': 'Servicio de audiología en general con fabricación de audífonos.', '328': 'Compresa fría',
             '308': 'ELECTRODO TYCO 2X2', '430': 'Producto: Lentes ultrasónicos',
             '751': 'Producto: Camera Mouse -CENAREC-.', '604': 'Prod. Protector pantalla Braille para celular',
             '238': 'Alquiler de Equipo Médico - Muletas', '963': 'Ortesis Auditivas: Audífonos Intra-canal',
             '178': 'zapato para yeso', '759': 'Producto: Mouse controlado por mov. ojos -CENAREC-.',
             '618': 'Prod. Impresora Braille Cyclone', '457': 'Producto: etiquetadora braille',
             '869': 'Producto: Cuaderno Electronico -CENAREC-.', '1081': 'Alcanzador',
             '523': 'Producto: audífonos stereo bellman',
             '796': 'Producto: Teclado con letras grandes y en color de alto contraste - CENAREC-.',
             '9': 'Terapia Física', '122': 'Educación Física', '681': 'Producto: Pulsador tipo Varilla -CENAREC-.',
             '502': 'Producto: máquina escribir clásica braille perkins', '932': 'Collar cervical filadelfia',
             '489': 'Producto: pizarra magnética con formas, letras y números',
             '761': 'Producto: Software Emulador de barrido -CENAREC-.',
             '972': 'Donación de equipo Técnico - Sillas Baño', '404': 'Ferula Muñeca',
             '84': 'Centro Atención Integral', '1033': 'Audifono tipo caja bolsillo', '124': 'Terapia física',
             '1070': 'Pesas para muñeca', '974': 'Donación de equipo Técnico - Rodilleras',
             '840': 'Producto: Funda tipo almohadilla para pulsador -CENAREC-.', '195': '',
             '549': 'Prod. Etiquetador con dial', '391': 'Bastón de una punta de apoyo',
             '476': 'Producto: reloj llavero con voz español', '959': 'Prod. Implante Coclear',
             '941': 'Audifono Intra auricular', '69': 'Servicio alquiler o préstamo de Camas Hospitalarias.',
             '312': 'COJÍN CUADRADO ANATÓMICO ENSUEÑO', '381': 'Prod. Muleta adulto',
             '803': 'Producto: Máquina para escritura en Braille estándar -CENAREC-.',
             '487': 'Producto: bastón movilidad de grafito color de lujo',
             '348': 'ELECTRODO VALUTRODE REDONDO 1.25', '70': 'Serv. Alquiler de Muletas',
             '997': 'Marcapaso binacameral', '1013': 'Cambio de encaje', '1082': 'Andadera Universal niño',
             '945': 'Prod. Manos Libres', '272': 'Cuña para Espalda', '161': 'Carretilla oxígeno',
             '572': 'Prod. Kit diagramación táctil', '108': 'Centro Atención Integral',
             '905': 'Férulas Polietileno adulto', '349': 'Mesa Puente',
             '849': 'Producto: Software lector de texto -CENAREC-.',
             '763': 'Producto: Software Emulador Mouse -CENAREC-', '198': 'Colchón ortopédico',
             '336': 'COJÍN DE GEL CUADRADO', '1086': 'Baston Ajustable',
             '768': 'Producto: Software Emulador Mouse -CENAREC-.', '324': 'ELECTRODO VALUTRODE CUADRADO 2X2',
             '822': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.',
             '1193': 'Venta producto de apoyo - Oximetro Digital',
             '1168': 'Alquiler producto de apoyo - Sillas Rueda Estándar 18 pulgadas',
             '1091': 'Inmovilizador de dedos', '979': 'Ferula ortoplast niño', '1096': 'Muslera elástica',
             '1028': 'Collar cervical tipo filadelfía.', '875': 'Producto: Conmutador tipo Pulsador -CENAREC-.',
             '387': '', '329': 'VENDA ELÁSTICA LE ROY 7,5 x 5MTS',
             '445': 'Producto: bascula peso con habla español',
             '422': 'Producto: impresora braille basic modelo DV 5', '266': 'Collar Cervical Blando',
             '345': 'Cojín cuadrado de espuma', '996': 'Protesis cardiacas biológica aortica',
             '723': 'Producto: Teclados de teclas grandes - CENAREC-.',
             '634': 'Prod. Elevador de sanitario con soportes',
             '806': 'Producto: Software Emulador Teclado Virtual -CENAREC-.',
             '1142': 'Venta producto de apoyo - Gigante para Suero',
             '539': 'Prod. Puntero gancho tipo puntero jumbo', '910': 'Quilla carbono niño',
             '550': 'Prod. Impresora Braille - Braillo 600',
             '671': 'Préstamo de equipo especial: Sillas Ruedas No ortopedica', '1057': 'Estabilizador rodilla',
             '100': 'Formación Humana', '380': 'Silla Ruedas para PC - 18 pulgadas', '946': 'Prod. Sistema FM',
             '655': 'COJIN AIRE GEL', '1058': 'muñequera y dedo pulgar',
             '1189': 'Venta producto de apoyo - Sillas baño con respaldar',
             '352': 'Andadera adulto aluminio con rodines',
             '968': 'Sistema de frecuencia modulada (juego de audífonos y micrófono)',
             '332': 'PINZA ADSON SIN DIENTES', '20': 'Terapia ocupacional',
             '147': 'Ser. alquiler camas ortopedicas', '947': 'Prod. Control para audífono',
             '151': 'Suspensorios Deportivo', '1137': 'Venta producto de apoyo - Canula Nasal Adulto',
             '701': 'Producto: Bastón Plegable -CENAREC-.', '370': 'Bastón 4 puntas - KX Medical',
             '219': 'Colchón de aire con compresor', '473': 'Producto: reloj hombre habla español',
             '504': 'Producto: reloj para hombre con habla español', '557': 'Prod. Reloj mujer con voz digital',
             '212': 'Cabestrillo', '742': 'Producto: Software Comunicación Sordo-Ceguera -CENAREC-.',
             '787': 'Producto: Corta Uñas Adaptado -CENAREC-.', '463': 'Producto: calculadora que habla español',
             '65': 'Centro educativo - Educación especial curricular.',
             '834': 'Producto: Conmutador electromiográfico -CENAREC-.', '144': 'Servicios educativos.',
             '743': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '1087': 'Bastón con asiento',
             '373': 'Muleta adulto JR', '276': 'LIGA THERA-BAND GRIS', '1035': 'Audifono tipo Retro auricular',
             '533': 'Prod. Grabador audio con software incluido', '578': 'Prod. Software Jaws',
             '628': 'Prod. Mesa Puente', '52': 'Terapia Ocupacional', '957': 'Prod. Softband',
             '563': 'Prod. Balon super suave espuma con cascabeles',
             '497': 'Producto: indicador nivel batería de líquidos', '133': ': Psicología',
             '728': 'Producto: Comunicador multinivel de 8 casillas -CENAREC-.',
             '464': 'Producto: Juego ajedrez para personas no videntes', '360': 'Silla baño con respaldo',
             '1009': 'Prótesis de pierna', '317': 'Electrodo carbono 5 cm',
             '427': 'Producto: bastón movilidad fibra vidrio', '1054': 'Mesa Puente',
             '821': 'Producto: Mesa con escotadura -CENAREC-.',
             '839': 'Producto: Comunicador de 32 casillas con barrido -CENAREC-.',
             '456': 'Producto: globo terraqueo con relieve', '1059': 'Dona Hule infable',
             '436': 'Producto: magnificador de imágenes alta definición',
             '514': 'Producto: paquete de papel imprimir braille',
             '805': 'Producto: Sistema de montaje para conmutadores -CENAREC-.', '188': 'Bota esguince grado 3',
             '851': 'Producto: Sistema de montaje para comunicadores -CENAREC-.',
             '412': 'SOPORTE ESCROTAL ATLÉTICO', '343': 'Cojin inflable cervical',
             '350': 'Silla Ruedas full ortopédica',
             '467': 'Producto: malla cómoda de cuerpo entero elevador pacientes', '112': 'Centro Atención Integral',
             '953': 'Prod. Deshumedecedor pastilla', '1188': 'Venta producto de apoyo - Sillas baño con respaldar',
             '610': 'Prod. Expert Mouse', '415': 'Ortesis muñeca derecho o izquierdo', '221': 'Ortesis hombro',
             '309': 'ELECTRODO WANDY CON ADHESIVO', '585': 'Prod. Bloque aprender braille money pocket',
             '1206': 'Silla Ruedas electrica SAT-FGO',
             '1150': 'Producto de apoyo - Alquiler Compresor Oxigeno New Life Elite', '987': 'Ortesis al tercio',
             '672': 'Préstamo de equipo especial: Camas Hospitalarias', '622': 'Prod. Teclado configurable para PC',
             '854': 'Producto: Software Emulador de mouse -CENAREC-.', '331': 'LIGA THERA-BAND AMARILLO',
             '913': 'Prótesis pierna', '597': 'Prod. Bastón rígido grafito', '89': 'Audiometrías',
             '385': 'Silla Ruedas con partes movibles', '983': 'Prótesis ocular individualizada',
             '375': 'Bastón 4 puntas - drive', '811': 'Producto: Software Emulador de Teclado Virtual -CENAREC-.',
             '1107': 'Almohada Cervical', '1066': 'Cuello inmovilizador',
             '706': 'Producto: Lupa de barra de 8 pulgadas -CENAREC-.', '1103': 'Cabestrillo',
             '1154': 'Venta producto de apoyo - Estetoscopio',
             '466': 'Producto: reloj caballero con voz español bicolor', '364': 'Colchón de aire con compresor',
             '437': 'Producto: atril manos libres', '93': 'Serv. Apoyo Emocional',
             '460': 'Producto: balón de campanas', '234': 'Alquiler de Equipo Médico - Cama Hospitalaria',
             '556': 'Prod. Bastón Plegable de aluminio', '176': 'Faja para torax', '284': 'LIGA THERA-BAND DORADO',
             '334': 'Compresa fría', '1209': 'Plataforma vertical SAT-GL', '967': 'Lupa con lámpara',
             '1153': 'Venta producto de apoyo - El Cobertor impermeable para colchón',
             '755': 'Producto: Pulsador que permite grabar un mensaje -CENAREC-.', '63': 'Terapia Física',
             '290': 'Bola de Gel', '42': 'Apoyos Didácticos', '196': 'Muñequera tunel carpal',
             '1163': 'Venta producto de apoyo - Sillas Rueda Full Ortopédica',
             '753': 'Producto: Impresora Braille -CENAREC-.', '423': 'Producto: identificador luz con voz español',
             '76': 'Serv. Terapia Ocupacional', '1164': 'Alquiler producto de apoyo - Sillas Rueda Full Ortopédica',
             '574': 'Prod. Mouse trackball', '28': 'Terapia de Lenguaje',
             '825': 'Producto: Carcasa de Teclado -CENAREC-.', '1127': 'Prod. Alquiler gigante suero',
             '154': 'Protector talón', '189': 'Bastón de 1 punta', '937': 'Audifono tipo caja bolsillo',
             '1180': 'Venta producto de apoyo - Pedal para Ejercicios', '881': 'Ferula para pie adulto',
             '303': 'ELECTRODO PREMIUN TAN REDONDO 2', '344': 'RODILLO DE MANO THERABAND ROJO',
             '142': 'Servicios Educativos', '277': 'MASILLA CANDO THERAPUTTY',
             '1195': 'Venta producto de apoyo - (BOLSA PARA RECOGER DESECHOS)', '393': 'Prod. Silla inodoro',
             '640': 'Prod. Estetoscopio', '925': 'Mano tipo garfio', '1094': 'Alquiler de andadera',
             '1148': 'Venta producto de apoyo - Alquiler Compresor Oxígeno Visión Air',
             '704': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '885': 'Ferula laminado resina niño',
             '50': 'Centro Atención Integral', '77': 'Serv. Apoyo Emocional', '547': 'Prod. Head Mouse',
             '310': 'COJÍN PARA PIERNAS', '748': 'Producto: Atril Ajustable -CENAREC-.',
             '603': 'Prod. Puntero Slip-on tipo marshmallow', '915': 'Prótesis brazo',
             '682': 'Producto: Comunicador de 3 casillas que se ajusta a la cadera -CENAREC-.',
             '605': 'Prod. Roller Mouse red', '267': 'Silla de Ruedas Standart',
             '776': 'Producto: Software Magnificador de pantalla para personas con baja visión -CENAREC-.',
             '1173': 'Venta producto de apoyo - Andadera Plegable de Aluminio', '1008': 'Prótesis de antebrazo',
             '1200': 'Muletas anfibias', '30': 'Terapia Ocupacional',
             '478': 'Producto: línea braille smart beetle teclado y pantalla braille ultra portatil',
             '243': 'Corset Toracolumbar', '148': 'Serv. Ocupacionales de Recreo', '242': 'Alquiler silla baño',
             '991': 'Electrodos para marcapasos', '1125': 'Prod. Sillas Ruedas', '163': 'Almohada tipo dona',
             '720': 'Producto: Utensilios de cocina -CENAREC-.', '82': 'Psiquiatría',
             '442': 'Producto: impresora braille everest modelo DV 5', '2': 'Psicología',
             '690': 'Comunicador de 7, 12 o 23 casillas, de diseño moderno, con 5 niveles. -CENAREC-.',
             '837': 'Producto: Software Lector de pantalla libre personas con baja visión -CENAREC-.',
             '509': 'Producto: punteras para bastón ambutech', '448': 'Producto: lupa escritorio de iluminación',
             '87': 'Terapia Física', '653': 'BIDEP DE ACERO',
             '831': 'Producto: Indicador de nivel de líquidos -CENAREC-.',
             '400': 'CAMA ORTOPÉDICA ELÉCTRICA CON BARANDAS Y COLCHÓN AMERICAN BANTEX', '152': 'Pesa arena',
             '1050': 'Tobillera neopreno', '58': 'Serv. Educativos', '901': 'Marcapaso binacameral',
             '644': 'Prod. Sillas de ruedas no ortopédicas', '893': 'Ortesis corta',
             '919': 'Protesis arriba rodilla', '744': 'Producto: Calculadora Visual -CENAREC-.',
             '695': 'Producto: Silla para posicionamiento -CENAREC-.', '543': 'Prod. Mini Balon con campanas',
             '621': 'Prod. Bastón puntero gancho tipo lapiz', '407': 'SoftPad',
             '855': 'Producto: Software Lector de pantalla para personas ciegas o con baja visión -CENAREC-.',
             '846': 'Producto: Control de radiofrecuencia -CENAREC-.', '396': 'Muleta Adulto',
             '579': 'Prod. Software traductor braille', '123': 'Artes Plásticas', '1064': 'Orinal masculino',
             '551': 'Prod. Guía para firma', '1017': 'Guante cosmetico', '150': 'Corrector clavícula',
             '778': 'Producto: Mouse tipo “joystick” para utilizar con el mentón -CENAREC-.',
             '734': 'Producto: Touchpad y mouse por teclas -CENAREC-.', '263': 'Férulas Polipropileno para mano.',
             '576': 'Prod. Marco aritmético y ábaco combinado', '201': 'Corrector postura',
             '297': 'Electrodo cuadrado azul', '209': 'Bastón de 4 puntos', '162': 'Riñon de acero',
             '218': 'Bolsa para enema', '175': 'Gigante 4 ganchos', '333': 'ELECTRODO VALUTRODE REDONDO 2.75',
             '829': 'Producto: Tabla con rodines - CENAREC-',
             '824': 'Producto: Puntero con agarrador manual -CENAREC-.', '339': 'Prod. ELECTRODO THERATRODE 2 x 2',
             '820': 'Producto: Focus - Display Braille -CENAREC-.', '570': 'Prod. Calculadora cientifica parlante',
             '465': 'Producto: juego cartas naipe en braille', '537': 'Prod. Impresora Braille jot a dot',
             '1135': 'Venta producto de apoyo - Bidet Plástico',
             '1162': 'Venta producto de apoyo - Sillas Rueda Estandar 18 pulgadas',
             '573': 'Prod. Software well clicker 2', '246': 'Estabilizador de Rodilla',
             '688': 'Lapiz escribe en papel termosensible -CENAREC-.', '269': 'BASTÓN DE 1 PUNTO',
             '392': 'BASTÓN 1 PUNTO ANTISHOCK CON FOCO', '470': 'Producto: lupa reglón 2x',
             '952': 'Prod. Deshumedecedor eléctrico', '383': 'Férula espinal rígida',
             '707': 'Producto: Software comunicación alternativa -CENAREC-.',
             '808': 'Producto: Grúa Hidráulica -CENAREC-.', '791': 'Producto: Borde para plato -CENAREC-.',
             '1041': 'Andadera Plegable', '203': 'Venda theraband', '314': 'Cojin Lumbar de malla',
             '876': 'Producto: Impresora Braille -CENAREC-.',
             '838': 'Producto: Grabadora con Pictograma -CENAREC-.',
             '472': 'Producto: lupa electronica bolsillo 7 pulgadas',
             '870': 'Producto: Cuaderno Electronico -CENAREC-.', '454': 'Producto: juego formas y colores',
             '172': 'Silla de baño', '18': 'Capacitaciones', '85': 'Centro de atención integral',
             '366': 'Bastón plegable azul, una punta', '177': 'Botella para orinar hombre',
             '47': 'Serv. Educativos: Manualidades.', '261': 'Férulas Polipropileno para brazo.',
             '600': 'Prod. Mouse Kid Trackball', '1036': 'Audifono tipo Intra canal', '224': 'Soporte codo',
             '817': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.',
             '505': 'Producto: rayo electronico personas baja visión',
             '737': 'Producto: Conmutador que emula el clic del mouse -CENAREC-.',
             '540': 'Prod. Guia actividades caja luz', '916': 'Zapato ortopedico bajo molde yeso adulto',
             '1076': 'Ferula muñeca', '262': 'Férulas Polipropileno PIE',
             '1040': 'Silla brazo tipo escritorio pies desmontables',
             '607': 'Prod. Impresora Braille - Braillo 600 sw', '187': 'Rodillera para meniscos',
             '960': 'Prod. Procesador de sonido', '171': 'Kinesiotape',
             '544': 'Prod. Impresora Braille - Braillo 600 sr', '411': 'Zapato para yeso', '984': 'Prótesis ocular',
             '1199': 'Silla Anfibia', '645': 'Prod. gigante suero', '917': 'Cambio de encaje',
             '200': 'Colchón de agua', '1020': 'Mano con guante cosmeticos', '988': 'Ortesis larga',
             '282': 'ELECTRODO PREMIUN BLANCO REDONDO 2',
             '845': 'Producto: Transmisor de alertas para timbre y teléfono -CENAREC-.',
             '1024': 'Corset Lona toracolumbar',
             '1158': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica 18 pulgadas',
             '774': 'Producto: Conmutador tipo pulsador -CENAREC-.', '936': 'Muleta axilar',
             '208': 'Faja industrial', '902': 'Marcapaso unicameral',
             '1157': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica 16 pulgadas',
             '903': 'Silla Ruedas Especializadas', '928': 'Corset lona toracolumbar',
             '624': 'Prod. Impresora Braille Juliet 120', '804': 'Producto: Computador Portátil Táctil -CENAREC-.',
             '1056': 'Muleta Universal', '548': 'Prod. Bastón grafito telescópico', '658': 'ESPALDERA POSTURAL',
             '792': 'Producto: Etiquetadora Braille -CENAREC-.', '306': 'Tens analgesico Drive',
             '1083': 'Inodoro Portatil 3 en 1', '790': 'Producto: Vaso adaptado para silla de ruedas -CENAREC-.',
             '146': 'Servicios ocupacionales.', '6': 'Ortopédia.', '1104': 'Mascarilla para nebulizar',
             '323': 'LIGA THERA-BAND NEGRO', '750': 'Producto: Software Controlador Mouse -CENAREC-.',
             '1061': 'Inmovilizador tobillo alto', '1019': 'Relleno anterior y corslette pierna',
             '582': 'Prod. Baston bola giratoria', '315': '', '1052': 'Elevador inodoro sin brazos',
             '553': 'Prod. Mouse Big track switch', '117': 'Educación Especial', '1207': 'Elevador tina',
             '630': 'Prod. Andaderas', '809': 'Producto: Lapicero Ergonómico -CENAREC-.',
             '676': 'Producto: Powerlink -CENAREC-.', '229': 'Bola de gel para mano',
             '647': 'Prod. Bastón de 4 puntas', '453': 'Producto: medidor de insulina',
             '278': 'LIGA THERA-BAND AZUL', '516': 'Producto: reloj despertador de mesa con voz español',
             '291': 'Electrodo pals cuadrado 2 x 2', '327': 'ELECTRODO THERATRODE 1.5 X 3.5',
             '1114': 'Muleta Antebrazo', '3': 'Terapia de Lenguaje', '1032': 'Muleta axilar.',
             '766': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.',
             '950': 'Prod. Audifono para móvil', '528': 'Producto: reloj braille para hombre seiko',
             '956': 'Prod. Sistema BAHA Attract',
             '795': 'Producto: Software Programa de reconocimiento de voz - CENAREC-.',
             '850': 'Producto: Silla Ruedas simple -CENAREC-.', '228': 'Muletas', '225': 'Soporte rotuliano',
             '513': 'Producto: rompecabezas de mascotas con sonidos',
             '555': 'Prod. Teclado para computador Big Blu', '121': 'Educación Musical',
             '1152': 'Venta producto de apoyo - Elevador de Sanitario con brazos',
             '493': 'Producto: bastón grafito baja visión o no videntes',
             '810': 'Producto: Vaso con tapa y pajilla -CENAREC-.', '1205': 'Salvaescalera HL350',
             '853': 'Producto: Conmutador por luz infra-roja -CENAREC-.',
             '754': 'Producto: Sistema de montaje para conmutadores -CENAREC-.',
             '245': 'SILLA DE RUEDAS PARA Parálisis Cerebral', '21': 'Terapia Física',
             '105': 'Alquiler Médicos ByB - Sillas Ruedas', '496': 'Producto: teléfono inalámbrico con voz español',
             '230': 'Alquiler: Cama Hospitalaria', '860': 'Producto: Videoteléfono -CENAREC-.',
             '575': 'Prod. Software Boardmaker', '1003': 'Férulas Polipropileno niño',
             '182': 'Muñequera para esguince tradicional', '390': 'Prod. Silla inodoro',
             '762': 'Producto: Software Comunicación Aumentativa -CENAREC-.',
             '730': 'Producto: Conmutador de tipo pulsador -CENAREC-.', '139': 'Taller Ebanistería',
             '632': 'Prod. gigante suero', '993': 'Protesis cardiacas biológica mec. mitrales', '251': 'ANDADERAS',
             '858': 'Producto: Mouse Roller Trackball -CENAREC-.', '713': 'Cuña ajustable -CENAREC-.',
             '692': 'Producto: Calzador de medias -CENAREC-.', '981': 'Ferula laminado resina niño',
             '657': 'PROTESIS PARA ARRIBA DE RODILLA', '367': 'Silla Baño Plástica', '129': ': Artes Plásticas',
             '862': 'Tenedor adaptado -CENAREC-.',
             '815': 'Producto: Mouse adaptado para conectar conmutadores -CENAREC-.',
             '424': 'Producto: lampara inteligente luz led',
             '1118': 'Silla Ruedas Reclinable escritorios pies elevables',
             '741': 'Producto: Pulsador Graba Mensaje audio -CENAREC-.', '113': 'Serv. Educativos',
             '1105': 'Barandal para inodoro', '708': 'Producto: Comunicador de 4 casillas -CENAREC-.',
             '650': 'SILLA DE RUEDAS DE 18 PULGADAS', '62': 'Centro de Atención Integral',
             '775': 'Producto: Computador operada mov. ojos -CENAREC-.',
             '830': 'Productos de apoyo: Pantalla Táctil Infrarroja -CENAREC-.',
             '770': 'Producto: Comunicador de 8 casillas con barrido -CENAREC-.', '341': 'BOLSA DE AGUA CALIENTE',
             '1065': 'Bastón Plegable', '599': 'Prod. Bastón 4 piernas de soporte',
             '1194': 'Alquiler producto de apoyo - Oximetro Digital', '231': 'Alquiler: Andaderas',
             '1166': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica 18 pulgadas',
             '1111': 'Concentradores de oxigeno',
             '764': 'Producto: Cubiertos adaptados con material moldeable -CENAREC-.', '1098': 'Gigante suero',
             '1047': 'Dona Espuma', '857': 'Producto: Mouse Roller Trackball -CENAREC-.',
             '414': 'Prod. Tobillera sin talón 2 vías', '779': 'Producto: Ayuda Táctil -CENAREC-.',
             '731': 'Producto: Cuchara y tenedor adaptados en estilo puño universal -CENAREC-.',
             '199': 'Plantillas de gel para pie', '586': 'Prod. Vara para medir para baja visión',
             '614': 'Prod. Baston gancho tipo marshmallow', '1084': 'silla brazo fijo, pies elevables',
             '357': 'Elevador de sanitario sin soportes', '989': 'Ortesis corta',
             '1181': 'Venta producto de apoyo - Esfigmomanometro Manual',
             '492': 'Producto: balanza de cocina con voz',
             '705': 'Producto: Escanea y lee cualquier libro o documento impreso -CENAREC-.',
             '57': 'Centro Atención Integral', '307': 'Electrodo pals', '1043': 'Muslera neopreno',
             '580': 'Prod. Mini Touchpad teclado', '434': 'Producto: bolsa lona apertura pacientes',
             '222': 'Gigante dos ganchos', '1093': 'Baston 4 puntos', '213': 'Corset toraco lumbar',
             '1075': 'Escalerilla 2 peldaños', '725': 'Producto: Conmutador Pulsador -CENAREC-.',
             '794': 'Producto: Puntero de cabeza -CENAREC-.', '386': 'Silla Baño con agarraderas',
             '896': 'Prótesis cardiacas mec. aórticas',
             '1156': 'Alquiler producto de apoyo - Mesa Puente Alimentos',
             '552': 'Baston aluminio identificacion plegable', '149': 'Faja sacrolumbar',
             '1049': 'Andadera con ruedas', '1172': 'Venta producto de apoyo - Barra Apoyo 24 pulgadas',
             '480': 'Producto: cuchara y tenedor personas con deficiencia cognitiva',
             '715': 'Producto: Comunicador de 2 casillas -CENAREC-.', '295': 'VENDA ELÁSTICA MEDLINE 2',
             '91': 'Ortopédia.', '1110': 'Talonera para piel de oveja', '1010': 'Prótesis de muslo',
             '899': 'Cateter balon intraaortico', '625': 'Prod. Bastón rígido fibra vidrio para niño',
             '519': 'Producto: medidor glucosa con voz en español', '602': 'Prod. Mouse Swiftpoint',
             '880': 'Ferula para pie niño', '926': 'Corset lona Lumbrosacro',
             '39': 'Terapia Física y Rehabilitación', '527': 'Producto: guía escritura tamaño carta',
             '71': 'Serv. Terapia Ocupacional', '432': 'Producto: cinta para medir en pulgadas baja visión',
             '1068': 'Rodillera con bisagras', '966': 'Ortesis Auditivas: Audífonos vía osea',
             '40': 'Serv. Educativos (Manualidades para la independencia)', '560': 'Prod. Software traduce braille',
             '832': 'Producto: Interfaz para baterías -CENAREC-.',
             '566': 'Prod. Maquina escribir braille - perkins', '217': 'Muletas canadienses', '337': 'COJÍN COXIS',
             '807': 'Producto: Conmutador con sensor de parpadeo de fibra óptica -CENAREC-.',
             '143': 'Servicios Educativos', '897': 'Prótesis cardiacas mec. mitrales',
             '727': 'Producto: Plato convencional adaptado con ventosas -CENAREC-.',
             '322': 'ELECTRODO VALUTRODE RECTANGULAR 2X4', '595': 'Prod. Set Geométrico en braille',
             '440': 'Producto: bastón movilidad aluminio hecho en CR',
             '429': 'Producto: reloj para mujer, con voz en español', '649': 'Prod. Muletas', '90': 'Psiquiatría',
             '717': 'Producto: Hojas Magnificadores -CENAREC-.', '483': 'Producto: juego de mesa tactil',
             '285': 'BOLSA DE AGUA CALIENTE PARA ENEMA', '313': 'VENDA ELÁSTICA 6 MEDLINE',
             '598': 'Prod. Bastón gancho metal deslizante', '185': 'Silla ruedas tipo escritorio',
             '43': 'Serv. Terapia Física', '239': 'Alquiler de Equipo Médico - Servicio Sanitario Portatil',
             '908': 'Quilla carbono adulto', '859': 'Producto: Mouse Trackball gigante -CENAREC-.',
             '330': 'ELECTRODO WANDY CON ADHESIVO', '202': 'Rodillera estabilizadora',
             '474': 'Producto: Grabadora audio digital voz clasica', '1072': 'Carretilla para oxigeno',
             '1088': 'Sillas Ruedas tipo inodoro', '134': ': Educación Especial', '1108': 'Baranda para cama',
             '49': 'Terapia Física', '769': 'Producto apoyo: Adaptación Lapicero -CENAREC-.',
             '378': 'Branadal para inodoro', '721': 'Producto: Calculadora teclas grandes -CENAREC-.',
             '299': 'Electrodo carbono 4 cm', '494': 'Producto: reloj para mujer con sintetizador de voz',
             '485': 'Producto: elevador manual pacientes', '877': 'Producto: Impresora Braille Enablin -CENAREC-.',
             '955': 'Prod. TV Streamer (transmisor)', '686': 'Producto: Mouse controlado mov. ojos -CENAREC-.',
             '714': 'Producto: Software Controlador Mouse -CENAREC-.',
             '41': 'Adecuación Curricular No Significativa', '538': 'Prod. Bastón soporte ajustable',
             '1175': 'Venta producto de apoyo - Barra Apoyo para baño', '36': 'Terapia de Lenguaje',
             '1190': 'Venta producto de apoyo - Muletas',
             '475': 'Producto: lampara inteligente luz dia r10 recargable',
             '449': 'Producto: cinta métrica con habla en español', '1128': 'Prod. Mesa Puente',
             '451': 'Producto: regletas plasticas escribir braille', '300': 'ELECTRODO TYCO 2',
             '382': 'Bidé plástico', '1037': 'Audifono tipo Intra auricular',
             '447': 'Producto: reloj cuadrado para caballero, con voz español',
             '1159': 'Venta producto de apoyo - Sillas Rueda Semi Ortopédica',
             '141': 'Apoyo Económico a las asociaciones vinculadas con el Tema de Discapacidad.',
             '951': 'Prod. Manos libres', '268': 'Corrector de Postura',
             '758': 'Producto: Conmutador Pulsador -CENAREC-.', '168': 'almohada antironquidos',
             '305': 'LIGA CANDO ROJO', '109': 'Centro Atención Integral',
             '685': 'Producto: Comunicador multinivel de 128 casillas -CENAREC-.',
             '260': 'Faja Lumbar (corset Lumbar)', '1131': 'Prod. Equipo oxigeno', '942': 'Prod. Tinnitool',
             '166': 'Bolsa orina para pierna', '1132': 'Alquiler de andadera',
             '884': 'Ferula laminado resina adulto', '248': 'CABESTRILLO', '32': 'Terapia Física',
             '29': 'Odontología', '930': 'Bastón', '226': 'Bide acero', '96': 'Centro Atención Integral',
             '826': 'Producto: Carcasa de Teclado -CENAREC-.', '1095': 'Pedal de ejercicio',
             '777': 'Dispositivo para colocar cilindros y botellas -CENAREC-.', '19': 'Terapia Física',
             '354': 'Prod. Trapecio Lumex', '361': 'Silla Ruedas - 18 pulgadas', '233': 'Alquiler: Muletas',
             '1073': 'Silla Baño especial', '1060': 'Silla Baño Obesos',
             '679': 'Producto: Mouse adaptado para conectar conmutadores -CENAREC-.',
             '789': 'Producto: Software Convierte la imagen de un texto -CENAREC-.',
             '1161': 'Venta producto de apoyo - Sillas Rueda Estandar 24 pulgadas',
             '836': 'Producto: Magnificador de pantalla para personas con baja visión -CENAREC-.',
             '55': 'Audiometría', '249': 'Muñequeras de soporte', '413': 'Prod. Faja Costal Mujer',
             '86': 'Centro de atención integral', '823': 'Productos de apoyo - CENAREC-. Abotonador',
             '1186': 'Venta producto de apoyo - Grúa Transporte Pacientes', '358': 'Bastón con sentadero',
             '1062': 'Bidet', '469': 'Producto: mouse ergonomico para PcD',
             '1120': 'Inmovilizador muñeca y antebrazo', '431': 'Producto: bastón movilidad aluminio',
             '397': 'Elevador de sanitario con soportes',
             '746': 'Producto: Comunicador de 4 casillas con barrido -CENAREC-.',
             '1187': 'Alquiler producto de apoyo - Grúa Transporte Pacientes', '223': 'Soporte cadera',
             '1198': 'Silla Salvaescalera PLA', '995': 'Cateter balon intraaortico',
             '97': 'Serv. Educación Especial', '565': 'Prod. Mini teclado', '164': 'Férula dedos',
             '1034': 'Audifono tipo vía osea', '675': 'Producto: Conmutador con sensor de proximidad -CENAREC-.',
             '827': 'Producto: Software de comunicación -CENAREC-.', '594': 'Prod. Material etiquetas braille',
             '190': 'almohada para dar de mamar', '506': 'Producto: lapicero en negrita', '365': 'Bastón 4 puntas',
             '635': 'Prod. Colchón de aire con compresor', '927': 'Corset Jewett', '111': 'Serv. Educativos',
             '567': 'Prod. Impresora etiquetas de medicamentos en Braille',
             '561': 'Prod. Duplicador Braille y táctil Maxi-form Impresora', '116': 'Terapia Física.',
             '749': 'Producto: Software emulador de Mouse -CENAREC-.', '252': 'ANDADERAS',
             '802': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.',
             '351': 'Bastón de 3 puntas', '1121': 'Balones terapéuticos', '562': 'Prod. Magnificador tipo bolsillo',
             '120': 'Artes Industriales', '398': 'Silla Ruedas con partes movibles', '254': 'Cojín coxis',
             '298': 'Tens anagelsico Drive', '904': 'Ferulas Polipropileno adulto',
             '814': 'Producto: Atril Madera -CENAREC-.', '1069': 'Sillas ruedas y andadera con ruedas',
             '132': ': Artes Industriales', '420': 'Tiflotecnología',
             '756': 'Producto: Sistema de montaje para conmutadores y otros dispositivos -CENAREC-.',
             '526': 'Producto: calculadora con voz en español',
             '1136': 'Venta producto de apoyo - Bastón de 4 puntos apoyo',
             '1176': 'Venta producto de apoyo - Nebulizador Adulto', '1016': 'Prótesis provisional abajo rodilla',
             '977': 'Ferula pie adulto',
             '874': 'Producto: Traductor de Braille a español (y otros idiomas) -CENAREC-.',
             '652': 'TOBILLERA DE BARRAS LATERALES', '503': 'Producto: reloj braille bolsillo para caballero',
             '403': 'Rodillera con regulación lateral', '389': 'Bastón una punta floreado',
             '975': 'Donación de equipo Técnico - Sillas Baño', '1124': 'Prod. Barra Cromada 18 pulgadas',
             '481': 'Producto: grabadora audio digital olympus', '106': 'Alquiler Médicos ByB - Muletas',
             '1055': 'Rodillera elastica', '1004': 'Quilla Carbono adulto', '216': 'Muslera',
             '433': 'Producto: alta voz manos libres', '617': 'Prod. Bastón guia plegable',
             '772': 'Producto: Software Lector de pantalla para personas ciegas o con baja visión -CENAREC-.',
             '372': 'Bastón una punta no vidente', '782': 'Vaso con tapa -CENAREC-.',
             '428': 'Producto: bastón de apoyo ajustable', '159': 'Tobillera', '26': 'Nutrición',
             '1002': 'Férulas Polietileno niño', '1170': 'Venta producto de apoyo - Vaso Humidificador',
             '522': 'Producto: rompecabezas de numeros en relieve y braille', '613': 'Prod. Cuadro álgebra táctil',
             '486': 'Producto: máquina inteligente braille con video perkins',
             '872': 'Producto: Escaner de palabras -CENAREC-.',
             '1139': 'Venta producto de apoyo - Camilla para Masajes', '1001': 'Férulas Polietileno adulto',
             '760': 'Producto: Comunicador Múltiple -CENAREC-.', '1113': 'Vaso humificador', '204': 'Bide plástico',
             '631': 'Prod. Sillas de ruedas no ortopédicas', '1119': 'Grúa levanta personas',
             '1044': 'Cama Ortopedica Electrica', '636': 'Prod. Mesa Puente', '1129': 'Prod. Grúa Hidráulica',
             '416': 'Tiflotecnología - Papel para Imprimir Braille', '247': 'Almohada Ortopédica',
             '1179': 'Venta producto de apoyo - Tanque Oxigeno 685 L',
             '408': 'Rodillera con barras laterales, tallas: s, m',
             '461': 'Producto: rompecabezas instrumentas sonidos', '501': 'Producto: guia lectura para firmar',
             '279': 'ELECTRODO WANDY CON ADHESIVO',
             '781': 'Producto: Generador de comunicadores de 7 niveles -CENAREC-.', '11': 'Terapia Ocupacional',
             '131': ': Terapía Lenguaje', '1109': 'Andaderas con 4 ruedas',
             '873': 'Producto: Touchpad mouse -CENAREC-.', '935': 'Collar Cervical Blando', '934': 'Andadera',
             '911': 'Quilla madera niño', '606': 'Papel Swell Touch', '107': 'Terapia Ocupacional',
             '281': 'VENDA COBAN DUKAL 3 ADHESIVA',
             '1165': 'Alquiler producto de apoyo - Sillas Rueda Estándar 20 pulgadas', '1045': 'Muñequera',
             '949': 'Prod. Manos libres inalambrico', '22': 'Terapia de Lenguaje', '637': 'Prod. Cama ortopedica',
             '678': 'Producto: Beberito con tapa -CENAREC-.', '283': 'Prod. Liga Theraband roja',
             '531': 'Prod. Puntero Slip-on Bola', '1106': 'Bastón de punto fijo',
             '160': 'Cuellos cervicales blando', '982': 'Ferula ortoplast adulto',
             '1053': 'Cuello cervical de espuma', '102': 'Alquiler Médicos ByB - Silla Baño',
             '651': 'FAJA POSOPERATORIA S/M CONFORTA MEDICA.', '7': 'Fisioterapia',
             '521': 'Producto: bastón movilidad grafito y hule baja vision', '165': 'Compresas gel reusable',
             '757': 'Producto: Gateador -CENAREC-.',
             '1': 'Serv. Educativo: La biblioteca posee un programa, con cursos mejoramiento de motora fina, junto con la Trabajadora Social que busca mejorar la calidad de vida de la familia.',
             '94': 'Serv. Capacitación', '170': 'Silla para evacuar', '289': 'PASTA CONDUCTORA TEN20',
             '401': 'Silla Ruedas 18 pulgadas', '135': 'Serv. Apoyo Económico', '72': 'Casa Hogar Comunitario',
             '44': 'Centro atención integral.', '889': 'Prótesis Mamaría', '395': 'Silla de baño',
             '1133': 'Venta producto de apoyo - Colchón espuma 5 pulgadas',
             '920': 'Prótesis provisional abajo rodilla',
             '273': 'Arnés de Soporte en la silla de Ruedas para pacientes con PC.', '961': 'Prod. Mini micrófono',
             '145': 'Centro Diurno de Atención Integral',
             '435': 'Producto: calculadora científica con habla español',
             '426': 'Producto: bolsa fuerte para elevador pacientes', '399': 'ANDADERA C: SENTADERO KX',
             '321': 'ELECTRODO ULTRASTIM', '8': 'Psiquiatría', '1097': 'Almohada ortopedica',
             '892': 'Ortesis larga', '542': 'Prod. Teclado Learning Board',
             '1169': 'Alquiler producto de apoyo - Sillas Rueda Semi Ortopédica', '207': 'Cuña para espalda',
             '379': 'Silla Ruedas 20 pulgadas', '83': 'Ortopédia.', '169': 'Taloneras',
             '16': 'Centro Atención Integral', '844': 'Producto: APP para Iphone -CENAREC-.',
             '184': 'Medias terapeuticas para varices', '347': 'VENDA ADHESIVA DE COLORES 3',
             '801': 'Producto: Software Lectura de textos -CENAREC-.',
             '482': 'Producto: tazas de medida cocina con marcas braille',
             '722': 'Producto: Software Magnificador y lector de pantalla -CENAREC-.', '670': 'Salvaescalera Bisón',
             '288': 'BOLA TERAPÉUTICA PARA MANO PEQUEÑA', '104': 'Alquiler Médicos ByB - Cama Hospitalaria',
             '1155': 'Venta producto de apoyo - Mesa Puente Alimentos',
             '1174': 'Venta producto de apoyo - Arnes de Grúa', '648': 'Prod. Silla Ruedas con partes movibles',
             '998': 'Marcapaso unicameral', '1101': 'silla ruedas para solo transporte',
             '665': 'Salvaescalera Flow 2', '992': 'Protesis cardiacas biológica mec. aortica',
             '1204': 'Salvaescalera HL320', '587': 'Prod. Impresora y software para imprimir formas en braille',
             '468': 'Producto: Lapicero ergonómico PcD en la mano', '35': 'Terapia ocupacional',
             '114': 'Animales Equinoterapia - Animales Equinoterapia Costa Rica.', '53': 'Terapia Física',
             '88': 'Fisioterapia', '1160': 'Venta producto de apoyo - Sillas Rueda Estandar 20 pulgadas',
             '660': 'Ascensor Ecovimec', '1184': 'Venta producto de apoyo - Cama Hospitalaria Manual',
             '320': 'VENDA ELÁSTICA 4', '962': 'Ortesis Auditivas: Audífonos de Caja o Bolsillo',
             '1192': 'Venta producto de apoyo - Inodoro Portatil con rodines', '56': 'Terapia Ocupacional',
             '418': 'Tiflotecnología', '452': 'Producto: guia firma regular', '541': 'Prod. Mouse Ergo Trackball',
             '405': 'SOPORTE ELÁSTICO REFORZADO PARA TOBILLO',
             '444': 'Producto: reloj circular caballero voz español',
             '1171': 'Venta producto de apoyo - Barra Apoyo 32 pulgadas', '969': 'Teclado “Línea Braille”',
             '136': 'Terapia Ocupacional', '498': 'Producto: reloj braille caballero', '316': 'Cojín Lumbar',
             '101': 'Alquiler Médicos ByB - Servicio Sanitario Portatil', '181': 'Estetoscopio',
             '1183': 'Venta producto de apoyo - Cama Hospitalaria Semi Eléctrica',
             '828': 'Producto: Magnificador portátil -CENAREC-.', '206': 'Collar philadelphia',
             '459': 'Producto: medidor de presión arterial',
             '847': 'Producto: Reloj Digital con Sintesis y reconocimiento de voz-CENAREC-.',
             '564': 'Prod. Magnificador Onyx PC', '890': 'Lente intraocular',
             '335': 'VENDA ELÁSTICA 2 LE ROY 5CM x5MTS', '1031': 'Collar cervical blando.',
             '964': 'Ortesis Auditivas: Audífonos Intra-auricular', '293': 'COJIN DE ESPUMA Y GEL',
             '490': 'Producto: reloj ovalado metal para hombre 4 alarmas con habla español',
             '863': 'Tijeras Adaptadas -CENAREC-.',
             '740': 'Producto: Software permite crear, editar e imprimir plantillas -CENAREC-.',
             '571': 'Prod. Teclado Maxim',
             '709': 'Producto: Software Magnificador tipo lupa multiplataforma -CENAREC-.',
             '1074': 'Silla Baño Transferencia', '355': 'Gigante de suero', '971': 'Diccionario de Sinónimos',
             '785': 'Producto: Sistema de montaje para conmutadores y comunicadores livianos -CENAREC-.',
             '15': 'Serv. Educativos', '871': 'Producto Apoyo: Andadera con asiento y canasta -CENAREC-.',
             '81': 'Fisioterapia', '1071': 'Oximetro de pulso', '256': 'MULETAS', '127': ': Estimulación Temprana',
             '126': ': Terapia Física', '529': 'Producto: ábaco personas no videntes',
             '677': 'Producto: Pulsador con grabación de secuencias de mensajes -CENAREC-.',
             '783': 'Producto: Magnificador giratorio -CENAREC-.', '311': 'VENDA ELÁSTICA DE COLORES 2',
             '596': 'Prod. Puntero rover free wheeling', '654': 'INMOBILIZADOR DE DEDO PULGAR MUÑECA.',
             '739': 'Producto: Material Antideslizante -CENAREC-.', '900': 'Protesis cardiacas biológica aortica',
             '793': 'Producto: Mueble de posicionamiento supino -CENAREC-.', '907': 'Ferulas Polipropileno niño',
             '318': 'ELECTRODO WANDY CON ADHESIVO', '59': 'Serv. Terapia Física',
             '788': 'Producto: Dispositivo limpiarse al usar el inodoro -CENAREC-.',
             '66': 'Servicio asistencia económica para pacientes en fase terminal', '1203': 'Salvaescalera OP',
             '1077': 'Almohada para CPAC', '581': 'Prod. Bastón gancho cerámica',
             '669': 'Salvaescalera Homeglide extra', '110': 'Serv. Educativos',
             '697': 'Producto: Mouse tipo “joystick” -CENAREC-.',
             '747': 'Producto: Conmutador doble para lengua, mentón o mejilla -CENAREC-.',
             '1196': 'Silla Salvaescalera BSK', '784': 'Conmutador de tipo pulsador -CENAREC-.',
             '425': 'Producto: Reloj para mujer con voz en español y pantalla para baja visión, banda de caucho',
             '668': 'Salvaescalera Capri', '1030': 'Andadera especializada según direcciones técnicas.',
             '924': 'mano con guante cosmetico', '663': 'Salvaescalera Platinium',
             '673': 'Producto: Generador de comunicadores -CENAREC-.', '642': 'Prod. Andaderas',
             '1026': 'Bastón especializada según direcciones técnicas.', '31': 'Psicología',
             '287': 'Anillo rotuliano', '601': 'Prod. Puntero gancho alto kilometraje', '138': 'Serv. Educativos',
             '128': ': Música', '812': 'Producto: Software Emulador de Teclado Virtual -CENAREC-.',
             '693': 'Producto: Sistema de montaje para comunicadores -CENAREC-.', '119': 'Educación para el Hogar',
             '1144': 'Venta producto de apoyo - Aspirador de Flemas', '227': 'Almohada termica',
             '98': 'Serv. Gestión y canalización de fondos para proyecto de bien social.',
             '158': 'Antifaz para dormir', '559': 'Prod. Impresora Braille - Braillo 300',
             '1102': 'Bolsas para agua caliente', '592': 'Prod. Baston plegable fibra vidrio',
             '616': 'Prod. Bloque bolsillo para aprender braille', '589': 'Prod. Mouse Adaptado con switch',
             '1048': 'Silla Baño con respaldo asiento en U', '1023': 'Corset Jewett',
             '867': 'Producto: Teclado de conceptos con conexión USB - CENAREC-.',
             '593': 'Prod. Mouse Slimblade trackball', '588': 'Prod. Bandeja actividades',
             '886': 'Ferula ortoplast adulto', '417': 'Tiflotecnología', '156': 'Termometro axilar digital',
             '882': 'Ferula para mano antiespasmica', '1067': 'Barra Cromada 32 pulgadas',
             '842': 'Producto: Mueble de posicionamiento prono -CENAREC-.', '535': 'Prod. Handshoe mouse',
             '495': 'Producto: rompecabezas animales de granja en braille', '421': 'Tiflotecnología',
             '716': 'Producto: Comunicador multinivel de 32 casillas -CENAREC-.',
             '402': 'Ortesis de hombro - talla: s, m, l', '816': 'Producto: Reloj braille -CENAREC-.',
             '477': 'Producto: cargador portátil energía solar', '193': 'Máscara Nebulizador pediatrico',
             '861': 'Producto: Dispositivo para lectura automática -CENAREC-.',
             '1143': 'Alquiler Gigante para Suero', '374': 'Silla de baño sin respaldo',
             '629': 'Prod. Cama ortopedica', '590': 'Prod. Bastón plegable para soporte',
             '1092': 'Silla Ruedas sencilla', '1208': 'Plataforma vertical STA-FLE', '215': 'Cojin lumbar',
             '532': 'Prod. Material desarrollo motora fina', '510': 'Producto: reloj braille para mujer',
             '211': 'Glucometros digitales', '1126': 'Prod. Muleta Universal', '976': 'Ferula pie niño',
             '680': 'Producto: Magnificador portátil -CENAREC-.', '906': 'Ferulas Polietileno niño',
             '931': 'Muleta canadiense', '439': 'Producto: lupa con luz LED 2 en 1',
             '712': 'Producto: Sintetizador de voz con Teclado Portátil Braille tipo Perkins -CENAREC-.',
             '1018': 'Zapato ortopedico bajo molde yeso niño', '205': 'Andadera con asiento',
             '517': 'Producto: lupa electronica hd de bolsillo', '524': 'Producto: guia para firmar con lupa',
             '1089': 'Inodoro Portatil 3 en 1 con ruedas', '797': 'Producto Apoyo: Andadera -CENAREC-.',
             '74': 'Centro Atención Integral', '923': 'Relleno anterior y corslette pierna',
             '240': 'Alquiler camas ortopedicas', '689': 'Producto: Despertador vibratorio Hal-Hen -CENAREC-.',
             '462': 'Producto: reloj para caballero con sintetizador de voz',
             '611': 'Prod. Prod. Material desarrollo de habilidades', '591': 'Prod. Impresora Braille Box',
             '499': 'Producto: elevador eléctrico pacientes', '325': 'FÉRULA DE DEDO ALUMINIO',
             '929': 'Corset Milwalke', '194': 'almohada ortopedica', '626': 'Prod. Teclado Portátil',
             '304': 'COLCHONETA KINDER Y GIMNASIO VINIL', '488': 'Producto: lupa de mano con luz integrada',
             '54': 'Fisioterapia',
             '771': 'Producto: Software juego interactivos par Personas con Autismo -CENAREC-.',
             '729': 'Producto: Mesa Reclinable -CENAREC-.',
             '518': 'Producto: magnificador de imágenes portatil 1.5x - 25x', '244': 'Collar de Thomas',
             '843': 'Producto: Magnificador digital de bolsillo -CENAREC-.', '17': 'Terapia Física',
             '799': 'Producto: Conmutador con sensor de movimientos musculares -CENAREC-.', '914': 'Prótesis muslo',
             '864': 'Producto: Software Emulador de mouse -CENAREC-.', '48': 'Terapia de Lenguaje',
             '710': 'Comunicador con 7 casillas -CENAREC-.', '235': 'Alquiler de Equipo Médico - Silla Baño',
             '856': 'Conmutador para apretar -CENAREC-.',
             '491': 'Producto: set geometria tactiles y alto contraste', '24': 'Psicología',
             '879': 'Producto: Teclado de colores - CENAREC-.', '990': 'Ortesis cables flexibles articulados (par)',
             '999': 'Silla Ruedas Especializadas', '376': 'Bastón de una punta, diferentes colores',
             '186': 'Barra para baño', '1051': 'Barra Cromada 24 pulgadas',
             '255': 'Botas Inmovilizadoras con Aire. (Férula Tipo Walker)', '888': 'Prótesis ocular',
             '620': 'Prod. Puntero Slip-on tipo lápiz', '153': 'Fajas inguinales', '1079': 'Ejercitador de mano',
             '406': 'SOPORTE ESCROTAL ATLÉTICO', '237': 'Alquiler de Equipo Médico - Silla de Ruedas',
             '752': 'Producto: conmutador juguetes -CENAREC-.',
             '67': 'Servicio alquiler o préstamo de sillas ruedas no ortopedicas.',
             '733': 'Producto: Software permite creación y personalización actividades didácticas - CENAREC-.',
             '922': 'Zapato ortopedico bajo molde yeso niño', '643': 'Prod. Colchón de agua',
             '446': 'Producto: rompecabezas de formas y colores', '338': 'LIGA THERA-BAND VERDE',
             '60': 'Serv. Apoyo Legal',
             '5': 'Asesoría técnica sobre petición de ayudas o procedimientos estatales.',
             '1078': 'Silla Brazo Fijo pies desmontable', '302': 'COMPRESA FRÍO CALOR PARA CERVICAL Y HOMBROS',
             '700': 'Producto: Software Emulador de Mouse -CENAREC-.',
             '852': 'Producto: Software Emulador que permite escribir Windows -CENAREC-.', '191': 'Pantorrillera',
             '500': 'Producto: juego dominó piezas grandes diseño animales',
             '214': 'Protector de gel para dedo pulgar', '1123': 'Rodillera con rotula',
             '800': 'Producto: Conmutador inalámbrico de tipo pulsador -CENAREC-.',
             '765': 'Producto: Software Emulador Mouse -CENAREC-.',
             '363': 'Silla transporte 19 pulgadas color azul', '994': 'Protesis cardiacas biológica mitral',
             '985': 'Prótesis Mamaría', '64': 'Serv. Educativos', '694': 'Producto: Mouse con laser -CENAREC-.',
             '674': 'Producto apoyo: Alimentador Electrónico -CENAREC-.', '1025': 'Corset Milwalke',
             '667': 'Salvaescalera Ischia', '699': 'Producto: Monitor inalámbrico para bebés -CENAREC-.',
             '92': 'Terapia del lenguaje, habla y voz', '253': 'ANDADERAS', '939': 'Audifono Retro auricular',
             '878': 'Producto: Reloj digital parlante -CENAREC-.',
             '1147': 'Producto de apoyo - Venta Compresor Oxigeno New Life Elite', '197': 'Canula de oxigeno nasal',
             '738': 'Producto: Impresora Braille -CENAREC-.', '1202': 'Salvaescalera',
             '1038': 'Estabilizador universal pulgar', '280': 'COJÍN DE ESPUMA',
             '833': 'Producto: Software Conversor texto a audio -CENAREC-.', '1197': 'Silla Salvaescalera A180',
             '265': 'Estabilizador de Tobillo', '410': 'Prod. Faja Costal', '545': 'Prod. Calendario aula',
             '115': 'Asistencia Médica Gratuita',
             '819': 'Producto: Conmutador de tipo pulsador con conector USB -CENAREC-.', '891': 'Ortesis al tercio',
             '192': 'Bola para terapia diferentes tamaños', '1012': 'Zapato ortopedico bajo molde yeso adulto',
             '1177': 'Venta producto de apoyo - Nebulizador Niño',
             '724': 'Producto: Editor de textos Braille - CENAREC-.',
             '441': 'Producto: reloj para mujer diseño elegante con voz español y bicolor',
             '732': 'Producto: Perilla Universal -CENAREC-.', '656': 'CORSE JEWET',
             '615': 'Prod. Reloj Parlante y braille, oro, para hombre', '577': 'Prod. Bastón plegable de grafito',
             '1141': 'Venta producto de apoyo - Bidet Acero', '933': 'Collar duro tipo thomas',
             '661': 'Ascensor Celsus'}

    item_name = get_item_name(text)
    groups = get_product_group(text)

    for key, value in names.items():
        value = str(value)
        if value == item_name:
            print("-VALUE HIT-")
            if groups != []:
                for group in groups:
                    line = str(line + str(key) + "|" + str(group) + "+")

            else:
                line = str(line + str(key) + "|13+")

    print(line)
    return line


def generate_group_superString(productMatrix):
    superString = ""
    for i in range(len(productMatrix)):
        path = productMatrix[i][0]
        # print(path)
        text = get_text_from(path , False)

        superString = superString + generate_group_line(text)


    print(superString)
    return superString

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
    get_service_orgIdFk(text)


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
        test_product_functions(get_text_from(fileMatrx[i][0] , False))
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
    get_organization_idFk_product(text)


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
        test_org_product_functions(get_text_from(fileMatrx[i][0] , False))
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


def generate_Items_Services_dictionary(serviceMatrix):
    Items = []
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


def generate_Products_dictionary(productMatrix):
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
            temp["cost"] = ">>" + get_product_cost(text) + ">>"
            temp["warranty"] = ">>No brinda información>>"
            temp["inStock"] = get_product_instock(text)
            temp["timeDelevery"] = ">>" + get_product_timeDelivery(text) + ">>"
            temp["warrantyImported"] = ">>No brinda información>>"
            temp["usefulLife"] = ">>" + get_product_usefulLife(text) + ">>"
            temp["spareParts"] = ">>No brinda información>>"
            temp["primaryFunctionalities"] = ">>" + get_product_primaryFuncionalities(text) + ">>"
            temp["secondlyFunctionalities"] = ">>No brinda información>>"
            temp["brand"] = ">>" + get_product_brand(text) + ">>"
            temp["model"] = ">>No brinda información>>"
            temp["height"] = ">>No brinda información>>"
            temp["width"] = ">>No brinda información>>"
            temp["deep"] = ">>No brinda información>>"
            temp["weight"] = ">>No brinda información>>"
            temp["Items_idPk"] = get_product_orgIdFk(text)
            i += 1

            Products.append(copy.deepcopy(temp))

    return Products


def generate_Services_dictionary(serviceMatrix):
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
            temp["Items_idPk"] = get_service_orgIdFk(text)
            i += 1

            Services.append(copy.deepcopy(temp))

    return Services


def generate_dictionaries(serviceMatrix , productMatrix):
    itemCounter = 1
    productCounter = 1
    serviceCounter = 1

    items = []
    products = []
    services = []

    orgRDY = []

    for row in serviceMatrix:
        path = row[0]
        try:
            image = row[1]
        except:
            image = "/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png"

        text = get_text_from(path , False)

        service = {}
        item = {}

        service["idPk"] = serviceCounter
        service["isPrivate"] = get_service_isPrivate(text)
        service["cost"] = ">>" + get_service_cost(text) + ">>"
        service["objectives"] = ">>" + get_service_objectives(text) + ">>"
        service["reaches"] = ">>" + get_service_reaches(text) + ">>"
        service["specificSupports"] = ">>" + get_service_specificSupports(text) + ">>"
        service["typeSupports"] = ">>" + get_service_typeSupports(text) + ">>"
        service["daysToOperations"] = [{}]
        service["responsabilityPerson"] = ">>" + get_service_responsabilityPerson(text) + ">>"
        service["cover"] = ">>" + get_service_cover(text) + ">>"
        service["requirements"] = ">>" + get_service_requirements(text) + ">>"
        service["accesibility"] = ">>" + get_service_accesibility(text) + ">>"
        service["others"] = ">>" + get_service_others(text) + ">>"
        service["scheduleExtraordinary"] = get_service_scheduleExtraoerdinary(text)
        service["otherExtraordinaryAttention"] = ">>" + get_service_otherExtraordinaryAttention(text) + ">>"
        service["attentionFrecuency"] = ">>" + get_service_attentionFrecuency(text) + ">>"
        service["Items_idPk"] = itemCounter

        services.append(copy.deepcopy(service))
        serviceCounter += 1


        item["idPk"] = itemCounter
        item["code"] = ">>No brinda información>>"
        item["name"] = ">>" + get_item_name(text) + ">>"
        item["description"] = ">>" + get_item_description_service(text) + ">>"
        item["observations"] = ">>" + get_item_observations_services(text) + ">>"
        item["image1"] = encode_image("/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png")
        item["image2"] = "imagen"
        item["image3"] = "imagen"
        item["visibility"] = 1
        item["isProduct"] = 0
        item["onDateUpdated"] = get_date()
        item["onDateCreated"] = get_date()
        item["daysToOperations"] = [{}]
        item["typeDeficiency"] = ">>" + get_item_typeDeficiency(text) + ">>"
        item["age"] = "[" + str(get_item_age(text)) + "]"
        item["sex"] = 2
        item["isForPregnant"] = 1
        item["isApproved"] = 1
        item["isChecked"] = 1
        item["isDeleted"] = 0
        item["organizationsIdFk"] = get_organization_idFk_service(text)

        items.append(copy.deepcopy(item))
        itemCounter += 1



    for row in productMatrix:
        path = row[0]
        try:
            image = row[1]
        except:
            image = "/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png"

        text = get_text_from(path , False)

        product = {}
        item = {}

        product["idPk"] = productCounter
        product["cost"] = ">>" + get_product_cost(text) + ">>"
        product["warranty"] = ">>No brinda información>>"
        product["inStock"] = get_product_instock(text)
        product["timeDelevery"] = ">>" + get_product_timeDelivery(text) + ">>"
        product["warrantyImported"] = 0
        product["usefulLife"] = ">>" + get_product_usefulLife(text) + ">>"
        product["spareParts"] = [{}]
        product["primaryFunctionalities"] = ">>" + get_product_primaryFuncionalities(text) + ">>"
        product["secondlyFunctionalities"] = [{}]
        product["brand"] = ">>" + get_product_brand(text) + ">>"
        product["model"] = ">>No brinda información>>"
        product["height"] = ">>No brinda información>>"
        product["width"] = ">>No brinda información>>"
        product["deep"] = ">>No brinda información>>"
        product["weight"] = ">>No brinda información>>"
        product["Items_idPk"] = itemCounter

        products.append(copy.deepcopy(product))
        productCounter += 1


        item["idPk"] = itemCounter
        item["code"] = ">>No brinda información>>"
        item["name"] = ">>" + get_item_name(text) + ">>"
        item["description"] = ">>" + get_item_description_products(text) + ">>"
        item["observations"] = ">>" + get_item_observations_products(text) + ">>"
        item["image1"] = encode_image("/home/fabian/Documents/repositories/adam_system/adam4/res/not-available-es.png")
        item["image2"] = ">>imagen>>"
        item["image3"] = ">>imagen>>"
        item["visibility"] = 1
        item["isProduct"] = 1
        item["onDateUpdated"] = get_date()
        item["onDateCreated"] = get_date()
        item["daysToOperations"] = [{}]
        item["typeDeficiency"] = ">>" + get_item_typeDeficiency(text) + ">>"
        item["age"] = "[" + str(get_item_age(text)) + "]"
        item["sex"] = 2
        item["isForPregnant"] = 1
        item["isApproved"] = 1
        item["isChecked"] = 1
        item["isDeleted"] = 0
        item["organizationsIdFk"] = get_organization_idFk_product(text)

        items.append(copy.deepcopy(item))
        itemCounter += 1

    print("Total items: " + str(itemCounter) + "\tTotal products: " + str(productCounter) + "\tTotal services: " + str(serviceCounter))

    return [items , products , services]



def get_organization_idFk_service(text):
    orgCounter = {'44': 'Asociación Pro niños con Parálisis Cerebral Cartago',
                  '33': 'Centro Educación Especial Carlos Luis Valle',
                  '47': 'Asociación para la Atención Integral de Personas Adultas con Discapacidad “El sol Brilla para Todos” CAIPAD',
                  '68': 'Fundación Hogar Manos Abiertas.', '19': 'Hospital Express',
                  '2': 'Asociación Central Pro-Ayuda de la Persona con Discapacidad de Palmares - APRADIS',
                  '76': 'Asociación Amigos del Grupo de Percusión-Inclusión -AAGRUPERI-',
                  '25': 'Hospital La Anexión - CCSS',
                  '27': 'Asociación Semillas de Esperanza Pro-Apoyo y Rehabilitación de Hojancha, Guanacaste.',
                  '15': 'Ayudas Técnicas que entrega la CCSS como institución en cada uno de sus hospitales.',
                  '55': 'Hospital San Rafael de Alajuela - CCSS', '37': 'Instituto Tecnológico de Costa Rica',
                  '36': 'Clínicas de la Audición', '18': 'Equipo Médico Montes Oca', '39': 'Asociación Seres de Luz',
                  '60': 'Asociación MORFAS (Miembros Organizados Fomentando Acciones Solidarias).',
                  '58': 'Hospital de San Carlos - CCSS', '3': 'Alquiler Médicos ByB', '10': 'Disprodorme S.A',
                  '32': 'Asociación Fraternidad Cristiana de Personas con Discapacidad',
                  '17': 'Hospital del Trauma del INS y sus clínicas alrededor del país.',
                  '43': 'Asociación Costarricense de Artriticos',
                  '49': 'Asociación de Personas con Discapacidad de Upala, ADEDISUPA.',
                  '26': 'Fundación Senderos de Oportunidades',
                  '70': 'Ministerio de Educación Pública: Centro de Enseñanza Especial Marta Saborío Fonseca, Alajuela',
                  '46': 'Hospital Carlos Luis Valverde Vega CCSS', '62': 'Asociación de Transparencia.',
                  '71': 'Asociación de Ayuda al Minusválido de San Carlos, AYUMISANCA.', '8': 'TifloproductosCR',
                  '65': 'Asociación Taller Protegido de Alajuela.', '69': 'Centro de educación especial Grecia',
                  '54': 'Centro de Educación Especial de Turrialba',
                  '1': 'Synapsis Medical, Tienda Ortopédica Y Equipo Medico',
                  '40': 'Colegio Universitario de Cartago -CUC', '64': 'Asociación Talita Cumi.',
                  '73': 'Municipalidad de Alajuela',
                  '50': 'Asociación Taller de Atención Integral y Capacitación, ATAICA.', '38': 'Clínica Fisiosport',
                  '75': 'Asociación Centro de Integración Ocupacional y Servicios Afines, ACIOSA',
                  '48': 'Fundación Doctora Chinchilla de Reyes.',
                  '31': 'Asociación de Apoyo a la Unidad de Rehabilitación Profesional de Turrialba.',
                  '16': 'Clínica Dinamarca', '21': 'Municipalidad de Carrillo, Guanacaste', '29': 'AZMONT S.A',
                  '67': 'Asociación Costarricense Pro- Ayuda al Epiléptico, ACOPE.', '42': 'Municipalidad de Cartago.',
                  '52': 'Fundación Servio Flores Arroyo', '6': 'Sear Médica',
                  '35': 'Clinica de Terapia Física María Goretti.', '5': 'Ortopédica Garbanzo',
                  '23': 'Asociación de Personas con Discapacidad -APEDI- GUANACASTE',
                  '4': 'Asociación Costarricense de Distrofia Muscular, ACODIM.',
                  '56': 'Asociación Sarchiseña de Discapacitados, ASADIS', '41': 'Asociación Atjala ( CAIPAD)',
                  '7': 'Asociación Pro-Patronato Nacional de Ciegos.',
                  '57': 'Asociación Pro-Ayuda a la Persona con Discapacidad de Zarcero, Llano Bonito y San Antonio, APAMAR',
                  '61': 'Asociación Pro-Personas con Discapacidad de Atenas -APRODISA-',
                  '74': 'Asociación Centro de Formación Socio-Productivo para el Desarrollo de las Personas Discapacitadas.',
                  '14': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.',
                  '51': 'Asociación para la Promoción de la Salud Mental, APROSAM.',
                  '24': 'Asociación Guanacasteca de Discapacidad, Autonomía y Comunidad Inclusiva, AGUDACI.',
                  '53': 'Fundación Amor y Esperanza.',
                  '12': 'Asociación pro Hospital Nacional de Geriatría y Gerontología Dr. Raúl Blanco Cervantes, APRONAGE.',
                  '11': 'Centro Educativo Dr. Carlos Sáenz Herrera',
                  '59': 'Centro Especializado en Terapia del lenguaje, habla y voz', '13': 'JR Sánchez Audiología',
                  '45': 'Asociación de Desarrollo Educativo de Paraíso -ASODEPA-',
                  '22': 'Centro de Terapia de Lenguaje y Guarderia Semillitas de Dios',
                  '34': 'Hospital Nacional Psiquiátrico - CCSS Roberto Chacón Paut',
                  '66': 'Centro de Terapia Asistida con Animales.', '9': 'Empresa Brailler Inc. Costa Rica',
                  '30': 'Chupis Ortopédica', '28': 'Hospital William Allen Taylor - CCSS',
                  '20': 'Sistema de Accesibilidad Total S.A', '63': 'Municipalidad de San Carlos.',
                  '72': 'Asociación Costarricense de Personas con Discapacidad Visual, ACOPEDIV'}

    name = get_org_name_service(text)

    for key , value in orgCounter.items():
        value = str(value)
        if value == name:
            print("\t\033[94morganizationsIdFk:\033[0m " + key)
            return key

    print("\t\u001B[31morganizationsIdFk:\033[0m ERROR -----------------------------------------------------------------------------------------------")
    return 100


def get_organization_idFk_product(text):
    orgCounter = {'44': 'Asociación Pro niños con Parálisis Cerebral Cartago',
                  '33': 'Centro Educación Especial Carlos Luis Valle',
                  '47': 'Asociación para la Atención Integral de Personas Adultas con Discapacidad “El sol Brilla para Todos” CAIPAD',
                  '68': 'Fundación Hogar Manos Abiertas.', '19': 'Hospital Express',
                  '2': 'Asociación Central Pro-Ayuda de la Persona con Discapacidad de Palmares - APRADIS',
                  '76': 'Asociación Amigos del Grupo de Percusión-Inclusión -AAGRUPERI-',
                  '25': 'Hospital La Anexión - CCSS',
                  '27': 'Asociación Semillas de Esperanza Pro-Apoyo y Rehabilitación de Hojancha, Guanacaste.',
                  '15': 'Ayudas Técnicas que entrega la CCSS como institución en cada uno de sus hospitales.',
                  '55': 'Hospital San Rafael de Alajuela - CCSS', '37': 'Instituto Tecnológico de Costa Rica',
                  '36': 'Clínicas de la Audición', '18': 'Equipo Médico Montes Oca', '39': 'Asociación Seres de Luz',
                  '60': 'Asociación MORFAS (Miembros Organizados Fomentando Acciones Solidarias).',
                  '58': 'Hospital de San Carlos - CCSS', '3': 'Alquiler Médicos ByB', '10': 'Disprodorme S.A',
                  '32': 'Asociación Fraternidad Cristiana de Personas con Discapacidad',
                  '17': 'Hospital del Trauma del INS y sus clínicas alrededor del país.',
                  '43': 'Asociación Costarricense de Artriticos',
                  '49': 'Asociación de Personas con Discapacidad de Upala, ADEDISUPA.',
                  '26': 'Fundación Senderos de Oportunidades',
                  '70': 'Ministerio de Educación Pública: Centro de Enseñanza Especial Marta Saborío Fonseca, Alajuela',
                  '46': 'Hospital Carlos Luis Valverde Vega CCSS', '62': 'Asociación de Transparencia.',
                  '71': 'Asociación de Ayuda al Minusválido de San Carlos, AYUMISANCA.', '8': 'TifloproductosCR',
                  '65': 'Asociación Taller Protegido de Alajuela.', '69': 'Centro de educación especial Grecia',
                  '54': 'Centro de Educación Especial de Turrialba',
                  '1': 'Synapsis Medical, Tienda Ortopédica Y Equipo Medico',
                  '40': 'Colegio Universitario de Cartago -CUC', '64': 'Asociación Talita Cumi.',
                  '73': 'Municipalidad de Alajuela',
                  '50': 'Asociación Taller de Atención Integral y Capacitación, ATAICA.', '38': 'Clínica Fisiosport',
                  '75': 'Asociación Centro de Integración Ocupacional y Servicios Afines, ACIOSA',
                  '48': 'Fundación Doctora Chinchilla de Reyes.',
                  '31': 'Asociación de Apoyo a la Unidad de Rehabilitación Profesional de Turrialba.',
                  '16': 'Clínica Dinamarca', '21': 'Municipalidad de Carrillo, Guanacaste', '29': 'AZMONT S.A',
                  '67': 'Asociación Costarricense Pro- Ayuda al Epiléptico, ACOPE.', '42': 'Municipalidad de Cartago.',
                  '52': 'Fundación Servio Flores Arroyo', '6': 'Sear Médica',
                  '35': 'Clinica de Terapia Física María Goretti.', '5': 'Ortopédica Garbanzo',
                  '23': 'Asociación de Personas con Discapacidad -APEDI- GUANACASTE',
                  '4': 'Asociación Costarricense de Distrofia Muscular, ACODIM.',
                  '56': 'Asociación Sarchiseña de Discapacitados, ASADIS', '41': 'Asociación Atjala ( CAIPAD)',
                  '7': 'Asociación Pro-Patronato Nacional de Ciegos.',
                  '57': 'Asociación Pro-Ayuda a la Persona con Discapacidad de Zarcero, Llano Bonito y San Antonio, APAMAR',
                  '61': 'Asociación Pro-Personas con Discapacidad de Atenas -APRODISA-',
                  '74': 'Asociación Centro de Formación Socio-Productivo para el Desarrollo de las Personas Discapacitadas.',
                  '14': 'Centro Nacional de Recursos para la Educación Inclusiva -CENAREC-.',
                  '51': 'Asociación para la Promoción de la Salud Mental, APROSAM.',
                  '24': 'Asociación Guanacasteca de Discapacidad, Autonomía y Comunidad Inclusiva, AGUDACI.',
                  '53': 'Fundación Amor y Esperanza.',
                  '12': 'Asociación pro Hospital Nacional de Geriatría y Gerontología Dr. Raúl Blanco Cervantes, APRONAGE.',
                  '11': 'Centro Educativo Dr. Carlos Sáenz Herrera',
                  '59': 'Centro Especializado en Terapia del lenguaje, habla y voz', '13': 'JR Sánchez Audiología',
                  '45': 'Asociación de Desarrollo Educativo de Paraíso -ASODEPA-',
                  '22': 'Centro de Terapia de Lenguaje y Guarderia Semillitas de Dios',
                  '34': 'Hospital Nacional Psiquiátrico - CCSS Roberto Chacón Paut',
                  '66': 'Centro de Terapia Asistida con Animales.', '9': 'Empresa Brailler Inc. Costa Rica',
                  '30': 'Chupis Ortopédica', '28': 'Hospital William Allen Taylor - CCSS',
                  '20': 'Sistema de Accesibilidad Total S.A', '63': 'Municipalidad de San Carlos.',
                  '72': 'Asociación Costarricense de Personas con Discapacidad Visual, ACOPEDIV'}

    name = get_org_name_product(text)

    for key , value in orgCounter.items():
        value = str(value)
        if value == name:
            print("\t\033[94morganizationsIdFk:\033[0m " + key)
            return key

    print("\t\u001B[31morganizationsIdFk:\033[0m ERROR -----------------------------------------------------------------------------------------------")
    return 100



def dic2csv_orgs(dictionaries):
    cols_name = ["idPk", "dni" , "name" , "email" , "web" , "telephone" , "legalRepresentative" , "assembly" , "socialNetworks" , "wazeAddress" , "schedule" , "reaches" , "mision" , "vision" , "objetive" , "dayOperations" ,"isAproved" , "isChecked" , "isDeleted" , "organizationsTypesidPk"]
    file = open("orgs.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("orgs.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    file = open("orgs.csv", "w")
    file.write(new)
    file.close()

def dic2csv_items(dictionaries):
    cols_name = ["idPk" , "code" , "name" , "description" , "observations" , "image1" , "image2" , "image3" , "visibility" , "isProduct" , "onDateUpdated" , "onDateCreated" , "daysToOperations" , "typeDeficiency" , "age" , "sex" , "isForPregnant" , "isApproved" , "isChecked" , "isDeleted" , "organizationsIdFk"]
    file = open("items.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("items.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    new = new.replace("{'age': '" , "{\"'age'\": \"'")
    new = new.replace("'}" , "'\"}")
    new = new.replace("\"\"Formar profesionales" , "\"Formar profesionales")
    new = new.replace("programas culturales.\"\"" , "programas culturales.\"")
    file = open("items.csv", "w")
    file.write(new)
    file.close()



def dic2csv_products(dictionaries):
    cols_name = ["idPk", "cost", "warranty", "inStock", "timeDelevery", "warrantyImported", "usefulLife", "spareParts","primaryFunctionalities", "secondlyFunctionalities", "brand", "model", "height", "width", "deep", "weight","Items_idPk"]
    file = open("products.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("products.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    new = new.replace(";\"\";" , ";\"No brinda información\";")
    new = new.replace(";\"\"", ";\"")
    new = new.replace("\"\";", "\";")
    file = open("products.csv", "w")
    file.write(new)
    file.close()



def dic2csv_services(dictionaries):
    cols_name = ["idPk", "isPrivate", "cost", "objectives", "reaches", "specificSupports", "typeSupports", "daysToOperations",
     "responsabilityPerson", "cover", "requirements", "accesibility", "others", "scheduleExtraordinary",
     "otherExtraordinaryAttention", "attentionFrecuency", "Items_idPk"]
    file = open("services.csv", "w")

    with file:
        csv.register_dialect("toMYSQL", delimiter=";")
        writer = csv.DictWriter(file, fieldnames=cols_name, dialect="toMYSQL")
        writer.writeheader()
        for dict in dictionaries:
            writer.writerow(dict)
        file.close()

    file = open("services.csv", "r")
    old = file.read()
    file.close()
    new = old.replace(">>", "\"")
    new = new.replace("\";\"\"Facilitar" , "\";\"Facilitar")
    new = new.replace("desenvuelve.\"\";\"No hay." , "desenvuelve.\";\"No hay.")
    new = new.replace("______________________" , "No brinda información.")
    file = open("services.csv", "w")
    file.write(new)
    file.close()



# ------------------------------------MAIN------------------------------------ #

def main():
    print("          _____          __  __    _______     _______ _______ ______ __  __ \n    /\   |  __ \   /\   |  \/  |  / ____\ \   / / ____|__   __|  ____|  \/  |\n   /  \  | |  | | /  \  | \  / | | (___  \ \_/ / (___    | |  | |__  | \  / |\n  / /\ \ | |  | |/ /\ \ | |\/| |  \___ \  \   / \___ \   | |  |  __| | |\/| |\n / ____ \| |__| / ____ \| |  | |  ____) |  | |  ____) |  | |  | |____| |  | |\n/_/    \_\_____/_/    \_\_|  |_| |_____/   |_| |_____/   |_|  |______|_|  |_|\n                    -Automatic Database Migration System-                    \n\n\n")
    serviceMatrix = get_files_from("/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Servicios de apoyo")
    productMatrix = get_files_from("/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Productos de apoyo/")

    # path = "/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Productos de apoyo/Heredia/Ortop__dica Garbanzo/bota walker/Ortopedica Garbanzo - BOTA WALKER.docx"
    # get_text_from(path , True)

    generate_group_superString(productMatrix)








if __name__ == "__main__":
    main()



















