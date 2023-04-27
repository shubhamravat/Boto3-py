import boto3
import base64

ecr_client = boto3.client('ecr')

# Replace these with your own values
repository_name = 'catpipeline'
image_tag = 'e64a378'

image_ids = [{'imageTag': image_tag}]
response = ecr_client.batch_get_image(repositoryName=repository_name, imageIds=image_ids)
image_manifest = response['images'][0]['imageManifest']
manifest = base64.b64decode(image_manifest).decode('utf-8')
dockerfile = manifest.split('"dockerfile": "')[1].split('",')[0]
print(dockerfile)
