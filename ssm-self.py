import boto3
import csv
ssm = boto3.client('ssm')
aws_mag_con=boto3.session.Session()
aws_ec2_con=aws_mag_con.client("ec2")
response=aws_ec2_con.describe_instances()["Reservations"]
instance_list=[]
count=1
hostname_error="NA"
csv_ob=open("satish_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","Host","Instance Id","State","Instance Type","AZ","Private IP","VPC ID","SubnetID"])
#print(response)
for item in response:
    for each in item['Instances']:
        #print(each)
        instance_list.append(each['InstanceId'])

for instance_id in instance_list:
    try:
        instance = aws_ec2_con.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
        state = instance['State']['Name']
        #print(hostname,instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId'])
        
        if state != 'running':
            print(f"Instance {instance_id} is not running")
            continue
        
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'hostname'
                ]
            }
        )

        command_id = response['Command']['CommandId']

        while True:
            status_response = ssm.list_commands(
                CommandId=command_id,
                InstanceId=instance_id
            )
            status = status_response['Commands'][0]['Status']
            if status in ['Pending', 'InProgress']:
                continue
            elif status == 'Success':
                output_response = ssm.get_command_invocation(
                    CommandId=command_id,
                    InstanceId=instance_id
                )
                hostname = output_response['StandardOutputContent']
                hostname=hostname.strip()
                #print(f"The hostname of instance {instance_id} is {hostname.strip()}")
                
                print(count,hostname,instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId'])
                csv_w.writerow([count,hostname,instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId']])
                
                count=count+1
                break
            else:
                print(f"Error executing command on instance {instance_id}")
                break
        #print(instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId'])
    
    except Exception as e:
        print(count,hostname_error,instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId'])
        csv_w.writerow([count,hostname_error,instance['InstanceId'],instance['State']['Name'],instance['InstanceType'],instance['Placement']['AvailabilityZone'],instance['PrivateIpAddress'],instance["VpcId"],instance['SubnetId']])
        count=count+1
        continue