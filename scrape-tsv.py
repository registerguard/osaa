import requests, lxml, csv
from bs4 import BeautifulSoup

schools = [("Sheldon",15211),("South Eugene",15255),("Thurston",15371),("Willamette",15488),("Churchill",14384),("Marist",14844),("North Eugene",14967),("Springfield",15296),("Cottage Grove",14441),("Elmira",14556),("Juction City",14739),("Marshfield",14850),("North Bend",14953),("Siuslaw",15244),("Sutherlin",15347),("Sweet Home",15353),("Bandon",14258),("Creswell",14468),("Harrisburg",14650),("Pleasant Hill",15077),("Central Linn",14366),("Monroe",14909),("North Douglas",14962),("Oakland",15009),("Oakridge",15013),("Reedsport",15121),("Waldport",15439),("Alsea",14229),("Crow",14483),("Elkton",14551),("Lowell",14824),("Mapleton",14839),("McKenzie",14867),("Mohawk",14899),("Triangle Lake",15396),("Yoncalla",15525)]

for school, id in schools:
	url = 'http://www.osaa.org/teams/{0}?year=2016'.format(id)
	#print url
	
	r = requests.get(url)
	#r.text
	
	data = []
	
	soup = BeautifulSoup(r.text, 'lxml')
	sked = soup.find(id="sub-tabs-schedule")
	for i, tr in enumerate(sked.find_all('tr')):
		if i > 0:
			data.append([])
		#print tr
		for j, td in enumerate(tr.find_all('td')):
			if j < 6:
				#print td.descendants
				strings = td.get_text()
				#strings = td.string
				if strings is not None:
					data[-1].append(strings)
				#print td.string
	
#	print data
	
	tsvname = 'tsv/{0}.tsv'.format(school.lower().replace(' ', '-'))
	
	file = open(tsvname, 'wb')
	wr = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter='\t')
	for i in data:
		wr.writerow(i)
