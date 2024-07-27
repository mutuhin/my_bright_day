import pandas as pd
import requests
from pathlib import Path

# Initialize the session
session = requests.Session()

# Provided cookie string
cookie_string = (
    "IMS_SOURCE_SPECIFY=Other | LP_BH_Corporate | Desktop; "
    "OptanonAlertBoxClosed=2024-07-26T12:10:05.359Z; "
    "_gcl_au=1.1.1888920633.1721995805; _gid=GA1.2.2120058078.1721995806; "
    "_tt_enable_cookie=1; _ttp=18g0JTukRdiU2vADjvG6AdOZjvl; "
    "_pin_unauth=dWlkPVlXRTRPVFF5WmpRdE5qUTVOQzAwTURobExXSTNObUV0TVdJNE5qZzVPVFU0TnpRMQ; "
    "_pendo_visitorId.672bb382-89e6-484c-6825-cb518fd863d2=; "
    "_pendo_accountId.672bb382-89e6-484c-6825-cb518fd863d2=; "
    "_pendo_meta.672bb382-89e6-484c-6825-cb518fd863d2=; "
    "_pendo_oldVisitorId.672bb382-89e6-484c-6825-cb518fd863d2=; "
    "_hjSessionUser_1090331=eyJpZCI6IjA2NThmNjEwLTJjMTEtNTBmNC04MjI1LTEzYzRlODExMzcxZiIsImNyZWF0ZWQiOjE3MjE5OTU4MDYwOTQsImV4aXN0aW5nIjp0cnVlfQ==; "
    "_pendo_visitorId.3527651379=73fb22ef-dcca-42d1-b867-3f9c117b4334; "
    "_pendo_oldVisitorId.3527651379=_PENDO_T_doM6iSIs5QM; "
    "_pendo_accountId.3527651379=fc2adc71-edba-ea11-a843-005056994c8e; "
    "_pendo_meta.3527651379=2121227886; _ga_0EY7LSHQSZ=GS1.1.1722023833.4.0.1722023833.0.0.0; "
    "_ga=GA1.2.1918225528.1721995806; _hjSessionUser_2516296=eyJpZCI6IjA0ZGRmMDg5LWEyMWItNWM1Ny1iZmU0LTExMjRhOTFjMjJjNyIsImNyZWF0ZWQiOjE3MjIwMTM2NTkxMDQsImV4aXN0aW5nIjp0cnVlfQ==; "
    "fs_uid=#o-1RB3CY-na1#40e25269-7bfe-44db-ba77-7c4b84a189b0:0fc212d0-0315-443b-8603-6249815b4fdf:1722031300898::1#881c95cf#/1753531890; "
    "OptanonConsent=isGpcEnabled=0&datestamp=Sat+Jul+27+2024+04%3A01%3A41+GMT%2B0600+(Bangladesh+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&consentId=8b9165e5-18ff-4c05-9535-62756b2304ae&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=BD%3BC&AwaitingReconsent=false; "
    "_uetsid=fee212804b4711ef8ff3e1ec1001e359; _uetvid=fee234d04b4711efb3fd39dcddfaa5ff; "
    "session=eyJ1c2VyX2lkIjogIjYyMTIzY2UzZmNiMDFhYzI4ZTM5MDdiOCIsICJ1c2VyX3R5cGUiOiAiZ3VhcmRpYW4iLCAiZXhwaXJlcyI6IDE3MjQ1OTE1NTguODkzOTEyLCAiaXNfbG9nZ2VkX2luIjogdHJ1ZX0=.ZqTC9A.5pl-m5fG_KUO9zxqZKN46f9suRY"
)

cookie_parts = cookie_string.split('; ')
for cookie in cookie_parts:
    name, value = cookie.split('=', 1)
    session.cookies.set(name, value)

csv_file_path = 'output.csv'
df = pd.read_csv(csv_file_path)

base_output_dir = Path('downloaded_images')
base_output_dir.mkdir(parents=True, exist_ok=True)

for month, group in df.groupby('Month'):
    month_dir = base_output_dir / month.replace(' ', '').lower()
    month_dir.mkdir(parents=True, exist_ok=True)

    for index, url in enumerate(group['URL'], start=1):
        try:
            response = session.get(url)
            response.raise_for_status()
            
            image_name = f'image{index:03}.jpg'
            image_path = month_dir / image_name
            
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            print(f'Downloaded {image_name} to {month_dir}')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download {url}: {e}')
