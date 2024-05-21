import re
# from elasticsearch import Elasticsearch
from elasticsearch import helpers,Elasticsearch
import datetime

CLOUD_ID = "128c49d897614d8cbbc6bf89e2ccbf0d:dXMtY2VudHJhbDEuZ2NwbC5jbG91ZC5lcy5pby80NDMkYWIxZjUzNzM5MDhhNGJjNjlmMjgzMjFlM2U2OTMxMjUkM2EyZWVkYzU0NzU5NDM1YzgwYThiY2IyZTc0YzYwMjA=="


es = Elasticsearch(
    "https://ab1f5373908a4bc69f28321e3e693125.us-central1.gcp.cloud.es.io",  # Elasticsearch endpoint
    api_key="NGVjamw0OEJ5VHdoclV5eENFY2I6NXlDUGVDTGpRQWE0VUlfZEtvRHF1dw==",
)
# Define the log pattern
log_pattern = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<level>\w+) - (?P<message>.*)'
)

def get_log_filename():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"logging_{today}.log"
# Log file path
log_file_path ="logging.log"

# Function to parse log line using log pattern
def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

# Function to read log file and push to Elasticsearch
def push_logs_to_elasticsearch():
    with open(log_file_path, 'r') as file:
        actions = []
        for line in file:
            print(f"Processing line: {line.strip()}")
            parsed_line = parse_log_line(line)
            if parsed_line:
                print(f"Parsed line: {parsed_line}")
                # Add metadata for Elasticsearch
                action = {
                    "_index": "logs-index",
                    "_source": {
                        "timestamp": parsed_line['timestamp'],
                        "level": parsed_line['level'],
                        "message": parsed_line['message']
                    }
                }
                actions.append(action)
            else:
                print(f"Line did not match pattern: {line.strip()}")
        
        # Print actions for debugging
        print("Actions to be pushed to Elasticsearch:")
        print(actions)

        # Bulk push to Elasticsearch
        if actions:
            helpers.bulk(es, actions)
            print(f"Pushed {len(actions)} logs to Elasticsearch.")
        else:
            print("No valid log lines found.")

# if __name__ == "__main__":
#     push_logs_to_elasticsearch()