import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialize InfluxDB client
influxdb_url = "http://localhost:8086"
token = "your-influxdb-token"
org = "your-org"
bucket = "jaeger-traces"

client = influxdb_client.InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Function to read Jaeger data from a file
def read_jaeger_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Convert Jaeger data to InfluxDB points
def jaeger_to_influxdb(data):
    points = []
    for trace in data['data']:
        trace_id = trace['traceID']
        processes = trace['processes']
        
        for span in trace['spans']:
            # Get span details
            span_id = span['spanID']
            operation_name = span['operationName']
            duration = span['duration']
            start_time = span['startTime']
            process_id = span['processID']
            service_name = processes[process_id]['serviceName']
            
            # Prepare InfluxDB point
            point = influxdb_client.Point("spans") \
                .tag("traceID", trace_id) \
                .tag("spanID", span_id) \
                .tag("service_name", service_name) \
                .tag("operation_name", operation_name) \
                .field("duration", duration) \
                .time(start_time, write_precision="ns")
            
            # Add span tags as InfluxDB tags
            for tag in span['tags']:
                key = tag['key']
                value = tag['value']
                if tag['type'] == 'string':
                    point = point.tag(key, value)
                elif tag['type'] == 'int64':
                    point = point.field(key, int(value))
            
            points.append(point)
    
    return points

# Read Jaeger data from a file (replace 'jaeger_data.json' with your actual file path)
file_path = 'otel-end-to-end.json'
jaeger_data = read_jaeger_data_from_file(file_path)

# Convert the Jaeger data to InfluxDB points
influxdb_points = jaeger_to_influxdb(jaeger_data)
# Write points to InfluxDB
write_api.write(bucket=bucket, org=org, record=influxdb_points)

print("Data written to InfluxDB successfully.")
