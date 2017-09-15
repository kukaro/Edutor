import csv


def readCSV(filename):
    f = open('data.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    for line in reader:
        print(line)
    f.close()
