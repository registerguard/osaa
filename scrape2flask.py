import requests, lxml
from bs4 import BeautifulSoup
import pandas as pd
from flask import *

# HT: http://chrisalbon.com/python/beautiful_soup_scrape_table.html
# HT: https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html

# List of schools and ids
schools = {"Sheldon":15211, "South Eugene":15255, "Thurston":15371, "Willamette":15488, "Churchill":14384, "Marist":14844, "North Eugene":14967, "Springfield":15296, "Cottage Grove":14441, "Elmira":14556, "Juction City":14739, "Marshfield":14850, "North Bend":14953, "Siuslaw":15244, "Sutherlin":15347, "Sweet Home":15353, "Bandon":14258, "Creswell":14468, "Harrisburg":14650, "Pleasant Hill":15077, "Central Linn":14366, "Monroe":14909, "North Douglas":14962, "Oakland":15009, "Oakridge":15013, "Reedsport":15121, "Waldport":15439, "Alsea":14229, "Crow":14483, "Elkton":14551, "Lowell":14824, "Mapleton":14839, "McKenzie":14867, "Mohawk":14899, "Triangle Lake":15396, "Yoncalla":15525}

app = Flask(__name__)

@app.route('/schools')
def show_schools():
	
	return render_template('schools.html', list=schools)
	

@app.route('/schools/<school>')
def show_school(school):
	#Set the url with each id
	link = 'http://www.osaa.org/teams/{0}?year=2016'.format(schools[school])
	
	r = requests.get(link)
	
	soup = BeautifulSoup(r.text, 'lxml')
	
	date = []
	day = []
	time = []
	opp = []
	
	# Find the correct schedule tab
	sked = soup.find(id="sub-tabs-schedule")
	# Loop over all the rows in the table with an index
	for row in sked.find_all('tr')[1:]:
	
		col = row.find_all('td')
	
		col1 = col[2].get_text()
		date.append(col1)
	
		col2 = col[3].get_text()
		day.append(col2)
	
		col3 = col[4].get_text()
		time.append(col3)
	
		col4 = col[5].get_text()
		opp.append(col4)
	
	columns = {'date': date, 'day': day, 'time': time, 'opponent': opp}

	df = pd.DataFrame(columns)
	return render_template('school.html', table=df.to_html())
	


if __name__ == "__main__":
	app.run(debug=True)
