#job-sync-hitobito-listmonk.py scripty by Lukas 11.2025 - V1
#Sync hitobito group members with listmonk users
import requests
from requests.auth import HTTPBasicAuth

# ==== variables ====
h_token = xyz
l_token = 123
# The hitobito API endpoint:
h_url = "https://piraten.hitobito.com/de/groups/1/people.json?token=" + h_token
# The Listmonk API endpoint:
l_url = "https://newsletter.piratenpartei.ch/api/subscribers"
# The listmonk newsletter listnumber
l_no = 22

# ==== Run ====
# A GET request to the hitobito API
response = requests.get(url)

# Convert the response
response_json = response.json()
mylist = response_json["people"] 

# Print the response
for i in mylist:
    print(i["email"],",",i["first_name"], sep='')

# Post to listmonk a user per for loop
for subscriber in mylist:
    # Prepair data from mylist
    data = {
        "email": subscriber["email"],
        "name": subscriber["name"],
        "status": "enabled",
        "lists": [l_no]
    }

    # Post data
    response = requests.post(
        l_url,
        auth=HTTPBasicAuth('hitobito-api', l_token),
        headers={'Content-Type': 'application/json'},
        json=data
    )

    # Print response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
