import csv


dict = {'abstract': '… not refer specifically to oral- only versions of these languages, but rather is used to distinguish\nthem from visual–gestural sign languages. 1\xa0… uation processes involved in the generation of an\nanimated avatar for signing our\xa0… English–SL translation using a prototype EBMT system\xa0… \n', 'title': 'Data-driven machine translation for sign languages', 'eprint': 'https://scholar.google.comhttp://doras.dcu.ie/570/1/SaraMorrisseyPhDThesis.pdf', 'author': 'S Morrissey', 'url': 'http://doras.dcu.ie/570/'}

field_names = ["title" , "eprint" , "author" , "abstract" , "url"]

counter = 0
with open('RESULTADOS.csv' , 'w') as file:
    writer = csv.DictWriter(file , fieldnames=field_names)
    writer.writeheader()

    for row in rows:
        row = dict
        print(row)
        writer.writerow(row)

        if counter >= 10:
            break
        else:
            counter = counter + 1

print(newdict)