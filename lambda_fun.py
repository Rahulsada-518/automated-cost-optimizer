import boto3

ec2 = boto3.client("ec2")

def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    instances_to_stop = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            tags = instance.get("Tags", [])
            keep_running = False

            for tag in tags:
                if tag["Key"] == "KeepRunning" and tag["Value"] == "Yes":
                    keep_running = True

            if not keep_running:
                instances_to_stop.append(instance_id)

    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        return {
            "status": "success",
            "message": f"Stopped instances: {instances_to_stop}"
        }

    return {
        "status": "success",
        "message": "No instances to stop"
    }