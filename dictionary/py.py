import csv
from bs4 import BeautifulSoup

with open("output.csv", newline='', encoding="utf-8") as infile, \
     open("cleaned.csv", "w", newline='', encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        word = row[0].strip()
        raw_html = row[1]
        soup = BeautifulSoup(raw_html, "html.parser")

        # Remove the header div (usually repeats the word)
        header = soup.find("div", class_="k")
        if header:
            header.decompose()

        # Get the remaining text (definition only)
        clean_def = soup.get_text(separator=" ", strip=True)

        writer.writerow([word, clean_def])
