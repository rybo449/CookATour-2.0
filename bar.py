from factual import Factual
import datetime
import sys
import csv
import googlemaps
import os
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split

factual = Factual('gfdD2lYBQ21Cs5M9eRpdEZCgDDswPvDzfeFOqYko','qkWK3Bv2wK7Jpz4e5JCSlKQVANbev8FHsCkoTSxZ')
places = factual.table('places')
gmaps = googlemaps.Client(key = 'AIzaSyDuSfwq0Nli3CzitI3SZob0t90dprS8JiQ')

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

	data = []
	ids = {}
	#bar_categories = [312,313,314,315,316]
	for j in xrange(5):
		d = factual.table("restaurants").filters({'$and':[{'category_ids':{'$includes':312}}]}).geo({"$circle":{"$center":[lat,lng], "$meters":2500}}).data()

		for i in d:
			factual_id = str(i[u'factual_id'])
			try:
				rating = str(i[u'rating'])
			except:
				continue
			try:
				if i[u'parking']:
					parking = str(1)
				else:
					parking = str(0)
			except:
				parking = str(0)
			try:
				if i[u'meal_dinner']:
					meal_dinner = str(1)
				else:
					meal_dinner = str(0)
			except:
				meal_dinner = str(0)
			try:
				if i[u'payment_cashonly']:
					cashonly = str(1)
				else:
					cashonly = str(0)
			except:
				cashonly = str(0)
			lat = str(i[u'latitude'])
			lng = str(i[u'longitude'])
			try:
				if i[u'attire']:
					attire = str(1)
				else:
					attire = str(0)
			except:
				attire = str(0)
			try:
				if i[u'price']:
					price = str(1)
				else:
					price = str(0)
			except:
				price = str('-1')
			try:
				if i[u'open_24hrs']:
					open_24hrs = str(1)
				else:
					open_24hrs = str(0)
			except:
				open_24hrs = str(0)
			try:
				if i[u'parking_street']:
					parking_street = str(1)
				else:
					parking_street = str(0)

			except:
				parking_street = str(0)
			try:
				if i[u'wifi']:
					wifi = str(1)
				else:
					wifi = str(0)
			except:
				wifi = str(0)
			try:
				name = str(i[u'name'])
			except:
				continue
			try:
				if i[u'meal_deliver']:
					meal_deliver = str(1)
				else:
					meal_deliver = str(0)
			except:
				meal_deliver = str(0)
			if not ids.setdefault(factual_id, 0):
				ids[factual_id] = 1
				data.append([factual_id, name,lat,lng,rating,parking,meal_dinner,cashonly,attire,price,open_24hrs,parking_street,wifi,meal_deliver])
	

	data = pd.DataFrame(data)

	#features = data.iloc[0:,2:].dropna()
	#pc_toarray = features.values
	#hpc_fit,hpc_fit1 = train_test_split(pc_toarray, train_size = 0.01)
	f.write("<p>factual_id,name,lat,lng,rating,parking,meal_dinner,cashonly,attire,price,open_24hrs,parking_street,wifi,meal_deliver")
	#for row in data:
	#	row_string = ""
	#	for row1 in row:
	#		row_string += 
	data.to_csv("sample.csv", index = False)
	#hpc = PCA(n_components = 2).fit_transform(hpc_fit)
	#k_means = KMeans()
	#k_means.fit(hpc)
	#f.write("<p>"+str(k_means)+"</p>\n")


	f.write("<p><b>Have fun on your trip! Choose Wisely :)</b></p>\n")
	f.write("{%  endblock %}\n")

