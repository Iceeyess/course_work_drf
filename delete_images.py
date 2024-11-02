import os


def main():
    """Execute the command lines in order to delete containers and images"""
    os.system('sudo docker compose down')
    os.system('sudo docker rmi $(sudo docker images)')

main()