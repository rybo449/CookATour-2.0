import googlemaps
from factual import Factual
from datetime import datetime as dt
import sys
import datetime
import inspect
from factual.utils import circle
from dateutil import tz
import random
import os

factual = Factual('gfdD2lYBQ21Cs5M9eRpdEZCgDDswPvDzfeFOqYko','qkWK3Bv2wK7Jpz4e5JCSlKQVANbev8FHsCkoTSxZ')
gmaps = googlemaps.Client(key = 'AIzaSyDuSfwq0Nli3CzitI3SZob0t90dprS8JiQ')

places = factual.table('places')


def printresults_food(data,f):

	track = str(data[u'category_labels'][0][-1])
	name = str(data[u'name'])

	try:
		telephone = str(data[u'tel'])
	except:
		telephone = str("Not Available")	

	f.write("<p>This place is "+name+"</p>\n")

	f.write("<p>They serve "+track+"</p>\n")
	f.write("<p>Call them to make a reservation: "+telephone+"</p>\n")
	return


def printresults_places(data,f):


	track = str(data[u'category_labels'][0][-1])
	templat = float(data[u'latitude'])
	templng = float(data[u'longitude'])
	name = str(data[u'name'])

	try:
		telephone = str(data[u'tel'])
	except:
		telephone = str("Not Available")
	
	f.write("<p>This place is "+ name+"</p>\n")
	f.write("<p>Here's the telephone number: "+telephone+"</p>\n")
	return


def route(time, lat, lng, templat, templng, time_left,f, input2):

	f.write("<p>Here are the Directions</p>\n")

	directions_result = gmaps.directions(origin = (lat, lng),destination = (templat, templng), mode = "transit", departure_time = time)
	try:
		time_taken = int(directions_result[0][u'legs'][0][u'duration'][u'value'])
	except:
		f.write(directions_result)

	for i in directions_result[0][u'legs'][0][u'steps']: 

		f.write("<p>This leg of your journey will take "+str(int(int(i[u'duration'][u'value'])/float(60)))+" minutes</p>\n")
		try:
			if i[u'transit_details'][u'num_stops']:
				f.write("")				
			print "<p>",i[u'html_instructions'],"<p>"
			f.write("<p>There are "+i[u'transit_details'][u'num_stops']+" stops!</p>\n")
			f.write("<p>You will have to take the "+i[u'transit_details'][u'line'][u'short_name']+" line</p>\n")
		except:
			print
			f.write("<p>"+i[u'html_instructions']+"</p>\n")

	
	time_left -=time_taken/float(60*60)
	return time_left


def decideplace(time, track, lat, lng, start, now,f, input2):

	if time<0:
		return time, templat, templng, name

	data = places.filters({'$and':[{'category_ids':{'$includes':track}}]}).geo(circle(lat,lng, 1000*time)).limit(5).data()
	if not data:
		templat = lat
		templng = lng
		name = start
	else:
		data = data[random.randrange(0,len(data))]

		templat = float(data[u'latitude'])
		templng = float(data[u'longitude'])
		name = str(data[u'name'])
		f.write("<p>Go from "+start+" to "+name+" starting at time "+str(now+input2-datetime.timedelta(hours = time))+"</p>\n")
		time = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time, f, input2)
		time -= 1
		printresults_places(data,f)
		
	return time, templat, templng, name

def decidefood(time, lat, lng, start, now,f, input2):
	f.write("<p>Time for a Snack!</p>\n")

	if time<0:
		return time, templat, templng, name
	if time<1:
		data = places.filters({'$and':[{'category_ids':{'$includes':338}}, {'category_ids':{'$excludes':341}}]}).geo(circle(lat,lng,1000*time)).limit(5).data()
		time -= 0.25	
		data = data[random.randrange(0,len(data))]	
	else:
		data = places.filters({'$and':[{'category_ids':{'$includes':347}}]}).geo(circle(lat,lng,1000*time)).limit(5).data()
		time -= 1
	try:
		data = data[random.randrange(0,len(data))]

		templat = float(data[u'latitude'])
		templng = float(data[u'longitude'])
		name = str(data[u'name'])
		f.write("<p>Go from "+ start+" to "+ name+" starting at time " +str(now+input2-datetime.timedelta(hours = time))+"</p>\n")
		time = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time,f, input2)
		printresults_food(data,f)

		#print time
	except:
		templat = lat
		templng = lng
		name = start
	return time, templat, templng, name

def run_CookATour(input1, input2, input3):

	geocode = gmaps.geocode(input1)
	lat = geocode[0][u'geometry'][u'location'][u'lat']
	lng = geocode[0][u'geometry'][u'location'][u'lng']
	templat = lat
	templng = lng


	categories_places = [108, 109, 110, 111, 112, 118, 312, 334]
	names_of_tracks = ['Buildings and Structures', 'Gardens', 'Historic and Protected Sites', 'Monuments and Memorials', 'Natural', 'Parks', 'Pub Crawl', 'Clubbing']
	file_location = os.getcwd()
	f = open(file_location+'/templates/pages/results.html','w')
	f.write("{%  extends 'layouts/main.html' %}\n")
	f.write("{%  block title %}About{%  endblock %}\n")
	f.write("{%  block content %}\n")
	now = dt.now()
	time_left = int(input2)

	input2 = datetime.timedelta(hours = int(input2))
	start = input1
	count = 0
	f.write("<p>This is the "+names_of_tracks[int(input3)]+" track!</p>\n")
	while time_left > 0.5:
		if count%2 == 0:
			time_left, templat, templng, start = decideplace(time_left, categories_places[int(input3)], templat, templng, start, now,f, input2)
		else:
			time_left, templat, templng, start = decidefood(time_left, templat, templng, start, now,f, input2)
		count += 1

	route(now + input2 - datetime.timedelta(hours = time_left), templat, templng, lat, lng, time_left,f, input2)
	f.write("<p>Have fun on your trip! Choose Wisely :)</p>\n")
	f.write("{%  endblock %}\n")
