import boto3

aws_mag_con_new = boto3.session.Session(region_name="ap-south-1")
aws_ssm_con_new = aws_mag_con_new.client('ssm', region_name="ap-south-1")
aws_ec2_con_new = aws_mag_con_new.client('ec2', region_name="ap-south-1")
aws_s3_con=aws_mag_con_new.client("s3")
import boto3
import paramiko
public_ip_list=[]

# Create EC2 client
ec2 = boto3.client('ec2')

response=ec2.describe_instances()
for each_item in response['Reservations']:
    for each_instances in each_item['Instances']:
        #print(each_instances["PublicIpAddress"])
        public_ip_list.append(each_instances['PublicIpAddress'])
print(public_ip_list)


# Download the private key from S3
s3 = boto3.client('s3')
s3.download_file('software-ssm', 'newaccount.pem', 'newaccount.pem')
for public_ip_address in public_ip_list:
    # Connect to the instance
    key = paramiko.RSAKey.from_private_key_file('newaccount.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(public_ip_address, username='ec2-user', pkey=key)

    # Create a file in /home/ec2-user
    stdin, stdout, stderr = ssh.exec_command('touch /home/ec2-user/testfilenew.txt')
    if stderr:
        print(stderr.readlines())
    else:
        print(stdout.readlines())

    # Close the SSH connection
    ssh.close()