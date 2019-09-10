import requests

def  distance(source, dest):
	url = 'https://www.distance24.org/route.json?stops=' + str(source) + '|' + str(dest)
	r = requests.get(url)

	dist = r.json()['distance']
	return dist

print( str(distance('Pune','Toronto')) + ' KM')

print(distance('Pune','Toronto')*9)

"""
rate = 9
print("Rate (per km) = Rs " + str(rate) + "/-")

source = input("Source: ")
dest = input("Destination: ")

url = "https://www.distance24.org/route.json?stops=" + str(source) + "|" + str(dest)

r = requests.get(url)
dist = r.json()["distance"]

print("-------------------------")
print( "Distance: " + str(dist) + " KM" )
cost = rate * dist
print("Cost: " + str(cost))
"""
