import boto3
aws_mag_con_new=boto3.session.Session(region_name="ap-south-1")
aws_ssm_con_new=aws_mag_con_new.client('ssm',region_name="ap-south-1")
aws_ec2_con_new=aws_mag_con_new.client('ec2',region_name="ap-south-1")
instance_id_list=[]
instance_id_linux_list=[]
response=aws_ec2_con_new.describe_instances()['Reservations']
print(response)

for each_instance in response:
  for each_item in each_instance['Instances']:
    print(each_item['InstanceId'])
    instance_id_list.append(each_item['InstanceId'])
    print(each_item['PlatformDetails'])
    if each_item['PlatformDetails']=='Linux/UNIX':
        instance_id_linux_list.append(each_item['InstanceId'])
print(instance_id_list)
print(instance_id_linux_list)

for each_instance in response:
  for each_item in each_instance['Instances']:
    if each_item['PlatformDetails']=='Linux/UNIX':
        ssm_response=aws_ssm_con_new.send_command(InstanceIds=instance_id_list
          ,DocumentName='Copy-AWS-ConfigureAWSPackage',DocumentVersion= '5')
    else:
      print("os is not linx")
