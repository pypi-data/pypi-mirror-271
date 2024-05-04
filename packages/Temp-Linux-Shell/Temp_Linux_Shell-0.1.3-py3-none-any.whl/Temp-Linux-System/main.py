import subprocess
import requests
import os
import argparse
from tqdm import tqdm
import shutil
import uuid
import socket
import sys

def main():
    tls(sys.argv[1:])

def get_latest_alpine_version():
    try:
        # Construct the URL for the latest version of Alpine Linux
        latest_version_url = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/"
        response = requests.get(latest_version_url)
        response.raise_for_status()
        # Extract the latest version number from the response content
        version = response.text.split('alpine-minirootfs-')[1].split('-x86_64.tar.gz')[0]
        return version
    except Exception as e:
        print(f"An error occurred while fetching the latest version: {e}")
        return None
def start_temp_alpine_shell(hostname, command=None, directory=None):
    try:
        if directory:
            working_directory = os.path.abspath(os.path.join(os.getcwd(), directory))
        else:
            working_directory = f"/var/tmp/alpine_temp_{uuid.uuid4().hex}"
            
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
        
        latest_version = get_latest_alpine_version()

        # Download the latest release of Alpine Linux
        print(f"\033[94mDownloading Alpine Linux version {latest_version}...\033[0m")
        download_url = f"https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-{latest_version}-x86_64.tar.gz"
        with requests.get(download_url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(f"{working_directory}/alpine.tar.gz", "wb") as file, tqdm(
                desc="Progress",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))

        # Extract the Alpine Linux filesystem
        print("\033[94mExtracting Alpine Linux filesystem...\033[0m")
        subprocess.run(["sudo", "tar", "-xzf", f"{working_directory}/alpine.tar.gz", "-C", working_directory])
        
        # Add package repositories
        print("\033[94mAdding package repositories...\033[0m")
        subprocess.run(["sudo", "sh", "-c", f"echo 'http://dl-cdn.alpinelinux.org/alpine/latest-stable/main' >> {working_directory}/etc/apk/repositories"])
        subprocess.run(["sudo", "sh", "-c", f"echo 'http://dl-cdn.alpinelinux.org/alpine/latest-stable/community' >> {working_directory}/etc/apk/repositories"])
        
        # Configure network
        print("\033[94mConfiguring network...\033[0m")
        subprocess.run(["sudo", "cp", "/etc/resolv.conf", f"{working_directory}/etc/resolv.conf"])  # Copy host's resolv.conf to chroot
        subprocess.run(["sudo", "mount", "-t", "proc", "/proc", f"{working_directory}/proc"])
        subprocess.run(["sudo", "mount", "--rbind", "/sys", f"{working_directory}/sys"])
        subprocess.run(["sudo", "mount", "--rbind", "/dev", f"{working_directory}/dev"])
        # Change the hostname
        print("\033[94mChanging hostname...\033[0m")
        subprocess.run(["sudo", "sh", "-c", f"echo '{hostname}' > {working_directory}/etc/hostname"])
        
        # Execute the specified command if provided
        if command:
            print(f"\033[94mExecuting command: {command}...\033[0m")
            subprocess.run(["sudo", "chroot", working_directory, "/bin/sh", "-c", command])
        else:
            # Print welcome message
            #ip_address = socket.gethostbyname(hostname)
            os.system("clear")
            print(f"\033[94mWelcome to the Temp Alpine Linux Shell!\033[0m")
            print(f"\033[94mYou are now in the Alpine Linux environment.\033[0m")
            print(f"\033[94m * Hostname: {hostname}\033[0m")
            #print(f"\033[94m * IP Address: {ip_address}\033[0m")
            print(f"\033[94m * Working Directory: {working_directory}\033[0m")
            print("")
            # Execute chroot command to change root directory to the extracted Alpine Linux environment
            subprocess.run(["sudo", "chroot", working_directory, "/bin/sh", "-l"])
    except FileNotFoundError:
        print("Required commands are not available. Make sure 'wget', 'tar', 'chroot', and 'bash' commands are installed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    #finally:
    #    if not persistent:
    #        # Clear the temporary directory after exiting the shell
    #        if os.path.exists(working_directory):
    #            if 
    #            shutil.rmtree(working_directory)
    #            print(f"\033[94mTemp directory cleared.\033[0m")


class tls:

    def __init__(self, name):
        parser = argparse.ArgumentParser(description="Start a temporary Alpine Linux shell")
        parser.add_argument("--hostname", "-hn", default="alpine", help="Specify the hostname for the Alpine Linux environment")
        parser.add_argument("--command", "-c", help="Command to execute in the Alpine Linux environment")
        parser.add_argument("--directory", "-d", help="Where the folder of the Shell should be")
        #parser.add_argument("--persistent", "-p", help="A Flag to make the Shell persistent. Make sure to specify a directory.", action="store_true")
        args = parser.parse_args()

        #if args.persistent and args.directory == None:
        #    print("Make sure to specify a directory.")
        #    quit()

        start_temp_alpine_shell(args.hostname, args.command, args.directory)