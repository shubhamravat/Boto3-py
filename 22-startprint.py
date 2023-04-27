import boto3
import csv
import pandas as pd
import openpyxl

aws_mag_con=boto3.session.Session()
ssm_con_cli = aws_mag_con.client("ssm")
parameter_name="/mpro/ecs-parametervaluenew"
parameter_value="786#$"

response = ssm_con_cli.describe_parameters(
#Name=parameter_name,
##Value=parameter_value,
#Type='SecureString',
#Overwrite=True
            )

#print(response)

response1=ssm_con_cli.put_parameter(
    Name=parameter_name,
Value=parameter_value,
Type='SecureString',
KeyId="alias/SSM-Encryption-Key",
Overwrite=True
)
response_key=ssm_con_cli.describe_parameters()["Parameters"]
for item in response_key:
        if  item['Type'] =='SecureString':
            print(item['KeyId'])
            print(f"Updated parameter '{parameter_name}' with value '{parameter_value}' and it is having keyID '{item['KeyId']}'")
    