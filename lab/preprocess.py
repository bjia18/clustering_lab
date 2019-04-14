data=open('dataset.csv')
title=True
countries=[]
averages=[0,0,0,0,0,0,0]
for i in data:
    if title:
        title=False
        continue
    i=i.strip('\n')
    j=i.split(',')
    for m in range(2,9):#add up values
        if j[m]:
            j[m]=int(j[m])
            averages[m-2]+=j[m]
    countries.append(j)

for i in range(7):#fill in the blanks with average
    averages[i]=round(averages[i]/len(countries))
for i in countries:
    for m in range(2,9):
        if i[m]=='':
            i[m]=averages[m-2]
    print(i)
output = open('processed_data.csv', "w")

for l in countries:#write output
    for i in range(len(l)):
        output.write(str(l[i]) + ('\n' if i == (len(l) - 1) else ','))

output.close()