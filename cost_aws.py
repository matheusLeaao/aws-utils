#!/usr/bin/env python3

import boto3
import datetime
from dateutil.relativedelta import relativedelta

accessKey = sys.argv[1]
secretKey = sys.argv[2]
now = datetime.datetime.utcnow()
last_month = now + relativedelta(months=-1)
year = int(str(now).split('-')[0])
month = int(str(now).split('-')[1])
day = 1
start = datetime.datetime(year = year, month = month, day = day).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')
cd = boto3.client('ce', aws_access_key_id=accessKey,
                 aws_secret_access_key=secretKey, region_name='us-east-1')
results = []
custo =0
token = None
while True:
    if token:
        kwargs = {'NextPageToken': token}
    else:
        kwargs = {}
    data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
    results += data['ResultsByTime']
    token = data.get('NextPageToken')
    if not token:
        break

#print('\t'.join(['TimePeriod', 'LinkedAccount', 'Service', 'Amount', 'Unit', 'Estimated']))
for result_by_time in results:
    for group in result_by_time['Groups']:
        amount = group['Metrics']['UnblendedCost']['Amount']
        custo += float(amount)
        #unit = group['Metrics']['UnblendedCost']['Unit']
        #print(result_by_time['TimePeriod']['Start'], '\t', '\t'.join(group['Keys']), '\t', amount, '\t', unit, '\t', result_by_time['Estimated'])
print(custo)
