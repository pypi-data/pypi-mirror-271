from datetime import datetime, timedelta
import os



# Access the API key from environment variables
SEMRUSH_KEY = os.getenv("SEMRUSH_KEY")
GCLOUD_FOLDER_ID = os.getenv("GCLOUD_FOLDER_ID")
MASTERDATA_SHEET_ID = os.getenv("MASTERDATA_SHEET_ID")

############################################################################################################
# General
############################################################################################################

# Define the start date and interval (last full month)
today = datetime.today()
start_date = datetime(today.year, today.month - 1, 1)
end_date = datetime(today.year, today.month, 1) - timedelta(days=1)


month = today.month - 6 if today.month > 6 else 12 + (today.month - 6)
year = today.year if today.month > 6 else today.year - 1
start_date_ga4 = datetime(year, month, 1).strftime("%Y-%m-%d")
end_date_ga4 = (datetime(today.year, today.month, 1) - timedelta(days=1)).strftime("%Y-%m-%d")
credentials_directory = 'configuration/'
masterdata_directory = 'configuration/master.csv'
clean_data_directory = 'data/clean_data/key_content_domain_data.csv'
# master_data = {
#     url:'https://www.thebircherbar.com.au/',
#     gsc:'no',
#     ga4:'no'    
# }

# Path to your service account key file
service_account_file = 'configuration/key-content-api-connector.json'
# Directory you want to upload
upload_folder = 'data'
# Folder ID on Google Drive where files should be uploaded
folder_id = GCLOUD_FOLDER_ID
# Scopes required by the API
scopes = ['https://www.googleapis.com/auth/drive']



############################################################################################################
# Semrush
############################################################################################################

url = 'https://api.semrush.com/analytics/v1/'

url_alternative = 'https://api.semrush.com/'

# Construct the request parameters
params = {
'key': SEMRUSH_KEY,
'type': 'backlinks_overview',
'target': '',
'target_type': 'root_domain',
'export_columns': 'ascore,total,domains_num,urls_num,ips_num,ipclassc_num,follows_num,nofollows_num,sponsored_num,ugc_num,texts_num,images_num,forms_num,frames_num'
}

params_alternative_old = {
'key': SEMRUSH_KEY,
'type': 'domain_ranks',
'domain': '',
'export_columns' : 'Db,Dn,Or,Ot,Oc,Ad,At,Ac,Sh,Sv'
}
params_alternative = {
    'key': SEMRUSH_KEY,
    'type': 'domain_ranks',
    'domain': '',
}


output_folder = 'raw_data' # Folder to save the report


############################################################################################################
# Pagespeed
############################################################################################################

ps_config = {
    "strategies": ["desktop","mobile"],  # Strategies to use for the assessment
    "thresholds": {	
        "LCP": 2500,  # milliseconds
        "INP": 200,  # milliseconds
        "CLS": 0.1  # CLS score
    },
    "metrics": {
        "LCP": "LARGEST_CONTENTFUL_PAINT_MS",
        "INP": "INTERACTION_TO_NEXT_PAINT",
        "CLS": "CUMULATIVE_LAYOUT_SHIFT_SCORE",
        "FCP": "FIRST_CONTENTFUL_PAINT_MS",
        "FID": "FIRST_INPUT_DELAY_MS",
        "TTFB": "EXPERIMENTAL_TIME_TO_FIRST_BYTE"
    }
}

############################################################################################################
# GSC
############################################################################################################

max_rows = 25000

# Define thresholds for each metric
thresholds = {
    'Impressions': {'Red': 1000},
    'Clicks': {'Red': 1},
    'Average Position': {'Green': 20}
}

############################################################################################################
# GA4
############################################################################################################

# GA4 Property ID


############################################################################################################
# Screaming Frog
############################################################################################################

temp = "data/raw_data/temporary_raw_sf_data"
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
