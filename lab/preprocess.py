import clusters
data_range=range(2,8)
indexes=[]
raw_data=[]

def find_similar(country, available):
    similarities = []  # List of 3 tuples of (index, score) with highest score
    country_vector = [int(country[i]) for i in available]

    for i in range(len(raw_data)):
        if '' in raw_data[i]:  # Skip countries without a full set of data
            continue

        test_vector = [int(raw_data[i][j]) for j in available]
        similarities = sorted(similarities + [(clusters.pearson(country_vector, test_vector), i)])[:3]

    return [raw_data[i] for i in map(lambda x: x[1], similarities)]


# Fill in missing values for a country
def fill(country):
    available = list(data_range)
    country_missing = []

    for i in data_range:
        if country[i] == '':
            available.remove(i)
            country_missing.append(i)
    similar_countries = find_similar(country, available)
    # Fill in missing values with averages
    for index in country_missing:
        country[index] = str(round(sum(map(lambda x: int(x[index]), similar_countries))/3))

def main():
    data=open('dataset.csv')
    count=-1
    for line in data:
        if count==-1:
            count+=1
            continue
        arr = line.rstrip().split(',')
        if '' in arr:
            indexes.append(count)
        raw_data.append(arr)
        count+=1
    data.close()
    for index in indexes:
        fill(raw_data[index])
    
    output = open('processed_data.csv', "w")
    for line in raw_data:
        for i in range(len(line)):
            output.write(line[i] + ('\n' if i == (len(line) - 1) else ','))

    output.close()

if __name__ == "__main__":
    main()
