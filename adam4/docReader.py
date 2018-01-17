import base64
import datetime
import json
import re
import string
from os import walk
from os.path import join, abspath , splitext
import base64
import datetime
import copy
import pprint
import docx2txt
import sys
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

def get_text_from(path):
    """Extract and format text from a docx file.

    Keyword arguments:
    path -- path to the file
    """
    text = ""
    try:
        text = str(docx2txt.process(path))                         # gets text from a docx
    except:
        None
    text = text.replace("Sí", "Si")                            # replaces characters
    text = text.replace("sí", "Si")                            # replaces characters
    text = text.replace("Observaciones :" , "Observaciones:")  # remove the extra space on "Observaciones" word
    text = text.replace("Teléfono (s)" , "telelelelele")
    text = text.replace("Teléfono(s)", "telelelelele")
    text = text.replace("Teléfono (s) ", "telelelelele")
    text = text.replace("Teléfono(s) ", "telelelelele")
    text = text.replace("telelelelele:", "telelelelele")
    #text = text.replace("Señale el tipo de oferente del producto de apoyo", " Señale el tipo de oferente del servicio de apoyo")
    text = text.replace("Nombre del servicio de apoyo"," Nombre del producto de apoyo")
    text = text.replace("Fax:", "Fax")
    text = text.replace("fax:", "Fax")
    text = text.replace("fax", "Fax")
    text = text.replace("\n" , " ")                            # removes all newline characters from text
    text = text.replace("\t" , " ")                            # replaces tabs with spaces
    text = text.replace("●" , "")                              # removes all bullets from text
    text = re.sub(' +' , ' ' , text)                           # removes all repeated whitespace from text
    #print("\033[94mTEXTO: \033[0m" + text)
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
        encodedIimage = base64.b64encode(image_file.read())

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

def get_item_name_product(text):
    start = "de apoyo que se brinda "
    if text.find(start) == -1:
        start = "de apoyo como lo enuncia la entidad que lo brinda."
        if text.find(start) == -1:
            start = "de apoyo, como lo enuncia la entidad que lo brinda."
    end = "7. Uso y aplicaciones del producto de apoyo:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mName of product:\033[0m " + needle)
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
    return needle


def get_item_description(text):
    start = "Fines:"
    if text.find(start) == -1:
        print("\t\033[94mDescription of product/service:\033[0m -")
        return "-"
    else:
        end = "Misión:"
        needle = text[text.find(start) + len(start): text.find(end)]
        print("\t\033[94mDescription of product/service:\033[0m " + needle)
        return needle


def get_item_observations(text):
    start = "Observaciones:"
    end = "Para uso interno "
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mObservations:\033[0m " + needle)
    return needle

def get_item_typeDeficiency(text):
    start = "Tipo de discapacidad:"
    end = "Otra:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mtypeDeficiency:\033[0m " + needle)
    return needle


def get_item_age(text):
    start = "Grupo etario (edad):"
    end = "Tipo de discapacidad:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mage:\033[0m " + needle)
    return needle


def get_item_sex(text):
    start = "Género:"
    end = "Grupo etario"
    needle = text[text.find(start) + len(start): text.find(end)]

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


# ------------------------------------ORGANIZATIONS------------------------------------ #
#TODO ARREGLAR ESTA VARA (que sirva para servicios y ademas verificar que sea de  la organizacion y no del productio/servicio)
def get_org_name_product(text):
    start = "Nombre del ente que brinda el producto de apoyo (institución, municipalidad, empresa u organización no gubernamental):"
    if text.find(start) == -1:
        start = "Nombre del ente que brinda el servicio de apoyo (institución, municipalidad, empresa u organización no gubernamental):"
    end = "4. Descripción del ente que brinda el producto de apoyo"
    if text.find(end) == -1:
        end = "4. Descripción del ente"
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mname:\033[0m " + needle)
    return needle


def get_org_email_product(text):
    start = "Dirección de correo electrónico:"
    end = "Web del servicio:"
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94memail:\033[0m " + needle)
    return needle


def get_org_web_product(text):
    start = "Web del servicio:"
    end = "Redes sociales:"
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mwebsite:\033[0m " + needle)
    return needle


def get_org_telephone_product(text):
    start = " telelelelele "
    end = "Dirección de correo electrónico:"
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
    #print("\t\033[94mtelephone:\033[0m " + needle)
    return needle


def get_org_socialnetworks_product(text):
    start = "Redes sociales:"
    end = "Dirección waze:"
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
    #print("\t\033[94msocialnetworks:\033[0m " + str(dict))
    return dict


def get_org_wazeAddress_product(text):
    start = "Dirección waze:"
    end = "Ubicación"
    needle = text[text.find(start) + len(start): text.find(end)]
    urls = re.findall(urlmarker.WEB_URL_REGEX, needle)
    #print("\t\033[94mwazeAddress:\033[0m " + str(urls))
    return urls


def get_org_reaches_product(text):
    start = " Fines: "
    end = " Misión: "
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mreaches:\033[0m " + needle)
    return needle


def get_org_mision_product(text):
    start = " Misión: "
    end = " Visión: "
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mmision:\033[0m " + needle)
    return needle


def get_org_vision_product(text):
    start = " Visión: "
    end = " Objetivos: "
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mvision:\033[0m " + needle)
    return needle


def get_org_objective_product(text):
    start = " Objetivos: "
    end = " Señale el tipo de oferente del servicio de apoyo"
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mobjective:\033[0m " + needle)
    needle = needle.replace("5." , "")
    return needle


def get_org_dayOperations_product(text):
    start = "de la semana que atienden para la obtención de productos de apoyo. "
    end = "Forma de atención:"
    needle = text[text.find(start) + len(start): text.find(end)]
    #print("\t\033[94mdayOperations:\033[0m " + needle)
    needle = needle.replace("13.", "")
    return needle


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
        #print("\t\033[94mtypesidPk:\033[0m 3")
        return 3

    elif(needle2.replace(" " , "") == "x" or needle2.replace(" " , "") == "X"):
        #print("\t\033[94mtypesidPk:\033[0m 2")
        return 2

    elif (needle3.replace(" ", "") == "x" or needle3.replace(" ", "") == "X"):
        #print("\t\033[94mtypesidPk:\033[0m 4")
        return 4

    elif (needle4.replace(" ", "") == "x" or needle4.replace(" ", "") == "X"):
        #print("\t\033[94mtypesidPk:\033[0m 1")
        return 1

    else:
        #print("\t\u001B[31mtypesidPk:\033[0m 1")
        return 1


# ------------------------------------SERVICES------------------------------------ #

def get_service_isPrivate(text):
    start = "Costo: Indique si es un servicio público, privado y el costo del mismo en términos de tiempo / costo. Servicio público ("
    end = ") Servicio privado ("
    needle = text[text.find(start) + len(start): text.find(end) + 1]
    if needle.replace(" " , "") == "X" or needle.replace(" " , "") == "x":
        print("\t\033[94misPrivate:\033[0m 0")
        return 0
    else:
        print("\t\033[94misPrivate:\033[0m 1")
        return 1


def get_service_cost(text):
    start = ") Costo del servicio: "
    end = "Tiempo/costo:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mcost:\033[0m " + needle)
    return needle


def get_service_objectives(text):
    start = "Objetivos: "
    end = " Apoyos específicos que brinda: "
    needle = text[find_nth(text , start , 2) + len(start): text.find(end)]
    print("\t\033[94mobjectives:\033[0m " + needle)
    return needle


def get_service_reaches(text):
    start = "Descripción del servicio: Fines: "
    end = " Objetivos: "
    needle = text[text.find(start) + len(start): find_nth(text , end , 2)]
    print("\t\033[94mreaches:\033[0m " + needle)
    return needle


def get_service_specificSupports(text):
    start = "Apoyos específicos que brinda: "
    end = " Tipo de apoyos: Individuales: ("
    needle = text[text.find(start) + len(start): text.find(end)]
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
        print("\t\033[94mtypeSupports:\033[0m -")
        return "-"


def get_service_daysToOperations(text):
    start = ") Disponibilidad: "
    end = "Otra información de interés (describa si son actividades, programas o proyectos u otros)"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mdaysToOperations:\033[0m " + needle)
    return needle
    #TODO generar json


def get_service_responsabilityPerson(text):
    start = "Información sobre la persona encargada y/o el equipo de trabajo que brinda el servicio de apoyo (refiérase a ocupación del personal responsable, formación académica, experiencia reconocida, destrezas adicionales y otros de interés):"
    end = "12. Cobertura del servicio de apoyo:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mresponsabilityPerson:\033[0m " + needle)
    return needle


def get_service_cover(text):
    start = "Cobertura del servicio de apoyo: Nacional: ("
    mid1 = ") Provincias (si no es cobertura nacional), describir las provincias: "
    mid2 = " Cantones (describir qué cantones cubre el servicio de apoyo): "
    end = " Se brinda de manera telef"
    needle1 = text[text.find(start) + len(start): text.find(mid1)]
    needle2 = text[text.find(mid1) + len(mid1): text.find(mid2)]
    needle3 = text[text.find(mid2) + len(mid2): text.find(end)]

    if needle1.replace(" " , "") == "x" or needle1.replace(" " , "") == "X":
        print("\t\033[94mcover:\033[0m Nacional")
        return "Nacional"

    if needle2 != "":
        if needle3 != "":
            print("\t\033[94mcover: Provincias: " + needle2 + " Cantones: " + needle3)
            return "Provincias: " + needle2 + " Cantones: " + needle3
        print("\t\033[94mcover:\033[0m " + needle2)
        return needle2

    if needle3 != "":
        print("\t\033[94mcover:\033[0m " + needle3)
        return needle3
    else:
        return "-"


def get_service_requirements(text):
    start = "Condiciones para acceder al servicio: Especifique los requisitos que se requieren para acceder al servicio. "
    end = " 14. Perfil de la persona usuaria:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94mrequirements:\033[0m " + needle)
    return needle


def get_service_accesibility(text):
    start = "17. Accesibilidad: Mencione si el servicio de atención reúne condiciones de accesibilidad según la normativa vigente. "
    end = "18. Observaciones:"
    needle = text[text.find(start) + len(start): text.find(end)]
    print("\t\033[94maccesibility:\033[0m " + needle)
    return needle


def get_service_others(text):
    start = "Observaciones: Indique aquí información que considere importante, detalle características del servicio que no queden reflejadas en los ítems anteriores."
    end = "Para uso interno"
    needle = text[text.find(start) + len(start): text.find(end)]
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
    get_service_daysToOperations(text)
    get_service_responsabilityPerson(text)
    get_service_cover(text)
    get_service_requirements(text)
    get_service_accesibility(text)
    get_service_others(text)
    get_service_scheduleExtraoerdinary(text)
    get_service_otherExtraordinaryAttention(text)
    get_service_attentionFrecuency(text)
    # items_idPk = fkId


def test_service(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_service_functions(get_text_from(fileMatrx[i][0]))
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
        test_product_functions(get_text_from(fileMatrx[i][0]))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_item_product_functions(text):
    # idPk += 1
    # code = 0
    get_item_name_product(text)
    get_item_description(text)
    get_item_observations(text)
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
    # organizationsIdFk = fkId


def est_item_product(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_item_product_functions(get_text_from(fileMatrx[i][0]))
        print("_____________________________________________________________________________________________________________________")
        print("")


def test_item_service_functions(text):
    # idPk += 1
    # code = 0
    get_item_name_service(text)
    get_item_description(text)
    get_item_observations(text)
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
    # organizationsIdFk = fkId


def test_item_service(fileMatrx):
    for i in range(len(fileMatrx)):
        print(str(i) + "\t|\t" + fileMatrx[i][0])
        test_item_service_functions(get_text_from(fileMatrx[i][0]))
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
    get_org_socialnetworks_product(text)
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
        test_org_product_functions(get_text_from(fileMatrx[i][0]))
        print("_____________________________________________________________________________________________________________________")
        print("")

# ------------------------------------BUILDING------------------------------------ #

#TODO hacer que esto sirva
def generate_Organizations_dictionary_product(productMatrix):
    Organizations = []
    printer = pprint.PrettyPrinter(indent=4 , width=500, depth=3)
    c = 1
    org_ready = []

    for row in productMatrix:
        temp = {}
        text = get_text_from(row[0])
        if get_org_name_product(text) not in org_ready:
            org_ready.append(get_org_name_product(text))
            temp["idPk"] = c
            temp["dni"] = "&No brinda información&"
            temp["name"] = "&" + get_org_name_product(text) + "&"
            temp["email"] = "&" + get_org_email_product(text) + "&"
            temp["web"] = "&" + get_org_web_product(text) + "&"
            temp["telephone"] = "&" + get_org_telephone_product(text) + "&"
            temp["legalRepresentative"] = "&No brinda información&"
            temp["assembly"] = []
            temp["socialNetworks"] = get_org_socialnetworks_product(text)
            temp["wazeAddress"] = get_org_wazeAddress_product(text)
            temp["schedule"] = "&n&"
            temp["reaches"] = "&" + get_org_reaches_product(text) + "&"
            temp["mision"] = "&" + get_org_mision_product(text) + "&"
            temp["vision"] = "&" + get_org_vision_product(text) + "&"
            temp["objetive"] = "&" + get_org_objective_product(text) + "&"
            temp["dayOperations"] = {}
            temp["isAproved"] = 1
            temp["isChecked"] = 1
            temp["isDeleted"] = 0
            temp["organizationsTypesidPk"] = get_org_typesidPk_product(text)
            c += 1

            Organizations.append(copy.deepcopy(temp))

    #print(Organizations)

    return Organizations


def dic2csv(dictionaries):
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
    file = open("toExport.csv", "w")
    file.write(old.replace("&", "\""))
    file.close()






# ------------------------------------MAIN------------------------------------ #

def main():
    print("          _____          __  __    _______     _______ _______ ______ __  __ \n    /\   |  __ \   /\   |  \/  |  / ____\ \   / / ____|__   __|  ____|  \/  |\n   /  \  | |  | | /  \  | \  / | | (___  \ \_/ / (___    | |  | |__  | \  / |\n  / /\ \ | |  | |/ /\ \ | |\/| |  \___ \  \   / \___ \   | |  |  __| | |\/| |\n / ____ \| |__| / ____ \| |  | |  ____) |  | |  ____) |  | |  | |____| |  | |\n/_/    \_\_____/_/    \_\_|  |_| |_____/   |_| |_____/   |_|  |______|_|  |_|\n                    -Automatic Database Migration System-                    \n\n\n")
    #serviceMatrx = get_files_from("/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Servicios de apoyo")
    productMatrix = get_files_from("/home/cipherlux/Dropbox/Inclutec/Migración/Informe Final CO - changed/Productos de apoyo")
    #path = "/home/fabian/Documents/repositories/catalog-migration/datosPorMigrar/Informe Final CO - changed/Productos de apoyo/San Jose/AZMONT/SALVAESCALERAS/Capri/AZMONT S.A - Prod. Salvaescalera Capri.docx"
    #text = get_text_from(path)


    #test_service(serviceMatrx)
    #test_product(productMatrix)
    #test_org_product(productMatrix)

    #get_org_typesidPk_product(text)
    list = generate_Organizations_dictionary_product(productMatrix)
    dic2csv(list)




if __name__ == "__main__":
    main()