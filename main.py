import os


def main():
    """Execute the command lines and upload to docker server and run containers"""
    os.system('sudo docker compose build')
    os.system('sudo docker compose up -d')

main()