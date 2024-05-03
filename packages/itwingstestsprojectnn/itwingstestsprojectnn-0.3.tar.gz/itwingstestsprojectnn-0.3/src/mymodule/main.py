from google.oauth2 import service_account
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from mymodule.config import *

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


def main(credentials, parameters):
    try:
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
            'startDate': parameters['start_date'],
            'endDate': parameters['end_date'],
            # Assign dimensions from parameters
            'dimensions': parameters['dimensions'],
            'rowLimit': parameters['max_rows'],
            'startRow': start_row
        }
        response = webmasters_service.searchanalytics().query(
            siteUrl=parameters['url'], body=request).execute()

        if 'rows' in response and response['rows'] and all(key in response['rows'][0] for key in ['impressions', 'clicks', 'position']):
            data = {
                'url': parameters['url'],
                'GSC Impressions': response['rows'][0]['impressions'],
                'GSC Clicks': response['rows'][0]['clicks'],
                'GSC CTR': "{:.2%}".format(response['rows'][0]['clicks'] / response['rows'][0]['impressions']),
                'GSC Average Position': round(response['rows'][0]['position']),
                'Phase 2': passed_or_failed(response['rows'][0]['impressions'], response['rows'][0]['clicks'], round(response['rows'][0]['position']))
            }
            # Add dimensions dynamically to the data dictionary
            for dim in parameters.get('dimensions', []):
                data[f'GSC {dim.capitalize()}'] = response['rows'][0]['keys'][parameters['dimensions'].index(
                    dim)]
            print("Result of data:", data)

            return data
        else:
            data = {
                'url': parameters['url'],
                'GSC Impressions': "-",
                'GSC Clicks': "-",
                'GSC CTR': "-",
                'GSC Average Position': "-",
                'Phase 2': "no access"
            }
            # Add dimensions dynamically to the data dictionary
            for dim in parameters.get('dimensions', []):
                data[f'GSC {dim.capitalize()}'] = "-"
            return data
    except Exception as e:
        print(f"Error: {e}")
        data = {
            'url': parameters['url'],
            'GSC Impressions': "-",
            'GSC Clicks': "-",
            'GSC CTR': "-",
            'GSC Average Position': "-",
            'Phase 2': "no access"
        }
        return data


def initialize_service(gsc_credentials):
    credentials = service_account.Credentials.from_service_account_info(
        gsc_credentials, scopes=SCOPES)
    service = build('webmasters', 'v3', credentials=credentials)
    return service
