#!/usr/bin/python3
import os
from sys import argv
from getpass import getpass
import platform


os_sys = platform.system()
if os_sys == 'Windows':
    file_path = "hbchecker.txt"
elif os_sys == 'Linux':
    file_path = "/etc/hbchecker.txt"
elif os_sys == 'Darwin':
    file_path = "hbchecker.txt"
else:
    print("HBChecker cannot run on " + os_sys + " just yet.")
    exit(1)

    print()

email = "@holbertonschool.com"
credentials = []

def check_credentials():
    if os.path.isfile(file_path) is False:
        return False
    else:
        return True

def get_credentials():
    username = ''
    password = ''
    proj_num = ''
    tries = 0
    if check_credentials() == False:
        welcome = ("\nWelcome to auto project checker! Project was created so you"
                " can run the checker without clicking the 'Check code button'"
                " everytime. You have the option to enter your holberton crede"
                "ntials which will be saved in '/etc/hbchecker.txt'. As long as "
                "this file exists, you should be good to go running this script."
                " prompted.\n\nType 'man hbchecker' or 'man push' for more information.")
        print(welcome)

        username = input("Holberton email: ")
        while email not in username and tries <= 2:
            print("Email not recognized, try again")
            username = input("Holberton email: ")
            tries += 1
        if email not in username:
            print("Exiting script, email did not end in '@holbertonschool.com'.")
            return 1
        password = getpass("Password: ")
        
        # Check argv for proj num
        for index in range(1, len(argv)):
            if argv[index].isdecimal():
                proj_num = argv[index]
        if proj_num == '':
            proj_num = input("Project URL or number: ")
            while proj_num == '' and 'https://intranet.hbtn.io/projects/' not in proj_num and\
                  'http://intranet.hbtn.io/projects/' not in proj_num or\
                  not proj_num.isdecimal():
                print(proj_num)
                print("Ex: 'http://intranet.hbtn.io/projects/212' or '212'")
                proj_num = input("Project URL or number: ")
        if proj_num.isdecimal():
            proj_num = 'http://intranet.hbtn.io/projects/' + proj_num
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(username + '\n' + password + '\n' + proj_num)
        print("Credentials saved to file!")
        credentials.append(username)
        credentials.append(password)
        credentials.append(proj_num)
        return credentials
    else:
        # Parse throught hbchecker.txt to get credentials
        with open(file_path, mode='r', encoding='utf-8') as openfile:
            read = openfile.read().splitlines()
            try:
                if email not in read[0]:
                    username = input("Holberton email: ")
                    while email not in username and tries <= 2:
                        print("Email not recognized, try again")
                        username = input("Holberton email: ")
                        tries += 1
                    if email not in username:
                        print("Exiting script, email did not end in '@holbertonschool.com'.")
                        return 1
                else:
                    username = read[0]
                if read[1] == '':
                    password = getpass("Password: ")
                else:
                    password = read[1]
                proj_num = read[2]
                for index in range(1, len(argv)):
                    if argv[index].isdecimal():
                        proj_num = argv[index]
                        print("proj_num changed: "+proj_num)
                if proj_num != '' and 'https://intranet.hbtn.io/projects/' not in proj_num and\
                   'http://intranet.hbtn.io/projects/' not in proj_num and\
                   not proj_num.isdecimal():
                    proj_num = input("Project URL or number: ")
                    while proj_num == '' and 'https://intranet.hbtn.io/projects/' not in proj_num and\
                          'http://intranet.hbtn.io/projects/' not in proj_num or\
                          not proj_num.isdecimal():
                        print(proj_num)
                        print("Ex: 'http://intranet.hbtn.io/projects/212' or '212'")
                        proj_num = input("Project URL or number: ")
                if proj_num.isdecimal():
                    proj_num = 'http://intranet.hbtn.io/projects/' + proj_num
                with open(file_path, mode='w', encoding='utf-8') as f:
                    f.write(username + '\n' + password + '\n' + proj_num)
                print("Credentials loaded from saved file")
                credentials.append(username)
                credentials.append(password)
                credentials.append(proj_num)
                return credentials
            except:
                os.remove(file_path)
                print("File not formatted correctly, removing and starting fresh again.")
                return 2
    print("File not formatted correctly, removing and starting fresh again.")
    return 2

def get_flags():
    flag_dict = {'check_every_task': False, 'check_files_changed': False}
    for index in range(1, len(argv)):
        if "-" in argv[index]:
            for l_idx in range(0, len(argv[index])):
                if "e" in argv[index][l_idx]:
                    flag_dict['check_every_task'] = True
                if "f" in argv[index][l_idx]:
                    flag_dict['check_files_changed'] = True
    return flag_dict

def get_files_changed():
    """Gets which files were changed"""
    files_list = []
    test = os.popen('git show --name-only')
    repo_location = os.popen('git rev-parse --show-toplevel')
    repo_location = repo_location.readlines()
    repo_location = repo_location[0]
    repo_location = repo_location.replace('\n', '')
    if "Not a git repository" in repo_location:
        files_list.append("Not a git repository")
        return files_list
    files_list.append(repo_location.split('/')[-1])
    output = test.readlines()
    for a in range(6, len(output)):
        files_list.append(output[a].replace('\n', ''))
    return files_list
