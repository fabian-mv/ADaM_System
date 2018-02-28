import scholarly
import csv
from tkinter import *
from tkinter import ttk
import urllib


def process_row(row):
        if 'abstract' in row:
            dirty_text = row["abstract"]

            dirty_text = dirty_text.replace("… ", "")
            dirty_text = dirty_text.replace("\n", " ")
            dirty_text = dirty_text.replace("\t", " ")
            dirty_text = dirty_text.rstrip()
            dirty_text = dirty_text.lstrip()
            clean_text = re.sub(' +', ' ', dirty_text)

            row["abstract"] = clean_text

        if 'eprint' in row:
            dirty_link = row['eprint']
            clean_link = dirty_link.replace("https://scholar.google.com" , "")

            row['eprint'] = clean_link

        return row


def build_super_dict(query , path , amount):
    amount = int(amount)
    publications = scholarly.search_pubs_query("darwin")

    field_names = ["title", "eprint", "author", "abstract", "url"]

    counter = 0
    with open('/home/fabian/Documents/repos/scholar_web_scrapper/results/scrapping_results.csv', 'w') as file:
        csv.register_dialect("toMYSQL", delimiter=";", quoting=1, doublequote=1)
        writer = csv.DictWriter(file, fieldnames=field_names, dialect="toMYSQL")
        writer.writeheader()

        for publication in publications:
            row = publication.__getattribute__('bib')

            clean_row = process_row(row)

            print(clean_row)
            if clean_row is not None:
                writer.writerow(clean_row)

            if counter >= 15:
                break
            else:
                counter = counter + 1


def search():
    path = "/home/fabian/Documents/repos/scholar_web_scrapper/results/"#str(entry_path.get())
    query = "darwin"#str(entry_query.get())
    amount = 10#int(entry_amount.get())

    build_super_dict(query , path , amount)



build_super_dict("" , "" , 10)
# root = Tk()
# root.title("Google Scholar Web Scrapper")
#
# entry_query = ttk.Entry(root, width=50)
# entry_query.insert(END, 'darwin')
# entry_query.grid(column=0, row=1, columnspan=4, padx=7, pady=(0,7))
#
# entry_path = ttk.Entry(root, width=30)
# entry_path.insert(END, '/home/fabian/Documents/repos/scholar_web_scrapper/results')
# entry_path.grid(column=0, row=3, columnspan=3, padx=7, pady=3 , sticky=W)
#
# entry_amount = ttk.Entry(root, width=10)
# entry_amount.insert(END, '10')
# entry_amount.grid(column=3, row=3, padx=7, sticky=W)
#
# label_search = ttk.Label(root, text="Search:").grid(column=0, row=0, sticky=(W), padx=7)
# label_path = ttk.Label(root, text="Directory to save results:").grid(column=0, row=2, sticky=(W), padx=7)
# label_amount = ttk.Label(root, text="Amount of results:").grid(column=3, row=2, sticky=(W), padx=7)
#
# button_search = ttk.Button(root, text="Search", command=search).grid(column=3, row=4, sticky=E+W+N+S, padx=7, pady=(3,10))
#
# entry_query.focus()
#
# root.mainloop()



