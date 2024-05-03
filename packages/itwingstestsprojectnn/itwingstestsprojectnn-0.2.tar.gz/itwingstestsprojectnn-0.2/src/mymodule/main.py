from google.oauth2 import service_account
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from gacs.config import *

# Define needed variables
SCOPES = ['https://www.googleapis.com/auth/webmasters',
          'https://www.googleapis.com/auth/webmasters.readonly']

def passed_or_failed(check_impressions, check_clicks, check_average_position):
    # Check Impressions
    if check_impressions < thresholds['Impressions']['Red']:
        return 'failed'
    # Check Clicks
    elif check_clicks < thresholds['Clicks']['Red']:
        return 'failed'
    # Check Average Position
    elif check_average_position > thresholds['Average Position']['Green']:
        return 'failed'
    else:
        return 'passed'

def main(url, gsc, max_rows, credentials):
    try:
        if gsc == "yes":
            try:
                webmasters_service = initialize_service(credentials)
                if webmasters_service is None:
                    return None
            except Exception as e:
                print(f"Error initializing service: {e}")
                return None

            start_date_str = start_date.strftime('%Y-%m-%d')
            current_end_date_str = end_date.strftime('%Y-%m-%d')
            start_row = 0
            request = {
                'startDate': start_date_str,
                'endDate': current_end_date_str,
                'dimensions': [],
                'rowLimit': max_rows,
                'startRow': start_row
            }
            response = webmasters_service.searchanalytics().query(siteUrl=url, body=request).execute()
            if 'rows' in response and response['rows'] and all(key in response['rows'][0] for key in ['impressions', 'clicks', 'position']):
                data = {
                    'url': url,
                    'GSC Impressions': response['rows'][0]['impressions'],
                    'GSC Clicks': response['rows'][0]['clicks'],
                    'GSC CTR': "{:.2%}".format(response['rows'][0]['clicks'] / response['rows'][0]['impressions']),
                    'GSC Average Position': round(response['rows'][0]['position']),
                    'Phase 2': passed_or_failed(response['rows'][0]['impressions'], response['rows'][0]['clicks'], round(response['rows'][0]['position']))
                }
                print("Result of adding:", data)
                return data
            else:
                data = {
                    'url': url,
                    'GSC Impressions': "-",
                    'GSC Clicks': "-",
                    'GSC CTR': "-",
                    'GSC Average Position': "-",
                    'Phase 2': "no access"
                }
                return data
        else:
            data = {
                'url': url,
                'GSC Impressions': "-",
                'GSC Clicks': "-",
                'GSC CTR': "-",
                'GSC Average Position': "-",
                'Phase 2': "no access"
            }
            return data
    except Exception as e:
        print(f"Error: {e}")
        data = {
            'url': url,
            'GSC Impressions': "-",
            'GSC Clicks': "-",
            'GSC CTR': "-",
            'GSC Average Position': "-",
            'Phase 2': "no access"
        }
        return data
        
def initialize_service(gsc_credentials):
    credentials = service_account.Credentials.from_service_account_info(gsc_credentials, scopes=SCOPES)
    service = build('webmasters', 'v3', credentials=credentials)
    return service
