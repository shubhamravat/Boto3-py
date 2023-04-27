import boto3
import paramiko
import winrm
import requests_ntlm
import requests
import os
import time
import subprocess
import base64

wind_private_ip_list=[]
linux_private_ip_list=[]

def install_ssm_windows(wind_private_ip_list , s3):
    session = requests.Session()
    s3.download_file('software-ssm', 'AmazonSSMAgentSetup.exe', '/tmp/AmazonSSMAgentSetup.exe')
    s3.download_file('software-ssm', 'newaccount.pem', '/tmp/newaccount.pem')
    #with open('/tmp/newaccount.pem','rb') as f:
     #   cert_pem=f.read()
      #  bytes_data=base64.b64decode(cert_pem)
    for wind_ip_list in set(wind_private_ip_list):
        s = winrm.Session(wind_ip_list, auth=('Administrator','Cloud@12345'), transport='ntlm', server_cert_validation='ignore', operation_timeout_sec=500, read_timeout_sec=800)
        try:
            # Check SSM status
            r=s.run_cmd('powershell.exe' , ['-Command' , '(Get-Service AmazonSSMAgent -ErrorAction SilentlyContinue).Status'])
            #print(r)
            output_str = r.std_out.decode()  # Convert bytes object to string
            running_keyword = output_str  # Extract the "Running" keyword
            #print(running_keyword)  # Output: "Running"
            time.sleep(2)
            if 'Running' in running_keyword:
                print(f"SSM already installed on {wind_ip_list}")
                continue
            else:
                # Install SSM
                #s = winrm.Session(wind_ip_list, auth=('Administrator','Cloud@12345'), transport='ntlm', server_cert_validation='ignore', operation_timeout_sec=500, read_timeout_sec=800)
                s.run_cmd('powershell.exe', ['-Command', 'aws s3 cp s3://software-ssm/AmazonSSMAgentSetup.exe C:/'])
                time.sleep(5)
                s.run_cmd('powershell.exe', ['-Command','C:/AmazonSSMAgentSetup.exe /install /quiet'])
                time.sleep(7)
                print(f"SSM installed on {wind_ip_list}")
        except Exception as e:
            print(f"Error occurred for {wind_ip_list}: {e}")
        


def install_ssm_linux(linux_private_ip_list ,s3):
    s3.download_file('software-ssm', 'newaccount.pem','/tmp/newaccount.pem')
    s3.download_file('software-ssm', 'amazon-ssm-agent.rpm','/tmp/amazon-ssm-agent.rpm')
    for private_ip_address in linux_private_ip_list:
        # Connect to the instance
        key = paramiko.RSAKey.from_private_key_file('/tmp/newaccount.pem')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(private_ip_address, username='ec2-user', pkey=key)
        
        # Check if SSM is already installed
        stdin, stdout, stderr = ssh.exec_command("sudo systemctl status amazon-ssm-agent --no-pager --plain | grep -oP '(?<=Active:\s)(\w+)'")
        output = stdout.read().decode('utf-8').strip()
        if output != "active":
            # Copy the SSM agent package to the instance
            sftp = ssh.open_sftp()
            sftp.put('/tmp/amazon-ssm-agent.rpm', '/home/ec2-user/amazon-ssm-agent.rpm')
            sftp.close()
    
            # Install and start the SSM agent
            stdin, stdout, stderr = ssh.exec_command('sudo yum install -y /home/ec2-user/amazon-ssm-agent.rpm && sudo systemctl start amazon-ssm-agent && sudo systemctl enable amazon-ssm-agent')
            if stderr:
                print(stderr.readlines())
            else:
                print(stdout.readlines())
        else:
            print(f"SSM already installed on {private_ip_address}")
    
        # Close the SSH connection
        ssh.close()


def lambda_handler(event,context):
    aws_mag_con_new = boto3.session.Session(region_name="ap-south-1")
    aws_ec2_con_new = aws_mag_con_new.client('ec2', region_name="ap-south-1")
    s3 = aws_mag_con_new.client("s3")
    private_ip_list=[]
    response=aws_ec2_con_new.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"]=="running" and instance["PlatformDetails"]=="Windows":
                wind_private_ip_list.append(instance["PrivateIpAddress"])
            else:
                linux_private_ip_list.append(instance["PrivateIpAddress"])

# Install SSM agent on Linux instances
    install_ssm_windows(wind_private_ip_list , s3 )
    install_ssm_linux(linux_private_ip_list , s3)

# Install SSM agent on Windows instances
    

    # Get a list of running instances and their private IP addresses
# Get a list of running instances and their private IP addresses