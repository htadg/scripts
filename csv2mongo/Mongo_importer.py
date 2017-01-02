# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import csv
import getopt
import json
import os
import re
import sys

from pymongo import MongoClient


path = 'Product_files/'
for csvfilename in os.listdir(path):
    if not csvfilename.endswith('.csv'):
        continue
    print "Current CSV: " + csvfilename

    ls = ''
    with open('{}/{}'.format(path, csvfilename), 'r') as f:
        ls += f.read()
    s1 = re.compile('(?P<num>[0-9]|[\w]|\(|\.) {0,}(\"{1,})(?P<later>[\w]|\)|\.|\-|\●|\  {0,})', re.IGNORECASE)
    s2 = re.compile('(\"{2,})[^,\n]', re.IGNORECASE)
    s3 = re.compile('[^,\n](\"{2,})', re.IGNORECASE)

    ls = re.sub(s1, '\g<num>\g<later>', ls)
    ls = re.sub(s2, '"', ls)
    ls = re.sub(s3, '"', ls)

    with open('{}/{}'.format(path, csvfilename), 'w') as f:
        f.write(ls)

    with open("Product_files/{}".format(csvfilename), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames

        host = "127.0.0.1"
        port = 27017
        mongo_client = MongoClient("mongodb://{}:{}".format(host, port))

        db = mongo_client.ndukan
        db[csvfilename.split('.')[0]].drop()

        z = "original,200,400,800".split(",")
        for each in reader:
            row = {}
            for field in header:
                if field == "imageUrlStr":
                    ls = each[field].split(";")
                    a = b = c = d = " "
                    for i in ls:
                        if z[0] in i:
                            a = i
                        elif z[1] in i:
                            b = i
                        elif z[2] in i:
                            c = i
                        elif z[3] in i:
                            d = i
                    row["imageoriginal"] = a
                    row["image200"] = b
                    row["image400"] = c
                    row["image800"] = d
                elif "Brand" in field:
                    row['brand'] = each[field] if each[field] != "" else " "
                else:
                    row[field] = each[field] if each[field] != "" else " "
            db[csvfilename.split('.')[0]].insert_one(row)
