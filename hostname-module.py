import boto3
#import time
#time.sleep(2)
# Replace the instance_id and command with your own values
instance_id = 'i-02f278e0ef7f2318a'
command = 'hostname'

# Create an SSM client
ssm_client = boto3.client('ssm')

# Send the command to the instance
response = ssm_client.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [command]}
)

# Get the command invocation ID
command_id = response['Command']['CommandId']

# Get the command output
output = ssm_client.get_command_invocation(
    CommandId=command_id,
    InstanceId=instance_id
)['StandardOutputContent']

# Print the output
print(output)

