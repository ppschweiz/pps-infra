#syncjob-hitobito-listmonk.py scripty by Lukas 11.2025 - V1.1
#Sync hitobito group members with Listmonk users
import requests
from requests.auth import HTTPBasicAuth

# ==== variables ====
# The hitobito token:
h_token = "{{ lookup('hashi_vault', 'secret=secret/hitobito/api/listmonk-token:value') }}"
# The hitobito group number
h_no = "52"
# The hitobito API endpoint with group number:
h_url = "https://piraten.hitobito.com/de/groups/" + h_no + "/people.json?token=" + h_token
# The Listmonk token for the user "hitobito-api":
l_token = "{{ lookup('hashi_vault', 'secret=secret/listmonk/api/hitobito-api:value') }}"
# The Listmonk API endpoint:
l_url = "https://newsletter.piratenpartei.ch/api/subscribers"
# The Listmonk newsletter list number
l_no = 22

# ==== Run ====
# A GET request to the hitobito API
response = requests.get(h_url)

# Convert the response
response_json = response.json()
mylist = response_json["people"]

# Print hitobito response
for i in mylist:
    print(i["email"],",",i["first_name"], sep='')

# Post to listmonk a user per for loop
for subscriber in mylist:
    # Prepair data from mylist
    data = {
        "email": subscriber["email"],
        "name": subscriber["first_name"],
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

    # Print Listmonk response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
