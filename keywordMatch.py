import json
import csv
import sys

# coding=utf-8
json_data = open(sys.argv[1]).read()

#data = json.loads(json_data)
#print(data)

data = json.JSONDecoder().decode(json_data)


counter = 0
dCounter = 0
rCounter = 0

found = False
dFound = False
rFound = False

csvfile = open("Keywords.csv", "rU")

for line in data:
  try:
    found = False
    dFound = False
    rFound = False
    headline = line['headline']
    csvfile = open("Keywords.csv", "rU")
    thisreader = csv.reader(csvfile, delimiter=",", quotechar="|")
    for row in thisreader:
      f = row[0]
      s = row[1] 
      if (f in headline) or (s in headline):
        found = True
        if row[3] in "R":
          rFound = True
        if row[3] in "D":
          dFound = True
    if found:
      print headline 
      counter = counter + 1
    if rFound:
      rCounter = rCounter + 1
    if dFound:
      dCounter = dCounter + 1
  except KeyError:
    {}
print "Total: ", counter
print "D: ", dCounter
print "R: ", rCounter



