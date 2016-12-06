from bs4 import BeautifulSoup
import urllib
import webbrowser
import csv
import json

root = "https://algorithmia.com"
genres = ["computer_vision", "machine_learning", "etc", "utilities"] # The base tag goes here
# data = csv.writer(open((genre + ".csv"), "w+"))

languages = ["curl", "cli", "java", "scala", "javascript", "nodejs", "python", "ruby", "rust"]


for genre in genres:
	print genre + "Started!"
	with open((genre + ".csv"), "r") as csvfile:
		#with open((genre + "_complete.csv"), "w") as new_csv:
		with open((genre + ".txt"), "w") as json_out:
			reader = csv.reader(csvfile)
			# writer = csv.writer(new_csv, delimiter = ',')
			# handler = csv.DictWriter(new_csv, fieldnames= ["Title", "Path", "Summary", "Label", "Details", "Permissions", "curl", "cli", "java", "scala", "javascript", "nodejs", "python", "ruby", "rust"])
			# handler.writeheader()
			# Commented out for exporting as JSON
			for row in reader:
				path = row[1]
				url = root + path

				r = urllib.urlopen(str(url))
				soup = BeautifulSoup(r)

				content = soup.find('div', class_="text-wordwrap summary-content")
				descr = str(content.find_all('span')[0])[25:-7]

				permissions_list = soup.find('div', class_="banner-info")
				permissions_list = permissions_list.find_all('span')
				permissions = []
				for i in range(1, len(permissions_list)):
					permissions.append(permissions_list[i].text)
				join_char = " | "
				permissions = join_char.join(permissions)

				syntax = []
				for lang in languages:
					syntax_list = soup.find_all('div', {"id":lang})
					syntax.append(syntax_list[0].find('code').text)
				new_row = row + [descr] + [permissions] + syntax
				json.dump(new_row, json_out)

	print genre + "Done!"
				