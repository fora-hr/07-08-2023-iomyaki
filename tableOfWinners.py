import json
from datetime import datetime
import pandas as pd
from IPython.display import display

# reading and saving files into variables
competitorsPath = 'competitors2.json'
with open(competitorsPath, 'r', encoding='utf-8-sig') as competitorsFile:
    competitors = json.load(competitorsFile)

resultsPath = 'results_RUN.txt'
with open(resultsPath, 'r', encoding='utf-8-sig') as resultsFile:
    results = resultsFile.read()

# sorting results by bib numbers and placing the finishing time ahead of the starting time
resultsOrderNumber = sorted(results.splitlines(), key=lambda line: (int(line.split(' ')[0]), line.split(' ')[1]))

# creating a list with bib numbers and resulting times
resultsTime = []

for i in range(0, len(resultsOrderNumber), 2):
    resultsTime.append(
        [
            resultsOrderNumber[i].split(' ')[0],
            datetime.strptime(resultsOrderNumber[i].split(' ')[2], '%H:%M:%S,%f') - datetime.strptime(
                resultsOrderNumber[i + 1].split(' ')[2], '%H:%M:%S,%f')
        ]
    )

# sorting results by the resulting time
resultsOrderTime = sorted(resultsTime, key=lambda result: result[1])

# creating and filling up a Pandas dataframe
df = pd.DataFrame(columns=['Занятое место', 'Нагрудный номер', 'Имя', 'Фамилия', 'Результат'])

place = 1
for result in resultsOrderTime:
    df = df._append(
        {
            'Занятое место': place,
            'Нагрудный номер': result[0],
            'Имя': competitors[result[0]]['Name'],
            'Фамилия': competitors[result[0]]['Surname'],
            'Результат': (datetime.strptime(str(result[1]), '%H:%M:%S.%f')).strftime('%M:%S,%f')[:-4]
        }, ignore_index=True
    )
    place += 1

# printing the resulting table
display(df.to_string(index=False))
