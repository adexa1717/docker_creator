import docker

import argparse


def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", dest="docker_image", type=str, help="Name of Docker image.")
    parser.add_argument("--bash-command", dest="bash_command", type=str, help="A bash command that runs inside a Docker image.")
    args = parser.parse_args()


    # create a Docker client
    client = docker.from_env()

    # create the Docker container with the specified image and command
    container = client.containers.run(args.docker_image, args.bash_command, detach=True)

    # print the container ID
    print("Container ID:", container.id)

    # print the container ID
    print("bash_command:", args.bash_command)

    # print the container ID
    print("docker_image:", args.docker_image)


if __name__ == "__main__":
    main()

