from factual import Factual
import datetime
import sys
import csv
import googlemaps
import os
from googleplaces import GooglePlaces, types, lang
from datetime import datetime as dt
from dateutil import tz
import random

google_places = GooglePlaces('AIzaSyDuSfwq0Nli3CzitI3SZob0t90dprS8JiQ')
factual = Factual('gfdD2lYBQ21Cs5M9eRpdEZCgDDswPvDzfeFOqYko','qkWK3Bv2wK7Jpz4e5JCSlKQVANbev8FHsCkoTSxZ')
places = factual.table('places')
gmaps = googlemaps.Client(key = 'AIzaSyDuSfwq0Nli3CzitI3SZob0t90dprS8JiQ')

def run_recurse(input1):
	file_location = os.getcwd()
	f = open(file_location+'/templates/pages/results_cluster.html','w')
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
	f.write("<p>"+str(input1)+"</p>")


	f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/static/magicslideshow/magicslideshow.css\"/>\n")
	f.write("<script src=\"/static/magicslideshow/magicslideshow.js\" type=\"text/javascript\"></script>\n")

	f.write("<p><b>Have fun on your trip! Choose Wisely :)</b></p>\n")
	f.write("{%  endblock %}\n")

	return

def run_BarCluster(input1):
	file_location = os.getcwd()
	f = open(file_location+'/templates/pages/results_cluster.html','w')
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
	geocode = gmaps.geocode(input1)
	lat = geocode[0][u'geometry'][u'location'][u'lat']
	lng = geocode[0][u'geometry'][u'location'][u'lng']
	f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/static/magicslideshow/magicslideshow.css\"/>\n")
	f.write("<script src=\"/static/magicslideshow/magicslideshow.js\" type=\"text/javascript\"></script>\n")
	data = []
	ids = {}
	#bar_categories = [312,313,314,315,316]
	d = factual.table("restaurants").filters({'$and':[{'category_ids':{'$includes':312}}]}).geo({"$circle":{"$center":[lat,lng], "$meters":2500}}).data()

	for i in d:
		factual_id = str(i[u'factual_id'])
		try:
			if i[u'alcohol_beer_wine']:
				alcohol_beer_wine = 1
			else:
				alcohol_beer_wine = 0
		except:
			alcohol_beer_wine = 0
		try:
			if i[u'groups_goodfor']:
				groups_goodfor = 1
			else:
				groups_goodfor = 0
		except:
			groups_goodfor = 0
		try:
			if i[u'alcohol']:
				alcohol = 1
			else:
				alcohol = 0
		except:
			alcohol = 1
		try:
			if i[u'alcohol_bar']:
				alcohol_bar = 1
			else:
				alcohol_bar = 0
		except:
			alcohol_bar = 0
		try:
			if i[u'seating_outdoor']:
				seating_outdoor = 1
			else:
				seating_outdoor = 0
		except:
			seating_outdoor = 0
		try:
			rating = float(i[u'rating'])/float(5)
		except:
			continue
		try:
			if i[u'parking']:
				parking = 1
			else:
				parking = 0
		except:
			parking = 0
		try:
			if i[u'meal_dinner']:
				meal_dinner = 1
			else:
				meal_dinner = 0
		except:
			meal_dinner = 0
		try:
			if i[u'payment_cashonly']:
				cashonly = 1
			else:
				cashonly = 0
		except:
			cashonly = 0
		lat = i[u'latitude']
		lng = i[u'longitude']
		try:
			if i[u'attire']:
				attire = 1
			else:
				attire = 0
		except:
			attire = 0
		try:
			if i[u'price']:
				price = int(i[u'price'])/float(5)
			else:
				price = 0.2
		except:
			price = 0.4
		try:
			if i[u'open_24hrs']:
				open_24hrs = 1
			else:
				open_24hrs = 0
		except:
			open_24hrs = 0
		try:
			if i[u'parking_street']:
				parking_street = 1
			else:
				parking_street = 0

		except:
			parking_street = 0
		try:
			if i[u'wifi']:
				wifi = 1
			else:
				wifi = 0
		except:
			wifi = 0
		try:
			name = i[u'name']
		except:
			continue
		try:
			if i[u'meal_deliver']:
				meal_deliver = 1
			else:
				meal_deliver = 0
		except:
			meal_deliver = 0
		if not ids.setdefault(factual_id, 0):
			ids[factual_id] = 1
		data.append([factual_id, name,lat,lng,rating,parking,meal_dinner,cashonly,attire,price,open_24hrs,parking_street,wifi,meal_deliver,alcohol_beer_wine,groups_goodfor,alcohol,alcohol_bar,seating_outdoor])
	
	#f.write(str(data))
	#data = pd.DataFrame(data)

	#features = data.iloc[0:,2:].dropna()
	#pc_toarray = features.values
	#hpc_fit,hpc_fit1 = train_test_split(pc_toarray, train_size = 0.01)
	#f.write("<p>factual_id,name,lat,lng,rating,parking,meal_dinner,cashonly,attire,price,open_24hrs,parking_street,wifi,meal_deliver")
	photo_counter = 1
	places_been = []
	irange = 0
	#f.write("<p>"+str(data)+"</p>\n")
	random_range = [x for x in xrange(len(data))]
	while irange <= min(3,len(data)):
		random_choice = random.choice(random_range)
		random_range.pop(random_range.index(random_choice))
		temp_place = data[random_choice][1]
		if temp_place in places_been:
			continue
		else:
			irange += 1
			places_been.append(temp_place)
			string = str(data[random_choice][2])+","+str(data[random_choice][3])
			query_result = google_places.nearby_search(name = data[random_choice][1],location=string,radius = 500)
			string = ""

			f.write("<div class=\"MagicSlideshow\" data-options=\"sselectors-style: bullets; selectors: bottom;width: 45%;height=45%;effect: fade\">\n")
			feature_vector = data[random_choice][1:]
			try:
				for photo in query_result.places[0].photos:
					f.write("<FORM method=\"post\" class=\"form\", ACTION=\"{{ url_for('recurse') }}\">\n")
					#f.write("<INPUT TYPE=IMAGE SRC")
					latlng = str("%.6f"%float(lat))+","+str("%.6f"%float(lng))
					try:
						photo.get(maxheight=500,maxwidth=500)
						photo.mimetype
						f.write("<INPUT TYPE=IMAGE SRC=\""+photo.url+"\" ALT=\""+str(photo_counter)+"\" BORDER=0 NAME=\""+str(photo_counter)+"\" title=\""+str(data[random_choice][1])+"\" data-caption=\"here is the caption\" value=\""+str(data[random_choice][1:])+"\">\n")
						#f.write("<a href=\"{{ url_for('recurse') }}\"><img src=\""+photo.url+"\"alt=\"CookATour Home\"title=\""+str(data[irange][1])+"\" border=\"0\"/></a>\n")
						#print photo.url
					except:
						continue
					f.write("</FORM>\n")

			except:
				f.write("<FORM method=\"post\" class=\"form\", ACTION=\"{{ url_for('recurse') }}\">\n")
				#notavailable_url = "/static/ico/notavailable.jpg"
				f.write("<INPUT TYPE=IMAGE SRC=\""+"/static/ico/notavailable.jpg"+"\" ALT=\""+str(photo_counter)+"\" BORDER=0 NAME=\""+str(photo_counter)+"\" title=\""+str(data[random_choice][1])+"\" value=\""+str(data[random_choice][1:])+"\">\n")
				f.write("</FORM>\n")
				#f.write("<a href=\"{{ url_for('recurse') }}\"><img src=\""+"/static/ico/notavailable.jpg"+"\"alt=\"CookATour Home\"title=\""+str(data[irange][1])+"\" border=\"0\"/></a>\n")
			f.write("</div>\n")		

			photo_counter += 1		
		#f.write("<p>"+str(data)+"</p>\n")

	#data.to_csv("sample.csv", index = False)
	#hpc = PCA(n_components = 2).fit_transform(hpc_fit)
	#k_means = KMeans()
	#k_means.fit(hpc)
	#f.write("<p>"+str(k_means)+"</p>\n")


	f.write("<p><b>Have fun on your trip! Choose Wisely :)</b></p>\n")
	f.write("{%  endblock %}\n")

