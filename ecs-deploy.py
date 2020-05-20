import boto3
import botocore
import os
import sys

def get_client(access_key_id=None, secret_access_key=None, region=None):
  session = boto3.session.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region
  )

  return session.client('ecs')

def exit_with_error(message, *args):
  print('Something went wrong:', message.format(*args), file=sys.stderr)
  sys.exit(1)

def update_service(client, cluster, service):
  client.update_service(cluster=cluster, service=service, forceNewDeployment=True)

def wait_service_stable(client, cluster, service):
  waiter = client.get_waiter('services_stable')
  waiter.wait(cluster=cluster, services=[service], WaiterConfig={'Delay': 15, 'MaxAttempts': 40})


def deploy_service():
  access_key_id = os.getenv('PLUGIN_ACCESS_KEY_ID')
  secret_access_key = os.getenv('PLUGIN_SECRET_ACCESS_KEY')
  region = os.getenv('PLUGIN_REGION')
  cluster = os.getenv('PLUGIN_CLUSTER')
  service = os.getenv('PLUGIN_SERVICE')

  client = get_client(access_key_id, secret_access_key, region)

  try:
    print('Updating service "{0}" on cluster "{1}"...'.format(service, cluster))
    update_service(client, cluster, service)

    print('Service updated. Waiting for service to be stable...')
    wait_service_stable(client, cluster, service)

    print('Service is stable now. All done.')

  except client.exceptions.ClusterNotFoundException:
    exit_with_error('The cluster "{0}" does not exist.', cluster)

  except client.exceptions.ServiceNotFoundException:
    exit_with_error('The service "{0}" does not exist on cluster "{1}".', service, cluster)

  except botocore.exceptions.WaiterError as error:
    exit_with_error('Cannot confirm service stability. {0}.', error)

if __name__ == '__main__':
  deploy_service()
