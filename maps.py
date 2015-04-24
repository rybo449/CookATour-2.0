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


def route(time, lat, lng, templat, templng, time_left,f, input2, hunger_count, input4):

	f.write("<p>Here are the Directions</p>\n")

	directions_result = gmaps.directions(origin = (lat, lng),destination = (templat, templng), mode = input4, departure_time = time)
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

	hunger_count += time_taken/float(60*60)
	time_left -=time_taken/float(60*60)
	return time_left, hunger_count


def decideplace(time, track, lat, lng, start, now,f, input2, places_been, hunger_count, input4):
	no_more = 0
	if time<0:
		return time, templat, templng, name, hunger_count, no_more


	data = places.filters({'$and':[{'category_ids':{'$includes':track}}]}).geo(circle(lat,lng, 1000*time)).data()
	count_datapoints = 0
	for datapoints in data:
		if datapoints[u'name'] not in places_been:
			break
		count_datapoints += 1
	if count_datapoints == len(data):
		no_more = 1
		return time, templat, templng, name, hunger_count, no_more
	if not data:
		templat = lat
		templng = lng
		name = start
	else:
		try:
			while True:
				temp_place = data[random.randrange(0,len(data))]
				if temp_place[u'name'] in places_been:
					continue
				else:
					places_been.setdefault(temp_place[u'name'], 0)
					break

			templat = float(temp_place[u'latitude'])
			templng = float(temp_place[u'longitude'])
			name = str(temp_place[u'name'])
			current_time = now+input2-datetime.timedelta(hours = time)
			current_time = current_time.strftime('%I:%M %p')
			f.write("<p>Go from "+ start+" to "+ name+" starting at time " +str(current_time)+"</p>\n")
			time, hunger_count = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time, f, input2, hunger_count, input4)
			time -= 1
			hunger_count += 1
			printresults_places(temp_place,f)
		except:
			templat = lat
			templng = lng
			name = start

	return time, templat, templng, name, hunger_count, no_more

def decidefood(time, lat, lng, start, now,f, input2, places_been, hunger_count, input4):

	if time<0:
		return time, templat, templng, name, hunger_count
	if time<1:
		data = places.filters({'$and':[{'category_ids':{'$includes':338}}, {'category_ids':{'$excludes':341}}]}).geo(circle(lat,lng,1000*time)).data()
		time -= 0.25	
	else:
		data = places.filters({'$and':[{'category_ids':{'$includes':347}}]}).geo(circle(lat,lng,1000*time)).data()
		time -= 1
	f.write("<p>Time for a Snack!</p>\n")

	try:
		while True:
			temp_place = data[random.randrange(0,len(data))]
			if temp_place[u'name'] in places_been:
				continue
			else:
				places_been.setdefault(temp_place[u'name'], 0)
				break


		templat = float(temp_place[u'latitude'])
		templng = float(temp_place[u'longitude'])
		name = str(temp_place[u'name'])
		current_time = now+input2-datetime.timedelta(hours = time)
		current_time = current_time.strftime('%I:%M %p')
		f.write("<p>Go from "+ start+" to "+ name+" starting at time " +str(current_time)+"</p>\n")
		time, hunger_count = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time,f, input2, hunger_count, input4)
		printresults_food(temp_place,f)

		#print time
	except:
		templat = lat
		templng = lng
		name = start
	return time, templat, templng, name, hunger_count

def run_CookATour(input1, input2, input3, input4):

	geocode = gmaps.geocode(input1)
	lat = geocode[0][u'geometry'][u'location'][u'lat']
	lng = geocode[0][u'geometry'][u'location'][u'lng']
	templat = lat
	templng = lng
	places_been = {}

	categories_places = [108, 109, 110, 111, 112, 118, 312, 334]
	names_of_tracks = ['Buildings and Structures', 'Gardens', 'Historic and Protected Sites', 'Monuments and Memorials', 'Natural', 'Parks', 'Pub Crawl', 'Clubbing']
	mode_of_transport = ["driving","walking","bicycling","transit"]
	file_location = os.getcwd()
	f = open(file_location+'/templates/pages/results.html','w')
	f.write("{%  extends 'layouts/main.html' %}\n")
	f.write("{%  block title %}Search Results{%  endblock %}\n")
	f.write("{%  block content %}\n")
	now = dt.now()
	time_left = int(input2)
	hunger_count = 0
	input2 = datetime.timedelta(hours = int(input2))
	start = input1
	count = 0
	no_more = 0
	less_food_tracks = ['Pub Crawl', 'Clubbing']
	more_food_tracks = ['Buildings and Structures', 'Historic and Protected Sites', 'Monuments and Memorials']
	average_food_tracks = ['Gardens', 'Natural', 'Parks']
	f.write("<p>This is the "+names_of_tracks[int(input3)]+" track!</p>\n")
	if names_of_tracks[int(input3)] in less_food_tracks:
		hunger_count -= 1
	elif names_of_tracks[int(input3)] in more_food_tracks:
		hunger_count += 1
	else:
		hunger_count += 0.5
	while time_left > 0.5:
		if hunger_count<4:
			time_left, templat, templng, start, hunger_count, no_more = decideplace(time_left, categories_places[int(input3)], templat, templng, start, now,f, input2, places_been, hunger_count, input4)
			if no_more:
				f.write("<p> Seems like there is only so much you can do here :)</p>")
				break
		else:
			hunger_count = 0
			time_left, templat, templng, start, hunger_count = decidefood(time_left, templat, templng, start, now,f, input2, places_been, hunger_count, input4)
		count += 1

	route(now + input2 - datetime.timedelta(hours = time_left), templat, templng, lat, lng, time_left,f, input2, hunger_count, input4)
	f.write("<p>Have fun on your trip! Choose Wisely :)</p>\n")
	f.write("{%  endblock %}\n")
