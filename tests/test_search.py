from searchtube import search
import datetime
q = input("enter q: ")

start = datetime.datetime.now()
x= search.search('UCXv-co3EYHF7aOH4A93qAHQ', q)

print(x)
print(len(x))
print(datetime.datetime.now() - start)