from google.oauth2 import service_account
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from mymodule.config import *
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest, Dimension, FilterExpression, Filter, FilterExpressionList
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError

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


def GAC(credentials, parameters):
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


def GA4(GA4parameters, credentials_json):
    try:
        if GA4parameters['ga4'] == "yes":
            credentials = service_account.Credentials.from_service_account_info(
                credentials_json)
            client = BetaAnalyticsDataClient(credentials=credentials)

            request = RunReportRequest(
                property=f"properties/{GA4parameters['ga4_property_id']}",
                dimensions=[Dimension(name="sessionMedium")],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions"),
                    Metric(name="bounceRate"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="engagementRate")
                ],
                date_ranges=[
                    DateRange(start_date=GA4parameters['start_date'], end_date=GA4parameters['end_date'])],
            )
            response = client.run_report(request)

            # Initialize counters
            total_sessions = 0
            organic_sessions = 0
            total_users = 0
            bounce_rate_sum = 0
            avg_session_duration_sum = 0
            engagement_rate_sum = 0

            # Process response to calculate metrics
            for row in response.rows:
                sessions = int(row.metric_values[1].value)
                total_sessions += sessions
                total_users += int(row.metric_values[0].value)
                bounce_rate_sum += float(row.metric_values[2].value) * sessions
                avg_session_duration_sum += float(
                    row.metric_values[3].value) * sessions
                engagement_rate_sum += float(
                    row.metric_values[4].value) * sessions

                if row.dimension_values[0].value.lower() == "organic":
                    organic_sessions += sessions

            # Calculate metrics
            percentage_organic_traffic = (
                organic_sessions / total_sessions * 100) if total_sessions > 0 else 0
            average_bounce_rate = (
                bounce_rate_sum / total_sessions) if total_sessions > 0 else 0
            average_session_duration = (
                avg_session_duration_sum / total_sessions) if total_sessions > 0 else 0
            average_engagement_rate = (
                engagement_rate_sum / total_sessions) if total_sessions > 0 else 0

            # Create the single result row
            row_data = {
                "url": GA4parameters['url'],
                "Organic Traffic": organic_sessions,
                "Percentage Organic Traffic": f"{percentage_organic_traffic:.2f}%",
                "Total Users": total_users,
                "Average Bounce Rate": f"{average_bounce_rate:.2%}",
                "Average Session Duration": f"{average_session_duration:.2f}",
                "Average Engagement Rate": f"{average_engagement_rate:.2%}",
                "Phase 3": passed_or_failedGA4(percentage_organic_traffic, average_bounce_rate)
            }
            rows = [row_data]
            # Using the adapted function to write/append to CSV
            return rows
        else:
            row_data = {
                "url": GA4parameters['url'],
                "Organic Traffic": "-",
                "Percentage Organic Traffic": "-",
                "Total Users": "-",
                "Average Bounce Rate": "-",
                "Average Session Duration": "-",
                "Average Engagement Rate": "-",
                "Phase 3": "no access"
            }
            rows = [row_data]
            return rows
    except GoogleAPICallError as e:
        print(f"Error: {e}")
        # Save "no access" to CSV in case of an error
        row_data = {
            "url": GA4parameters['url'],
            "Organic Traffic": "-",
            "Percentage Organic Traffic": "-",
            "Total Users": "-",
            "Average Bounce Rate": "-",
            "Average Session Duration": "-",
            "Average Engagement Rate": "-",
            "Phase 3": "no access"
        }
        rows = [row_data]
        return rows

# Function to determine passed or failed based on the given thresholds


def passed_or_failedGA4(percentage_organic_traffic, average_bounce_rate):
    # Check Impressions
    if percentage_organic_traffic > 65:
        return 'failed'
    # Check Clicks
    elif average_bounce_rate > 55:
        return 'failed'
    # Check Average Position
    # elif check_average_position > thresholds['Average Position']['Green']:
    #     return 'failed'
    else:
        return 'passed'
