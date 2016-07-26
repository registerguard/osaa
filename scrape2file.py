import requests, lxml, csv
from bs4 import BeautifulSoup

# List of schools and ids
schools = [("Sheldon",15211),("South Eugene",15255),("Thurston",15371),("Willamette",15488),("Churchill",14384),("Marist",14844),("North Eugene",14967),("Springfield",15296),("Cottage Grove",14441),("Elmira",14556),("Juction City",14739),("Marshfield",14850),("North Bend",14953),("Siuslaw",15244),("Sutherlin",15347),("Sweet Home",15353),("Bandon",14258),("Creswell",14468),("Harrisburg",14650),("Pleasant Hill",15077),("Central Linn",14366),("Monroe",14909),("North Douglas",14962),("Oakland",15009),("Oakridge",15013),("Reedsport",15121),("Waldport",15439),("Alsea",14229),("Crow",14483),("Elkton",14551),("Lowell",14824),("Mapleton",14839),("McKenzie",14867),("Mohawk",14899),("Triangle Lake",15396),("Yoncalla",15525)]

# Recursive method to figure out if we want csv or tsv and if the input is good
def selectDelimiter(delimTyped):
	if delimTyped == 'csv':
		localDelim = [',', 'csv']
	elif delimTyped == 'tsv':
		localDelim = ['\t', 'tsv']
	else:
		newDelimTyped = raw_input('Error. Please select either csv or tsv: ')
		localDelim = selectDelimiter(newDelimTyped)
	return localDelim

# Get input, should be either 'csv' or 'tsv' minus the quotes
delimInput = raw_input('What format would you like to save the files in? (Options: csv or tsv): ')
delim, delimLabel = selectDelimiter(delimInput)

print 'Working...'

# Loop over the schools in the list
for school, id in schools:
	# Set the url with each id
	url = 'http://www.osaa.org/teams/{0}?year=2016'.format(id)
	
	r = requests.get(url)
	
	# Create new empty list for below
	data = []
	
	soup = BeautifulSoup(r.text, 'lxml')
	# Find the correct schedule tab
	sked = soup.find(id="sub-tabs-schedule")
	# Loop over all the rows in the table with an index
	for i, tr in enumerate(sked.find_all('tr')):
		if i > 0:
			# Append new lists if not first
			data.append([])
		# Loop over cells with index
		for j, td in enumerate(tr.find_all('td')):
			# Just get the first six (don't need any more columns)
			if j < 6:
				# Get just the text (See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text)
				strings = td.get_text()
				if strings is not None:
					data[-1].append(strings)
	
	# For testing
# 	print data
	
	# Set directory and name of files (Example: csv/sheldon.csv)
	svname = '{0}/{1}.{0}'.format(delimLabel, school.lower().replace(' ', '-'))
	
	file = open(svname, 'wb')
	wr = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=delim)
	for i in data:
		wr.writerow(i)

print 'Done!'
