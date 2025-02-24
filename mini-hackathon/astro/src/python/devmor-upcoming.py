#Author: busara-s
#Create date: 23/02/25
#Desc: Shows upcomming BKK dev morning meetups.
# API only avaliable for meetups pro plan.

import requests

# Your Meetup API key
api_key = 'YOUR_MEETUP_API_KEY'

# SG
#group_urlname = 'sg-devmorning'

#Japan - https://www.meetup.com/dev-morning/
#group_urlname = 'dev-morning'

# BKK Dev Morning
group_urlname = 'bkk-devmorning'



# Meetup API endpoint for upcoming events
url = f'https://api.meetup.com/{group_urlname}/events?&sign=true&photo-host=public&page=20&key={api_key}'

# Make the request
response = requests.get(url)

if response.status_code == 200:
    events = response.json()
    if events:
        for event in events:
            print(f"Event Name: {event['name']}")
            print(f"Event Date: {event['local_date']} at {event['local_time']}")
            print(f"Event Link: {event['link']}\n")
    else:
        print("No upcoming events found.")
else:
    print(f"Error fetching events: {response.status_code}")




