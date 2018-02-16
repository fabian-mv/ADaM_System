archivo = open("/home/fabian/Documents/repositories/adam_system/adam4/names.csv", "r+")
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



archivo = open("/home/fabian/Documents/repositories/adam_system/adam4/numbers.csv", "r+")
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
