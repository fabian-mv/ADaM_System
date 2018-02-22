import textract
import traceback
import re


# ------------------------------------STRING ANALYSIS------------------------------------ #

def analyze_pdf(path , verbose=False):
    print("\u001B[36mAnalyzing document...\u001B[0m" , end='' , flush=True)

    try:
        document_as_bytes = textract.process(path , encoding='utf-8')
        if verbose:
            print("\u001B[32;1mDone. Analysis result:\u001B[0m")
            print(str(document_as_bytes))
        else:
            print("\u001B[32;1mDone.\u001B[0m")
        return document_as_bytes
    except:
        print("\u001B[31;1mError.\u001B[0m")
        traceback.print_exc()


def encode_bytes(bytes , verbose=False):
    print("\u001B[36mEncoding bytes...\u001B[0m" , end='' , flush=True)

    document_as_string = bytes.decode('utf8')
    if verbose:
        print("\u001B[32;1mDone. Retrieved text from bytes:\u001B[0m")
        print(document_as_string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return document_as_string


def rectify_document_as_string(string, verbose=False):
    print("\u001B[36mRectifying string...\u001B[0m" , end='' , flush=True)

    string = string.replace("\t", " ")
    string = re.sub(' +', ' ', string)
    string = string.strip()
    if verbose:
        print("\u001B[32;1mDone. Rectified string:\u001B[0m")
        print(string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return string


# ------------------------------------TEXT ANALYSIS------------------------------------ #

def generate_superhaystack(text , verbose=False):
    print("\u001B[36mGenerating Superhaystack...\u001B[0m" , end='' , flush=True)

    print("\u001B[36mRemoving head and tail...\u001B[0m" , end='' , flush=True)
    head = text.find("Clasificación a dos niveles. Clases y subclases\n") + 49
    tail = text.find("Miembros de ISO 9999 en la familia OMS de clasificaciones internacionales")

    superhaystack = text[head:tail]

    print("\u001B[36mRemoving headers and footers...\u001B[0m", end='', flush=True)
    side = "LICENCIA PARA UN USUARIO. COPIA Y USO EN RED PROHIBIDAS\n\nDIRECCIÓN DE NORMALIZACIÓN DE INTECO AUTORIZA" \
           " ELUSO DE ESTA NORMA PARA LOS MIEMBROS DEL CTN 03/SC 02\n"
    header = "UNE-EN ISO 9999:2017"
    footer = "LICENCIA PARA UN USUARIO. COPIA Y USO EN RED PROHIBIDAS\n\nDIRECCIÓN DE NORMALIZACIÓN DE INTECO " \
             "AUTORIZA EL USO DE ESTA NORMA PARA LOS MIEMBROS DEL CTN 03/SC 02"

    superhaystack = superhaystack.replace(side , "")
    superhaystack = superhaystack.replace(header , "")
    superhaystack = superhaystack.replace(footer , "")

    print("\u001B[36mRemoving page numbers...\u001B[0m", end='', flush=True)
    superhaystack.replace("", "")
    superhaystack = re.sub('-\s\d{1,3}\s-' , "" , superhaystack)
    superhaystack = re.sub('\n+', "\n\n", superhaystack)


    if verbose:
        print("\u001B[32;1mDone. Generated superhsytack:\u001B[0m")
        print(superhaystack)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return superhaystack


def clean_string(string , verbose=False):
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = re.sub(' +', ' ', string)
    string = string.strip()

    if verbose:
        print("\u001B[32;1mDone. Generated clean string:\u001B[0m")
        print(string)
    return string


def get_next_subclass(haystack, verbose=False):
    match = re.search('\d{2}\s\d{2}\n+.+\n+\d{2}\s\d{2}', haystack)
    dirty_subclass = match.group(0)

    clean_sublass = re.sub('\n+\d{2}\s\d{2}\n*' , '' , dirty_subclass)

    if verbose:
        print("\u001B[32;1mDone. Retrieved next subclass:\u001B[0m")
        print(clean_sublass)
    return clean_sublass


def delete_next_subclass(haystack , subclass , verbose=False):
    index = haystack.find(subclass)
    if index != -1:
        haystack = haystack[index + len(subclass):]
        if verbose:
            print("\u001B[32;1mDone. Deleted subclass from haystack. Haystack is now:\u001B[0m")
            print(haystack)
        return haystack
    else:
        print("\u001B[31mError: couldn't find subclass.\u001B[0m")


def get_class_code_from_subclass(subclass , as_string=False , verbose=False):
    class_code = int(subclass[:2])

    if as_string:
        class_code = str(class_code)

    if verbose:
        print("\u001B[32;1mDone. Class code is:\u001B[0m")
        print(class_code)

    return class_code


def get_subclass_code_from_subclass(subclass , as_string=False , verbose=False):
    subclass_code = int(subclass[3:5])

    if as_string:
        subclass_code = str(subclass_code)

    if verbose:
        print("\u001B[32;1mDone. Subclass code is:\u001B[0m")
        print(subclass_code)

    return subclass_code





# ------------------------------------MAIN------------------------------------ #

def main():
    print("\n    _____  _____  ____  _                       _       _             \n   |_   _|/ ____|/ __ \| |                     | |     | |            \n     | | | (___ | |  | | |_ _ __ __ _ _ __  ___| | __ _| |_ ___  _ __ \n     | |  \___ \| |  | | __| '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|\n    _| |_ ____) | |__| | |_| | | (_| | | | \__ \ | (_| | || (_) | |   \n   |_____|_____/ \____/ \__|_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|   \n                  -ISO999:2016 PDF to JSON translator-                    \n\n\n")

    document_as_string = rectify_document_as_string(encode_bytes(analyze_pdf("/home/fabian/Documents/repositories/adam_system/adam4/UNE-EN_ISO_9999=2017.pdf")))
    superhaystack = generate_superhaystack(document_as_string)

    subclass = get_next_subclass(superhaystack , verbose=True)

    class_code = get_class_code_from_subclass(subclass , verbose=True)

    subclass_code = get_subclass_code_from_subclass(subclass,verbose=True)



if __name__ == "__main__":
    main()