import itertools
import csv

countries = []
with open('countrycodes.csv', newline='', encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in  csvreader:
        countries.append(row[0].strip())
countries = [
    'GER',
    'GBR',
    'IDO',
    'IRE',
    'JPN',
    'USA'
]

print(countries)
print(len(countries))
#countries = [1, 2, 3, 4, 5]

pairs = list(itertools.combinations(countries, 2))
count = 0
for pair in pairs:
    count = count + 1
    #print(pair)

with open('country_pairs.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Country A', 'Countrry B']) # Write header
    for pair in pairs:
        csvwriter.writerow([pair[0], pair[1]])
        print(pair[0], pair[1])
print(count)

print('finished')
