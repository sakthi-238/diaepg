import requests
import xmltodict, json
from datetime import datetime

token = requests.get('https://ddt.vbox-you.shop/spiderman.php').json()['token']

# Preparing the EPG XML structure
epg_data = {
	"tv": {
		"channel": [],
		"programme": []
	}
}


with open("epg_dialog.json", "r", encoding="utf-8") as file:
	epg_json_data = json.load(file)


for eppg in epg_json_data:

	url = "https://api1.viu.lk/api/client/v2/default/shows/grid"

	headers = {
			"authorization": f"Bearer {token}",
			"user-agent": "Dart/3.3 (dart:io)"
	}


	params = {
		"start_date": "2025-02-03T18:30:00.000Z",
		"end_date": "2025-02-04T18:30:00.000Z",
		"channels": f"{eppg['Id']}",
		"translation": "en",
		"hash": "37a6259cc0c1dae299a7866489dff0bd"
	}

	response = requests.get(url, params=params, headers=headers)
	print(f"Channel Name: {eppg['Name']} Channel Id: {eppg['Id']} Status Code: {response.status_code}")

	#print(response.text)

	data = response.json()

	def format_time(dt_str):
		return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.000Z").strftime("%Y%m%d%H%M%S +0000")

	for channel in data["data"]:
		channels = {
				"@id": f"ts{eppg['Id']}",
				"display-name": eppg["Name"],
				"icon": {"@src": f"https://api1.viu.lk/api/client/v1/global/images/{eppg['logo_id']}?accessKey=WkVjNWNscFhORDBLCg=="}
		}

		channels = {k: v for k, v in channels.items() if v is not None}
		epg_data["tv"]["channel"].append(channels)
		for show in channel["shows"]:

				programme = {
						"@start": format_time(show["start"]),
						"@stop": format_time(show["end"]),
						"@channel": f"ts{channel['id']}",
						"@id": str(show["id"]),
						"title": show["title"],
						"icon": {"@src": f"https://api1.viu.lk/api/client/v1/global/images/{show['image_id']}?accessKey=WkVjNWNscFhORDBLCg=="}
				}

				programme = {k: v for k, v in programme.items() if v is not None}
				epg_data["tv"]["programme"].append(programme)
		
	xml_output = xmltodict.unparse(epg_data, pretty=True)

	with open("dialog.xml", "w", encoding="utf-8") as xml_file:
		xml_file.write(xml_output)	

	#break
