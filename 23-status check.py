import boto3

aws_mag_con=boto3.session.Session()
aws_ec2_status=aws_mag_con.client("ec2")
response= aws_ec2_status.describe_instance_status()['InstanceStatuses']
sns_con_cli=aws_mag_con.client("sns")
status_check_instance_list=[]
sns_topic_arn ="arn:aws:sns:ap-south-1:532102821576:Offer"
for item in response:
    instance_status=(item['InstanceStatus']['Status']) 
    system_status=(item['SystemStatus']['Status'])
    if instance_status != 'ok' or system_status != 'ok':
        #print(item['InstanceId'])
        status_check_instance_list.append(item['InstanceId'])
        message = f"Instance with instance ID = {item['InstanceId']}  has failed status check ."
        response = sns_con_cli.publish(TopicArn=sns_topic_arn, Message=message)
        print("SNS message sent:", response['MessageId'])
    else:
         print("no status check fail All good!")

print(status_check_instance_list)