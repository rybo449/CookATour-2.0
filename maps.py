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


def printresults_food(data,f, counter):

	identifier = "places"+str(counter)

	f.write("<a href=\"javascript: void(0);\" onClick=\"toggle('"+identifier+"')\">Click for Name and Phone Number</a>\n")


	track = str(data[u'category_labels'][0][-1])
	name = str(data[u'name'])

	try:
		telephone = str(data[u'tel'])
	except:
		telephone = str("Not Available")	

	f.write("<p>This place is "+name+"</p>\n")

	#f.write("<p>They serve "+track+"</p>\n")
	#f.write("<p>Call them to make a reservation: "+telephone+"</p>\n")
	output_string = "<p>They serve "+track+"</p>\n" + "<p>Call them to make a reservation: "+telephone+"</p>\n"
	f.write("<div id=\""+identifier+"\" style=\"display:none;\">"+output_string+"</div>\n")
	counter+=1
	return counter


def printresults_places(data,f, counter):

	identifier = "places"+str(counter)

	f.write("<a href=\"javascript: void(0);\" onClick=\"toggle('"+identifier+"')\">Click for Name and Phone Number</a>\n")

	track = str(data[u'category_labels'][0][-1])
	templat = float(data[u'latitude'])
	templng = float(data[u'longitude'])
	name = str(data[u'name'])

	try:
		telephone = str(data[u'tel'])
	except:
		telephone = str("Not Available")
	
	#f.write("<p>This place is "+ name+"</p>\n")
	#f.write("<p>Here's the telephone number: "+telephone+"</p>\n")
	output_string = "<p>This place is "+ name+"</p>\n" + "<p>Here's the telephone number: "+telephone+"</p>\n"
	f.write("<div id=\""+identifier+"\" style=\"display:none;\">"+output_string+"</div>\n")
	counter+=1
	return counter


def route(time, lat, lng, templat, templng, time_left,f, input2, hunger_count, input4, counter):
	identifier = "places"+str(counter)

	f.write("<a href=\"javascript: void(0);\" onClick=\"toggle('"+identifier+"')\">Here are the Directions</a>\n")
	#f.write("<p>Here are the Directions</p>\n")
	output_string = ""
	directions_result = gmaps.directions(origin = (lat, lng),destination = (templat, templng), mode = input4, departure_time = time)
	try:
		time_taken = int(directions_result[0][u'legs'][0][u'duration'][u'value'])
	except:
		f.write(directions_result)

	f.write("<p><i>This leg of your journey will take "+str(int(time_taken/float(60)))+" minutes</i></p>\n")		
	for i in directions_result[0][u'legs'][0][u'steps']: 

		#f.write("<p>This leg of your journey will take "+str(int(int(i[u'duration'][u'value'])/float(60)))+" minutes</p>\n")
		try:
			if i[u'transit_details'][u'num_stops']:
				f.write("")				
			#print "<p>",i[u'html_instructions'],"<p>"
			#f.write("<p>There are "+i[u'transit_details'][u'num_stops']+" stops!</p>\n")
			#f.write("<p>You will have to take the "+i[u'transit_details'][u'line'][u'short_name']+" line</p>\n")

			#output_string += "<p>There are "+i[u'transit_details'][u'num_stops']+" stops!</p>\n"
			output_string += "<p>You will have to take the "+i[u'transit_details'][u'line'][u'short_name']
			if len(i[u'transit_details'][u'line'][u'short_name'])>1:
				output_string+= " bus</p>\n"
			else:
				output_string+=" subway line</p>\n"
			#f.write("This is a test!")

		except:
			#print
			#f.write("<p>"+i[u'html_instructions']+"</p>\n")
			output_string += "<p>"+i[u'html_instructions']+"</p>\n"

	f.write("<div id=\""+identifier+"\" style=\"display:none;\">"+output_string+"</div>\n")
	hunger_count += time_taken/float(60*60)
	time_left -=time_taken/float(60*60)
	counter+=1
	return time_left, hunger_count, counter


def decideplace(time, track, lat, lng, start, now,f, input2, places_been, hunger_count, input4, counter):
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
			f.write("<p><br><br><b>Go from "+ start+" to "+ name+" starting at time " +str(current_time)+"</b></p>\n")
			time, hunger_count, counter = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time, f, input2, hunger_count, input4, counter)
			time -= 1
			hunger_count += 1
			counter = printresults_places(temp_place,f, counter)
		except:
			templat = lat
			templng = lng
			name = start

	return time, templat, templng, name, hunger_count, no_more, counter

def decidefood(time, lat, lng, start, now,f, input2, places_been, hunger_count, input4, counter):

	if time<0:
		return time, templat, templng, name, hunger_count
	if time<1:
		data = places.filters({'$and':[{'category_ids':{'$includes':338}}, {'category_ids':{'$excludes':341}}]}).geo(circle(lat,lng,1000*time)).data()
		time -= 0.25	
	else:
		data = places.filters({'$and':[{'category_ids':{'$includes':347}}]}).geo(circle(lat,lng,1000*time)).data()
		time -= 1
	f.write("<p><br><br><b>Time for a Snack!</b></p>\n")

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
		f.write("<p><br><br><b>Go from "+ start+" to "+ name+" starting at time " +str(current_time)+"</b></p>\n")
		time, hunger_count, counter = route(now + input2 - datetime.timedelta(hours = time), lat, lng, templat, templng, time,f, input2, hunger_count, input4, counter)
		counter = printresults_food(temp_place,f, counter)

		#print time
	except:
		templat = lat
		templng = lng
		name = start
	return time, templat, templng, name, hunger_count, counter

def run_CookATour(input1, input2, input3, input4):




	geocode = gmaps.geocode(input1)
	lat = geocode[0][u'geometry'][u'location'][u'lat']
	lng = geocode[0][u'geometry'][u'location'][u'lng']
	templat = lat
	templng = lng
	places_been = {}

	categories_places = [108, 142, 110, 111, 118, 312, 334]
	names_of_tracks = ['Buildings and Structures', 'Shopping', 'Historic and Protected Sites', 'Monuments and Memorials', 'Parks', 'Pub Crawl', 'Clubbing']
	mode_of_transport = ["driving","walking","bicycling","transit"]
	file_location = os.getcwd()
	f = open(file_location+'/templates/pages/results.html','w')
	f.write("{%  extends 'layouts/main.html' %}\n")
	f.write("{%  block title %}Search Results{%  endblock %}\n")
	f.write("{%  block content %}\n")

	##Start the initial javascript to hide the driving instructions
	f.write("<script type=\"text/javascript\">\n")
	f.write("function toggle(obj) {\n")
	f.write("var obj=document.getElementById(obj);\n")
	f.write("if (obj.style.display == \"block\") obj.style.display = \"none\";\n")
	f.write("else obj.style.display = \"block\";\n")
	f.write("}\n")
	f.write("</script>\n")



	now = dt.now(tz.tzlocal())
	time_left = int(input2)
	hunger_count = 0
	input2 = datetime.timedelta(hours = int(input2))
	start = input1
	counter = 0
	no_more = 0
	less_food_tracks = ['Pub Crawl', 'Clubbing']
	more_food_tracks = ['Buildings and Structures', 'Historic and Protected Sites', 'Monuments and Memorials']
	average_food_tracks = ['Shopping', 'Parks']
	f.write("<h1>This is the "+names_of_tracks[int(input3)]+" track!</h1>\n")
	if names_of_tracks[int(input3)] in less_food_tracks:
		hunger_count -= 1
	elif names_of_tracks[int(input3)] in more_food_tracks:
		hunger_count += 1
	else:
		hunger_count += 0.5
	while time_left > 0.5:
		if hunger_count<4:
			time_left, templat, templng, start, hunger_count, no_more, counter = decideplace(time_left, categories_places[int(input3)], templat, templng, start, now,f, input2, places_been, hunger_count, input4, counter)
			if no_more:
				f.write("<p><b> Seems like there is only so much you can do here :)</b></p>")
				break
		else:
			hunger_count = 0
			time_left, templat, templng, start, hunger_count, counter = decidefood(time_left, templat, templng, start, now,f, input2, places_been, hunger_count, input4, counter)
		counter += 1

	f.write("<p><br><br><b>Time to head back!</b></p>")
	route(now + input2 - datetime.timedelta(hours = time_left), templat, templng, lat, lng, time_left,f, input2, hunger_count, input4, counter)
	f.write("<p><b>Have fun on your trip! Choose Wisely :)</b></p>\n")
	f.write("{%  endblock %}\n")
