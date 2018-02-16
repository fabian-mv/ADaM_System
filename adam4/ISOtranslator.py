import textract
import traceback
import re


# ------------------------------------STRING ANALYSIS------------------------------------ #

def analyze_pdf(path , verbose=True):
    print("\u001B[36mAnalyzing document...\u001B[0m" , end='' , flush=True)

    try:
        document_as_bytes = textract.process(path , encoding='utf-8')
        if verbose:
            print("\u001B[32;1m\tDone. Analysis result:\u001B[0m")
            print("\t" + str(document_as_bytes))
        else:
            print("\u001B[32;1mDone.\u001B[0m")
        return document_as_bytes
    except:
        print("\u001B[31;1m\tError.\u001B[0m")
        traceback.print_exc()


def encode_bytes(bytes , verbose=True):
    print("\u001B[36mEncoding bytes...\u001B[0m" , end='' , flush=True)

    document_as_string = bytes.decode('utf8')
    if verbose:
        print("\u001B[32;1m\tDone. Retrieved text from bytes:\u001B[0m " + document_as_string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return document_as_string


def rectify_string(string , verbose=True):
    print("\u001B[36mRectifying string...\u001B[0m" , end='' , flush=True)

    # string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = re.sub(' +', ' ', string)
    string = string.strip()
    if verbose:
        print("\u001B[32;1m\tDone. Rectified string:\u001B[0m " + string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return string


# ------------------------------------TEXT ANALYSIS------------------------------------ #

def generate_superhaystack(text , verbose=True):
    print("\u001B[36mGenerating Superhaystack...\u001B[0m" , end='' , flush=True)

    print("\u001B[36mRemoving head and tail...\u001B[0m" , end='' , flush=True)
    head = text.find("6 Clasificación\n6.1\n\nClasificación a un nivel. Clases\n") + 55
    tail = text.find("Miembros de ISO 9999 en la familia OMS de clasificaciones internacionales")

    superhaystack = text[head:tail]


    print("\u001B[36mRemoving headers and footers...\u001B[0m", end='', flush=True)
    side = "LICENCIA PARA UN USUARIO. COPIA Y USO EN RED PROHIBIDAS\n\nDIRECCIÓN DE NORMALIZACIÓN DE INTECO AUTORIZA EL USO DE ESTA NORMA PARA LOS MIEMBROS DEL CTN 03/SC 02\n"
    header = "UNE-EN ISO 9999:2017"
    footer = ""

    superhaystack = superhaystack.replace(side , "")
    superhaystack = superhaystack.replace(header , "")


    if verbose:
        print("\u001B[32;1m\tDone. Generated superhsytack:\u001B[0m")
        print(superhaystack)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return superhaystack



# ------------------------------------MAIN------------------------------------ #

def main():
    print("\n    _____  _____  ____  _                       _       _             \n   |_   _|/ ____|/ __ \| |                     | |     | |            \n     | | | (___ | |  | | |_ _ __ __ _ _ __  ___| | __ _| |_ ___  _ __ \n     | |  \___ \| |  | | __| '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|\n    _| |_ ____) | |__| | |_| | | (_| | | | \__ \ | (_| | || (_) | |   \n   |_____|_____/ \____/ \__|_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|   \n                  -ISO999:2016 PDF to JSON translator-                    \n\n\n")

    document_as_string = rectify_string( encode_bytes( analyze_pdf("/home/fabian/Documents/repositories/adam_system/adam4/UNE-EN_ISO_9999=2017.pdf" , False) , False) , False)
    generate_superhaystack(document_as_string , False)












if __name__ == "__main__":
    main()