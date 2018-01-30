archivo = open("/home/fabian/Desktop/namesOnly (copy).csv", "r+")
contenido = archivo.read()
archivo.close()
contenido


names = []
line = ""
for char in contenido:
    if char != "\n":
        line = line + char
    else:
        names.append(line.replace("\"" , ""))
        line = ""



archivo = open("/home/fabian/Desktop/namesOnly (another copy).csv", "r+")
contenido = archivo.read()
archivo.close()
contenido



numbers = []
line = ""
for char in contenido:
    if char != "\n":
        line = line + char
    else:
        numbers.append(line.replace("\"" , ""))
        line = ""





result = {}
for i in range(len(names)):
    result[numbers[i]] = names[i]

print(result)
