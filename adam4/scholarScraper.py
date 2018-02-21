import scholarly
import csv
import re


def process_row(row):
    dirty_text = row["abstract"]

    dirty_text = dirty_text.replace("… ", "")
    dirty_text = dirty_text.replace("\n", " ")
    dirty_text = dirty_text.replace("\t", " ")
    dirty_text = dirty_text.rstrip()
    dirty_text = dirty_text.lstrip()
    clean_text = re.sub(' +', ' ', dirty_text)

    row["abstract"] = clean_text

    return row


def build_super_dict():
    publications = scholarly.search_pubs_query("\"sign languages\" , avatar, translation")

    field_names = ["title", "eprint", "author", "abstract", "url"]

    counter = 0
    with open('RESULTADOS.csv', 'w') as file:
        csv.register_dialect("toMYSQL", delimiter=";", quoting=1, doublequote=1)
        writer = csv.DictWriter(file, fieldnames=field_names, dialect="toMYSQL")
        writer.writeheader()

        for publication in publications:
            row = publication.__getattribute__('bib')

            clean_row = process_row(row)

            print(clean_row)
            writer.writerow(clean_row)

            if counter >= 200:
                break
            else:
                counter = counter + 1


def main():
    build_super_dict()


if __name__ == "__main__":
    main()
