archivo = open("/home/fabian/Desktop/ORGnames.csv", "r+")
contenido = archivo.read()
archivo.close()



names = []
line = ""
for char in contenido:
    if char != "\n":
        line = line + char
    else:
        names.append(line.replace("\"" , ""))
        line = ""



archivo = open("/home/fabian/Desktop/ORGnumbers.csv", "r+")
contenido = archivo.read()
archivo.close()




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
