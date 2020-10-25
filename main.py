import pandas as pd
import math

#для большего понимания использовал эту статью
#https://habr.com/ru/post/150399/



def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list


k = 4
user = 29
data = pd.read_csv("data.csv")
daycontext = pd.read_csv("context_day.csv")
placecontext = pd.read_csv("context_place.csv")
weekend = [' Sat', ' Sun']
place = [' h']

#подготовка словаря для получения коэф. схожести
forSimData = data[data['Unnamed: 0'] != 'User 30'].T

del data['Unnamed: 0']
chosenUser = data.iloc[user]
simDict = dict()
for i in forSimData:
    simDict[i] = 0

#подсчет коэф. сходства
for i in simDict.keys():
    sumuv = 0
    sumu2 = 0
    sumv2 = 0
    movie = 0
    for item in data.iloc[i]:
        if(chosenUser[movie] != -1 and item != -1):
            sumuv += chosenUser[movie]*item
            sumu2 += chosenUser[movie]**2
            sumv2 += item**2
            simDict[i] = sumuv / (math.sqrt(sumu2) * math.sqrt(sumv2))
        movie+=1


#результат 1
result1 = dict(sorted(simDict.items(), key = lambda kv:kv[1], reverse = True) [:k])
print(result1)


toMeanCounter = 0
cnt = 0
meanCurrentUser = 0
meanDict = dict()
#подсчет средней оценки текущего пользователя
for i in chosenUser:
    if i>=0:
        toMeanCounter+=i
        cnt+=1

meanCurrentUser = toMeanCounter/cnt
#подсчет средних оценок похожих пользователей
for i in result1:
    toMeanCounter = 0
    cnt = 0
    for j in data.iloc[i]:
        if j >= 0:
            toMeanCounter += j
            cnt += 1
    meanDict[i] = toMeanCounter/cnt


shouldRate = list()
#фильмы, которые пользователь не оценил
counter = 0
for i in chosenUser:
    if i == -1:
        shouldRate.append(counter)
    counter += 1

result1Task = dict()
for film in shouldRate:
    sumup = 0
    sumdown = 0
    for i in meanDict:
        if(data.iloc[i][film] != -1):
            sumup += simDict[i]*(data.iloc[i][film]-meanDict[i])
            sumdown += simDict[i]

    result1Task[film+1] = round(meanCurrentUser + sumup/sumdown, 3)
print(result1Task)



recommendedDict = dict()
lastCoutner = 0
for i in shouldRate:
    if placecontext.iloc[user][i] == place[0]:
        if daycontext.iloc[user][i] in weekend:
            recommendedDict[i+1] = result1Task[i+1]
            counter+=1

result2 = dict(sorted(recommendedDict.items(), key = lambda kv:kv[1]))
lastResult = dict()
if result2:
    keys = getList(result2)
    print(keys[0])





result = {
    'User': user + 1,
    '1': result1Task,
    '2': result2
}
print(result)
import json
with open('result.json', 'w') as fp:
    json.dump(result, fp)
