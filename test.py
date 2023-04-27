import boto3
import datetime
import pytz
from datetime import datetime
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
current_time_ist = now.strftime('%H:%M')
trigger_time=datetime(2023, 2, 15, 1, 16, 0, tzinfo=tz)
trigger_time_ist=trigger_time.strftime('%H:%M')

print(current_time_ist)
print(trigger_time_ist)

#https://dheeraj3choudhary.com/aws-lambda-and-eventbridge-or-find-unused-ebs-volumes-on-weekly--and-notify-via-email