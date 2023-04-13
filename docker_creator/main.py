import docker

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", dest="docker_image", type=str, help="Name of Docker image.")
    parser.add_argument("--bash-command", dest="bash_command", type=str,
                        help="A bash command that runs inside a Docker image.")
    parser.add_argument("--aws-cloudwatch-group", dest="aws_group", type=str, help="A name of an AWS CloudWatch group")
    parser.add_argument("--aws-cloudwatch-stream", dest="aws_stream", type=str,
                        help="A name of an AWS CloudWatch stream")
    parser.add_argument("--aws-access-key-id", dest="kwy_id", type=str, help="AWS access key ID")
    parser.add_argument("--aws-secret-access-key", dest="access_key", type=str, help="AWS secret access key")
    parser.add_argument("--aws-region", dest="region", type=str, help="A name of an AWS region")
    return parser.parse_args()


def main():
    args = get_args()
    # create a Docker client
    client = docker.from_env()

    # create the Docker container with the specified image and command
    container = client.containers.run(args.docker_image, args.bash_command, detach=True)

    # print the container ID
    print("Container ID:", container.id)


if __name__ == "__main__":
    main()
