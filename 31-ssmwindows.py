import boto3
import paramiko
import pywinrm

# Create a new Boto3 session and clients for SSM, EC2, and S3 services
aws_mag_con_new = boto3.session.Session(region_name="ap-south-1")
aws_ssm_con_new = aws_mag_con_new.client('ssm', region_name="ap-south-1")
aws_ec2_con_new = aws_mag_con_new.client('ec2', region_name="ap-south-1")
aws_s3_con = aws_mag_con_new.client("s3")

# Download the required files from the S3 bucket
aws_s3_con.download_file('software-ssm', 'newaccount.pem', 'newaccount.pem')
aws_s3_con.download_file('software-ssm', 'AmazonSSMAgentSetup.exe', 'AmazonSSMAgentSetup.exe')

# Initialize empty lists to store public IP addresses and platform details
public_ip_list = []
platform_list = []

# Describe all instances in the region and filter for running Windows instances
response = aws_ec2_con_new.describe_instances()
for each_item in response['Reservations']:
    for each_instance in each_item['Instances']:
        try:
            if each_instance['State']['Name'] == 'running' and each_instance['PlatformDetails'] == 'Windows':
                public_ip_list.append(each_instance['PublicIpAddress'])
                platform_list.append(each_instance['PlatformDetails'])
        except KeyError:
            pass

# Iterate over the public IP addresses of Windows instances and establish an SSH connection with each
for public_ip_address in public_ip_list:
    # Initialize an SSH client and connect to the instance
    key = paramiko.RSAKey.from_private_key_file('newaccount.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(public_ip_address, username='Administrator', pkey=key)
    
    # Execute a command to copy the Amazon SSM agent installer from the S3 bucket to the C:\ drive
    command = 'aws s3 cp s3://software-ssm/AmazonSSMAgentSetup.exe  C:\\'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    print(f'Command: {command}\nOutput: {output}\nError: {error}')

    # Close the SSH connection
    ssh.close()
