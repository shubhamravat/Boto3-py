import boto3
import csv
import re
from botocore.exceptions import ClientError
from botocore.client import Config
from datetime import datetime, timedelta
import pytz
import os

# Fetch AWS credentials from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Alternatively, use AWS SDK to fetch credentials

aws_mag_con = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key , region_name='ap-south-1')




instance_dict={}
instance_dict_name={}
instance_name_list=[]
lambda_desc_list=[]
lambda_name_list=[]
tables_name=[]
api_list=[]
asg_list=[]
redshift_list=[]
kakfka_list=[]
inst_id_list=[]
sqs_name_list=[]


# Create a session using the exported credentials


aws_cli_ec2=aws_mag_con.client('ec2')
#response = aws_cli_ec2.describe_instances()
#print(response)

aws_cli_api = aws_mag_con.client('apigateway')
aws_cli_lambda=aws_mag_con.client('lambda')
aws_cli_elb=aws_mag_con.client('elbv2')
aws_cli_rds=aws_mag_con.client('rds')
aws_cli_dynamo=aws_mag_con.client('dynamodb')
aws_cli_asg=aws_mag_con.client('autoscaling')
aws_cli_redshift=aws_mag_con.client('redshift')
aws_cli_kafka=aws_mag_con.client('kafka')
aws_cli_sqs=aws_mag_con.client('sqs')
today = datetime.now()# Calculate one day before todayone_day_ago = today - timedelta(days=2)

target_date_report = today - timedelta(days=1)

date_string = target_date_report.strftime("%d %B %Y")

print("MediaReady Stats:", date_string)
first_row_value="MediaReady Stats:" +  date_string
ist_tz = pytz.timezone('Asia/Kolkata')

utc_tz = pytz.utc

# Get current datetime in IST
ist_now = datetime.now(ist_tz)

print('IST NOW:::::::',ist_now)

# Calculate one day ago in IST
one_day_ago_ist = ist_now - timedelta(days=1)

# Set time to midnight (00:00:00)
start_ist = one_day_ago_ist.replace(hour=0, minute=0, second=0)

# Set time to 23:59:59
end_ist = one_day_ago_ist.replace(hour=23, minute=59, second=0)

# Convert IST times to UTC
start_utc = start_ist.astimezone(utc_tz)
end_utc = end_ist.astimezone(utc_tz)

# Format UTC times as strings
start_utc_str = start_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
end_utc_str = end_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

print("Start Time (UTC):", start_utc_str)
print("End Time (UTC):", end_utc_str)

datetime_obj = datetime.strptime(end_utc_str, "%Y-%m-%dT%H:%M:%SZ")

# Extract and format the date
date_only = datetime_obj.strftime("%Y-%m-%d")


count=0
# CloudWatch Client
aws_cloudwatch_cli = aws_mag_con.client('cloudwatch')

namespace_list = []
csv_ob=open(f"/root/insufficient_alarms_inventory_{date_only}.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","AlarmName","Arn","State","namespace value","Attached Resource","Instance_State"])
# Describe CloudWatch Alarms with pagination
alarms = []
row_count=0
paginator = aws_cloudwatch_cli.get_paginator('describe_alarms')
for response in paginator.paginate():
    alarms.extend(response['MetricAlarms'])
#print(alarms)
count = len(alarms)


for item1 in alarms:
    #print(item['Namespace'])
   if 'Namespace' in item1:
       name_space_value=item1['Namespace']
       if name_space_value not in namespace_list:
           namespace_list.append(name_space_value)
   else:
       print(item1['AlarmName'])

#print(namespace_list)

###EC2 describe #####
response_ec2=aws_cli_ec2.describe_instances()['Reservations']
for item in response_ec2:
    for items in item['Instances']:
        instance_id=(items['InstanceId'])
        inst_id_list.append(instance_id)
        instance_state=items['State']['Name']
        for tag in items['Tags']:
            if tag['Key']=='Name':
                instance_name=tag['Value']
                instance_name_list.append(instance_name)

        instance_dict_name[instance_id] = {
            'Name': instance_name,
            'State': instance_state

        }
        instance_dict[instance_id] = instance_state
'''
response_ec2=aws_cli_ec2.describe_instances()['Reservations']
for item in response_ec2:
    for items in item['Instances']:
        instance_id=(items['InstanceId'])
        instance_state=items['State']['Name']
        instance_dict[instance_id]=instance_state
'''
###lambda describe####

paginator = aws_cli_lambda.get_paginator('list_functions')
for response in paginator.paginate():
    lambda_desc_list.extend(response['Functions'])
#print(lambda_list)
for lamb_item in lambda_desc_list:
    lambda_final_name=(lamb_item['FunctionName'])
    lambda_name_list.append(lambda_final_name)


##### api describe #######

response_api = aws_cli_api.get_rest_apis()['items']
for item_api in response_api:
    api_name=item_api['name']
    api_list.append(api_name)



########## ASG DESCRIBE ######


response_asg = aws_cli_asg.describe_auto_scaling_groups()['AutoScalingGroups']
for item in response_asg:
    asg_name=item['AutoScalingGroupName']
    asg_list.append(asg_name)



##### REDSHIFT DESCRIBE #####

response_redshift = aws_cli_redshift.describe_clusters()['Clusters']
for item_redshift in response_redshift:
    redshift_name=item_redshift['ClusterIdentifier']
    redshift_list.append(redshift_name)


######## KAFKA DESCRIBE #############
response_kafka=aws_cli_kafka.list_clusters()['ClusterInfoList']
for item_kakfka in response_kafka:
    kafka_cluster_name=item_kakfka['ClusterName']
    kakfka_list.append(kafka_cluster_name)


#####Describe SQS  #########

response_sqs=aws_cli_sqs.list_queues()
for item_sqs in response_sqs['QueueUrls']:
    #print(item)
    queue_name = item_sqs.split('/')[-1]
    #print(queue_name)
    sqs_name_list.append(queue_name)


for item2 in alarms:
    if 'Namespace' in item2:
        row_count=row_count+1
        if row_count==1500:
            print(row_count)
        Resource_Value='NA'
        instance_state='NA'
        if item2['Namespace']=='AWS/EC2' or item2['Namespace']=='CWAgent' or item2['Namespace']=='System/Linux':
            dimensions = item2['Dimensions']
            for d in dimensions:
                insid=d['Value']
                #print(insid)
                if insid in instance_dict:
                    Resource_Value=insid
                    instance_state=instance_dict[insid]
                    break
            if instance_state=='NA':
                instance_state='Terminated'


        elif item2['Namespace']=='AWS/Lambda':
            lambda_name=item2['Dimensions']
            for d in lambda_name:
                lambda_names=d['Value']
                #print(lambda_names)
                #print(lambda_name_list)
                if lambda_names in lambda_name_list:
                        Resource_Value=lambda_names
                        break

        elif item2['Namespace']=='AWS/RDS':
            response_rds=aws_cli_rds.describe_db_instances()
            rdsdb=item2['Dimensions']
            for d in rdsdb:
                rds_id=d['Value']
                #print(rds_id)
                for item_rds in response_rds['DBInstances']:


                    rds_identifier=item_rds['DBInstanceIdentifier']
                    if rds_identifier == rds_id:
                            Resource_Value=rds_identifier
                            break

        elif item2['Namespace']=='AWS/ApplicationELB':
            response_elb = aws_cli_elb.describe_load_balancers()
            elbarn=item2['Dimensions']
            for d in elbarn:
                elb_arns=d['Value']
                #print("lb arn from alarm = ",elb_arns)
                for elb in response_elb['LoadBalancers']:
                    elbin_arn=elb['LoadBalancerArn']
                    #print("load balancer arn=",elbin_arn)
                    if elb_arns in elbin_arn:
                            Resource_Value=elbin_arn
                            break
        elif item2['Namespace']=='ContainerInsights':
            eks_client = aws_mag_con.client('eks')
            #print(eks_client)
            response_container_insgt = eks_client.list_clusters()['clusters']
            containerinsight_dimensions = item2['Dimensions']
            for ci in containerinsight_dimensions:
                container_ci_value=ci['Value']
                if container_ci_value in response_container_insgt:
                    Resource_Value = container_ci_value
                    break

        elif item2['Namespace']=='AWS/DynamoDB':
            dynamo_dimension=item2['Dimensions']
            response_dynamo = aws_cli_dynamo.list_tables()
            for item in response_dynamo['TableNames']:
                tables_name.append(item)
            for dynamo_value in dynamo_dimension:
                dynamo_value_new=dynamo_value['Value']
                if dynamo_value_new in tables_name:
                    #print("yes")
                    Resource_Value=dynamo_value_new
                    break

        elif item2['Namespace']=='AWS/ApiGateway':
            response_api = aws_cli_api.get_rest_apis()
            api_id=item2['Dimensions']
            for d in api_id:
                api_ids=d['Value']
                print(api_ids)
                if api_ids in api_list:
                    Resource_Value=api_ids
                    break

        elif item2['Namespace']=='AWS/AutoScaling':
            asg_dimensions = item2['Dimensions']
            for autog in asg_dimensions:
                asg_dimensions_value=autog['Value']
                if asg_dimensions_value in asg_list:
                    Resource_Value=asg_dimensions_value
                    break

        elif item2['Namespace']=='AWS/Redshift':
            redshift_dimensions=item2['Dimensions']
            for redsft in redshift_dimensions:
                redshift_dimensions_value=redsft['Value']
                if redshift_dimensions_value in redshift_list:
                    Resource_Value=redshift_dimensions_value
                    break

        elif item2['Namespace']=='AWS/Kafka':
            kafka_dimensions=item2['Dimensions']
            for item_kafk in kafka_dimensions:
                kafka_dimensions_value=item_kafk['Value']
                if kafka_dimensions_value in kakfka_list:
                    Resource_Value=kafka_dimensions_value
                    break

        elif item2['Namespace']=='SERVICES' or item2['Namespace']=='MONGO' or item2['Namespace']=="Pgpool" or item2['Namespace']=='KAFKA' or item2['Namespace']=='HAZELCAST':
            ec2_alarm_name=item2['AlarmName']
            pattern = r"/(i-[a-zA-Z0-9]+)/"
            match = re.search(pattern, ec2_alarm_name)
            if match:
    # Access the matched instance ID group
                instance_id_dimensions = match.group(1)
                if instance_id_dimensions in inst_id_list:
                    Resource_Value=instance_id_dimensions
                    print(Resource_Value)
                    instance_state=instance_dict[Resource_Value]
                    print("final state",instance_state)

            if instance_state=='NA':
                instance_state='Terminated'

        elif item2['Namespace']=='RABBITMQ':
                #print(item2)
                for item_mq in item2['Dimensions']:
                     if item_mq['Name']=='ServiceName':
                          mq_dimensions=item_mq['Value']
                          Resource_Value=mq_dimensions

        elif item2['Namespace']=='AWS/SQS':
                for item_sqs in item2['Dimensions']:
                     if item_sqs['Name']=='QueueName':
                          sqs_dimensions=item_sqs['Value']
                          if sqs_dimensions in sqs_name_list:
                            Resource_Value=sqs_dimensions




        csv_w.writerow([row_count, item2["AlarmName"], item2["AlarmArn"], item2["StateValue"], item2['Namespace'], Resource_Value,instance_state])
        #print(f"Writing row for {item2['AlarmName']}")


csv_ob.close()
s3_cp_client = aws_mag_con.client(
    's3'
    #aws_access_key_id=aws_access_key_id,
   # aws_secret_access_key=aws_secret_access_key
)

# Copy file from local directory to S3 bucket
s3_cp_client.upload_file(f"/root/insufficient_alarms_inventory_{date_only}.csv", 'jenkins-bucket-2024', f"insufficient_alarms_inventory_{date_only}.csv")
print("file uploaded to the bucket")

# After the upload_file function call
upload_output = f"File uploaded to bucket: jenkins-bucket-2024 as insufficient_alarms_inventory_{date_only}.csv"

# Print the output
print(upload_output)




sns_client = aws_mag_con.client('sns',region_name='ap-south-1')
s3_client = aws_mag_con.client('s3',config=Config(signature_version='s3v4') ,region_name='ap-south-1')
response = s3_client.generate_presigned_url('get_object',Params={'Bucket': 'jenkins-bucket-2024','Key': f'insufficient_alarms_inventory_{date_only}.csv'},HttpMethod='GET',ExpiresIn=5000)
print(response)
presigned_url=response

topic_arn = 'arn:aws:sns:ap-south-1:940231484373:access_key_rotation'
message = f"Hi please find the downloaded link to the auto generated media ready daily monitoring report placed in S3 bucket jenkins-bucket-2024, click on the link to download the excel file:  {presigned_url}"

response = sns_client.publish(
    TopicArn=topic_arn,
     Subject="Media Ready Daily Monitoring Report Download Link",
    Message=message,
    MessageAttributes={
        'email': {
            'DataType': 'String',
            'StringValue': 'rawatshubham198@gmail.com'
        }
    }
)

print(message)

print("Message published with message ID:", response['MessageId'])
