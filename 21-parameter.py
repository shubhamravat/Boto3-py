import boto3
import csv
import pandas as pd
import openpyxl

aws_mag_con=boto3.session.Session()
ssm_con_cli = aws_mag_con.client("ssm")


# Read the Excel file into a pandas dataframe2
df = pd.read_excel('parameter_values.xlsx')

# Write the dataframe to a CSV file
df.to_csv('parameter_values.csv', index=False)


# Open the CSV file
with open('parameter_values.csv', 'r') as file:
    reader = csv.reader(file)

    # Loop through each row in the CSV file
    for row in reader:
        # Get the parameter name and value from the CSV file
        parameter_name = row[0]
        parameter_value = row[1]
        parameter_str_type=row[2]
        if parameter_str_type=='String':
            # Update the parameter value in AWS Parameter Store
            response = ssm_con_cli.put_parameter(
                Name=parameter_name,
                Value=parameter_value,
                Type='String',
                Overwrite=True)
            print(f"Updated parameter '{parameter_name}' to value '{parameter_value}'")
        
        elif parameter_str_type=="SecureString":
            response = ssm_con_cli.put_parameter(
                Name=parameter_name,
                Value=parameter_value,
                Type='SecureString',
                KeyId="alias/SSM-Encryption-Key",
                Overwrite=True
            )
            response_key=ssm_con_cli.describe_parameters()["Parameters"]
            for item in response_key:
                if  item['Type'] =='SecureString':
                    print(f"Updated parameter '{parameter_name}' with value '{parameter_value}' and it is having keyID '{item['KeyId']}'")
    
    


