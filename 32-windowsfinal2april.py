import boto3
import paramiko
import winrm
import requests_ntlm
import requests
import os
import time
import subprocess


def lambda_handler(event,context):
    aws_mag_con_new = boto3.session.Session(region_name="ap-south-1")
    #aws_ssm_con_new = aws_mag_con_new.client('ssm', region_name="ap-south-1")
    aws_ec2_con_new = aws_mag_con_new.client('ec2', region_name="ap-south-1")
    aws_s3_con=aws_mag_con_new.client("s3")
    ec2 = boto3.client('ec2')
    # Set up AWS credentials and create S3 client
    session = boto3.Session(region_name='ap-south-1')
    s3 = session.client('s3')
    response=aws_ec2_con_new.describe_instances()
    private_ip_list=[]
    #response=ec2.describe_instances()
    for each_item in response['Reservations']:
        for each_instances in each_item['Instances']:
            try:
                if each_instances['State']['Name'] == 'running':
                    private_ip_list.append(each_instances['PrivateIpAddress'])
            except KeyError:
                pass
    print(private_ip_list)
    
    for wind_ip_list in private_ip_list:
        session = requests.Session()
        s3.download_file('software-ssm', 'AmazonSSMAgentSetup.exe', '/tmp/AmazonSSMAgentSetup.exe')
        s3.download_file('software-ssm', 'newaccount.pem', '/tmp/newaccount.pem')
        with open('/tmp/newaccount.pem', 'r') as f:
            cert_pem = f.read()
        s = winrm.Session(wind_ip_list, auth=('Administrator','Cloud@12345'), transport='ntlm', server_cert_validation='ignore', cert_pem=cert_pem, operation_timeout_sec=500, read_timeout_sec=800)
        try:
            s.run_cmd('powershell.exe', ['-Command', 'aws s3 cp s3://software-ssm/AmazonSSMAgentSetup.exe C:/ && C:/AmazonSSMAgentSetup.exe /install /quiet'])
        except Exception as e:
            print(f"Timeout error occurred for {wind_ip_list}: {e}")
        finally:
            s = None