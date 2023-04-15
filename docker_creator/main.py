import argparse

import boto3
import docker
from docker.types import LogConfig


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", dest="docker_image", type=str, help="Name of Docker image.")
    parser.add_argument("--bash-command", dest="bash_command", type=str,
                        help="A bash command that runs inside a Docker image.")
    parser.add_argument("--aws-cloudwatch-group", dest="aws_group", type=str, help="A name of an AWS CloudWatch group")
    parser.add_argument("--aws-cloudwatch-stream", dest="aws_stream", type=str,
                        help="A name of an AWS CloudWatch stream")
    parser.add_argument("--aws-access-key-id", dest="key_id", type=str, help="AWS access key ID")
    parser.add_argument("--aws-secret-access-key", dest="access_key", type=str, help="AWS secret access key")
    parser.add_argument("--aws-region", dest="region", type=str, help="A name of an AWS region")
    return parser.parse_args()


def create_aws_client(aws_access_key_id, aws_secret_access_key, aws_region):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    return session.client("docker_creator_logs")


def set_up_docker_container(args):
    client = docker.from_env()
    log_config = LogConfig(
        type="awslogs",
        config={
            "awslogs-region": args.region,
            "awslogs-group": args.aws_group,
            "awslogs-stream": args.aws_stream,
            "awslogs-create-group": "true",
            "awslogs-multiline-pattern": "{timestamp_format} {log_level_pattern}"
        }
    )

    container = client.containers.run(
        args.docker_image,
        args.bash_command,
        detach=True,
        log_config=log_config
    )

    return container.logs(stream=True, follow=True)


def main():
    args = get_args()
    aws_client = create_aws_client(
        aws_access_key_id=args.key_id,
        aws_secret_access_key=args.access_key,
        aws_region=args.region
    )
    log_events = set_up_docker_container(args=args)

    for log_event in log_events:
        response = aws_client.put_log_events(
            logGroupName=args.aws_group,
            logStreamName=args.aws_stream,
            logEvents=[
                {
                    "timestamp": int(log_event.attrs["timestamp"]),
                    "message": log_event.decode("utf-8").strip()
                }
            ]
        )


if __name__ == "__main__":
    main()
