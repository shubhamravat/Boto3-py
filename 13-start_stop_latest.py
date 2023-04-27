import boto3
import datetime
import pytz
from datetime import datetime
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
sns_con_cli = aws_mag_con.client("sns")
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
current_time_ist = now.strftime('%H:%M')
print(current_time_ist)
sns_topic_arn ="arn:aws:sns:ap-south-1:532102821576:Offer"
start_times = {
    'wordpress': datetime(2023, 2, 20, 14, 17, 0, tzinfo=tz),
    'myangularapp': datetime(2023, 2, 20, 14, 17, 0, tzinfo=tz)
}


f1=[{'Name': 'tag-key', 'Values': ['Schedule']},    
            {'Name': 'tag-value', 'Values': ['True']}
        ]
def start_instances(f1):
    # Get the list of all instances with the Schedule tag set to "True"
    reservations = aws_ec2_cli.describe_instances(Filters=f1)['Reservations']

    # Loop through each instance and check its tags to determine whether it should be started
    for item in reservations:
        for instance in item['Instances']:
            # Check if the instance has an Application tag
            if 'Tags' in instance:
                tags = instance['Tags']
                print(tags)
                tag_keys = []
                for tag in tags:
                    tag_keys.append(tag['Key'])
                if 'application' in tag_keys:
                    app_name = None
                    for tag in tags:
                        if tag['Key'] == 'application':
                            app_name = tag['Value']
                            break
                    start_times_IST=start_times[app_name].astimezone(tz).strftime('%H:%M')
                    print(start_times_IST)
                    # Check if the start time has been reached for this instance's application
                    if current_time_ist == start_times_IST:
                        # Start the instance
                        aws_ec2_cli.stop_instances(InstanceIds=[instance['InstanceId']])
                        print(f"Stopping {app_name} instance with ID {instance['InstanceId']}")
                        # Send SNS message when the instance starts
                        message = f"The {app_name} instance with ID {instance['InstanceId']} has stopped."
                        response = sns_con_cli.publish(TopicArn=sns_topic_arn, Message=message)
                        print("SNS message sent:", response['MessageId'])
                    else:
                        print("time not matching")

start_instances(f1)