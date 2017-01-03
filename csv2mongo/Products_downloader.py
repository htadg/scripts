#!/usr/bin/env python

import os
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

os.system('rm List.json')
os.system('rm -rf Product_files')
os.system('mkdir Product_files')

# curl -H "Fk-Affiliate-Id:<Affiliate Tracking ID>" -H
# "Fk-Affiliate-Token:<Affiliate API Token>" "<API URL>"

affidID = "9dukan"
affidToken = "90b88b653bab42669db90c175632b060"
Header_affidID = "Fk-Affiliate-Id:{affidID}".format(affidID=affidID)
Header_affidToken = "Fk-Affiliate-Token:{affidToken}".format(
    affidToken=affidToken)

listing_url = "https://affiliate-api.flipkart.net/affiliate/download/feeds/{affidID}.json".format(
    affidID=affidID)

request_url = 'curl -H "{}" -H "{}" "{}" > List.json'.format(
    Header_affidID, Header_affidToken, listing_url)

os.system(request_url)
# Product Listing downloaded and saved to List.json



# pprint(data)
print

taskNumber = 1

ProductList = data["apiGroups"]["affiliate"]["apiListings"]

for List in ProductList:
    itemName = ProductList[List]["apiName"]
    itemGet = ProductList[List]["availableVariants"]["v1.1.0"]["get"]
    totalNumber = len(ProductList)
    oldFilename = itemGet[64:].split('?')[0]

    print bcolors.OKBLUE + "Task:" + "{taskNumber}/{totalNumber}".format(taskNumber=taskNumber, totalNumber=totalNumber),
    print "| Current Product: " + itemName + bcolors.ENDC

    request_url2 = 'curl -H "{Header_affidID}" -H "{Header_affidToken}" "{itemGet}" > Product_files/{itemName}.zip'.format(
        Header_affidID=Header_affidID, Header_affidToken=Header_affidToken, itemGet=itemGet, itemName=itemName
    )


    # curl -H "Fk-Affiliate-Id:<your_affiliate_id>" -H
    # "Fk-Affiliate-Token:<your_affiliate_token>"
    # https://affiliate-api.flipkart.net/feeds/1.0/rawfiles/7jv?expiresAt=1468256319525&sig=0aa990da4e427b6405693683d96873d8
    # >  <output_file_name>.zip

    print "Downloading " + itemName + ".zip"
    os.system(request_url2)

    print "Extracting " + itemName + ".zip"

    os.system(
        'unzip Product_files/{itemName}.zip -d Product_files'.format(itemName=itemName))

    os.system('rm Product_files/{itemName}.zip'.format(itemName=itemName))

    os.rename('Product_files/{oldFilename}.csv'.format(oldFilename=oldFilename),'Product_files/{itemName}.csv'.format(itemName=itemName))

    # os.system('mv Product_files/{oldFilename} Product_files/{itemName}.csv'.format(oldFilename=oldFilename, itemName=itemName))
    # os.system("rename 's/oldname/newname' Product_files/{oldFilename} Product_files/{itemName}.csv".format(oldFilename=oldFilename, itemName=itemName))

    print bcolors.OKGREEN + "Created: " + itemName + ".csv" + bcolors.ENDC

    taskNumber = taskNumber + 1
    print
