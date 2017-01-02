import os
import schedule
import time
import urllib

url = 'http://htadg.github.io/'
path_to_save = '/home/hiten/Desktop/tut/'
counter = 1

def down():
	global counter
	print "="*48, counter, "="*49
	data = urllib.URLopener()
	files = data.retrieve(url, os.path.join(path_to_save, 'data-'+str(counter)))
	print files
	print "="*100
	counter += 1

# schedule.every().day.at("20:54").do(down)
'''
while True:
	schedule.run_pending()
	time.sleep(1)
'''
down()
