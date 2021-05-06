![Image of auto proj](https://i.imgur.com/WZNODKC.png)
# Welcome to HBChecker
## What is this?
This is a python selenium script to check the results of the checker. Instead of hitting the 'check code' button for every task, you just run this script once and that's it. This project is primarily built for vagrant running on ```ubuntu 16.04 LTS distro``` but could also run on PC with VSCode with a little tinkering.
## Setup for Vagrant running Ubuntu
1. Clone the repo: ```git clone https://github.com/jfangwang/HBChecker.git```
2. cd into HBChecker repo: ```cd HBChecker```
3. Everything is bundled in ```selenium_install.sh``` to keep things simple. For installation, run the file by entering in ```./install_me.sh``` into terminal. Enter 'y' when prompted and usually takes 3-4 minutes to install.
4. The install file adds aliases to ~/.bashrc file so just restart the terminal or enter ```source ~/.bashrc```
5. You are done and ready to go.

## Usage
### First run
After installation, hbchecker is available as an alias command saved in ~/.bashr run. After entering ```hbchecker```, the script will prompt you to enter in your holberton email, password and project URL which will be save to a file located in ```/etc/hbchecker.txt```. If you enter incorrect credentials by mistake, HBChecker will timeout and prompt you to re-enter your credentials. This can be avoided by deleting ```/etc/hbchecker.txt``` file and start fresh again.

![Image of prompt](https://i.imgur.com/CK9VBQQ.png)
### How do I run it?
Just run ```hbchecker``` to run it normally. The default behavior will skip tasks that have been marked as done by the checker to reduce time.        
### How do I switch projects?
```hbchecker [PROJECT]``` where ```[PROJECT]``` represents a url or project number.Example: ```hbchecker 212``` or ```hbchecker https://intranet.hbtn.io/projects/212```
The script will save the new project url and will not need the extra argument again.

### Options:
### -e
Clicks 'Start Test' button and checks the results on every task verifying your grade before the deadline.
### -f
Any files that are pushed to the project repo will be checked against the checker.  hbchecker  will  only  print  out selected  results  based off the user's latest push and know which tasks to check for. If none of the files pushed tow git are required by no task, nothing will show up.

## Common Commands
* ```hbchecker -e 212``` or ```hbchecker 212 -e``` : Check every task in the 0x00. C - Hello, World project.
* ```hbchecker``` : Check the results of whatever project url is saved. If no project url exists, it will prompt you to enter one in.
* ```hbchecker -f 212``` :  Any files that are pushed to the project repo will be checked against the checker.  hbchecker  will  only  print  out selected  results  based off the user's latest push and know which tasks to check for. If none of the files pushed to git are required by no task, nothing will show up.

## Contributing
Feel free to make a pull request, raise any git issues and will be updated accordingly.

## Files

| File          | Description   |
| ------------- |:-------------:|
| checker.py    | Checks the checker with selenium     |
| chromedriver.exe      | chromedriver for windows     |
| hbchecker.py     | Main entry point for running script    |
| helper_functions.py     | Helper functions for getting information    |
| install_me.sh      | Installs all required packages for this project   |
| /etc/hbchecker.txt      | File containing credentials to your login |
| setup.py    | Necessary to install all files as a module with pip locally |

## Pending List of Features Coming
* Add a flag to change login credentials
* Automatically know which project to check for without knowledge of the project number.

## Author
Jonny Wang from NHV Cohort #13
