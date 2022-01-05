import requests
import json
import sys

url = "https://api.swapcard.com/graphql"
auth_token = 'foobar'
head = {'Authorization': 'Bearer ' + auth_token}
data = [
    {
        "operationName": "EventPeopleList",
        "variables": {
            "viewId": "RXZlbnRWaWV3XzMwMzgzOQ==",
            "search": "",
            "selectedFilters": [
                {
                    "mustEventFiltersIn": []
                }
            ],
            "sort": None,
            "endCursor": None
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "c62b436f3122cb87a03f761bd856e63f7f1d37cbcb43f3010434a86490f0a28c"
            }
        }
    }
]

attendees = []
has_endCursor = True
response = requests.post(url, json=data, headers=head)
while has_endCursor:
    response = requests.post(url, json=data, headers=head)
    for i in json.loads(response.text)[0]['data']['view']['people']['nodes']:
        attendees.append(i)
    has_endCursor = json.loads(response.text)[0]['data']['view']['people']['pageInfo']['hasNextPage']

    if has_endCursor:
        next_endCursor = json.loads(response.text)[0]['data']['view']['people']['pageInfo']['endCursor']
        data[0]['variables']['endCursor'] = next_endCursor

print(json.dump(attendees, sys.stdout, indent=4))
