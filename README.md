![Image of auto proj](https://i.imgur.com/WZNODKC.png)
# Welcome to HBChecker

## Current List of Pending Features Coming
- [x] Add a flag to check every task
- [x] Only check tasks that have changed files
- [x] Use cookies to speed up the login process
- [ ] Add a flag to change login credentials
- [ ] Auto update program to get the most recent changes of the master repo.
- [ ] Automatically know which project to check without knowledge of the project number.

## What is this?
This is a python selenium script to check the results of the checker. Instead of hitting the 'check code' button for every task, you just run this script once and that's it. By default, the script will only check tasks that have not been completed yet. This project is primarily built for vagrant running on ```ubuntu 16.04 LTS distro``` but could also run on PC with VSCode. The installation script only works with Linux at the moment so be warned.

## Setup for Vagrant running Ubuntu
1. Clone the repo: ```git clone https://github.com/jfangwang/HBChecker.git```
2. cd into HBChecker repo: ```cd HBChecker```
3. Everything is bundled in ```./install_me.sh``` to keep things simple. For installation, run the file by entering in ```./install_me.sh``` into terminal. Enter 'y' when prompted and usually takes 3-4 minutes to install.
4. The install file adds aliases to ~/.bashrc file so just restart the terminal or enter ```source ~/.bashrc```
5. You are done and ready to go.

## Setup for Windows 10
***Dev's Notes: Not done writing the complete guide on this but this is what we have so far. Please raise issues if we are missing anything, still working on this guide.***
1. Clone the repo: ```git clone https://github.com/jfangwang/HBChecker.git```
2. cd into HBChecker repo: ```cd HBChecker```
3. Open Windows Command Prompt.
4. Enter ```pip install selenium```. Refer to https://www.selenium.dev/documentation/en/selenium_installation/installing_selenium_libraries/ for more info. This project runs on Python.
5. ~~Install Google Chrome Driver~~ Google Chrome Driver is included in the repo
6. You should be good. From this point on, installing VSCode will be incredibly useful for running this script.

## Things you should know after installation
Near the end of the install file, the script creates two seperate aliases:
1. <b>hbchecker</b>: This is the main command that should be used when checking over projects.
2. <b>push</b>: This alias is really two commands shoved together. It runs 'git push' and then 'hbchecker -f' after the git push. The idea was to create an alternative command to show only checker results that only contained files the user pushed. They would know if their pushed changes changed the results of the checker or not

## Usage
### First run...
### On Linux
After installation, hbchecker is available as an alias command saved in ~/.bashr run. After entering ```hbchecker```, the script will prompt you to enter in your holberton email, password and project URL which will be save to a file located in ```/etc/hbchecker.txt```. If you enter incorrect credentials by mistake, HBChecker will timeout and prompt you to re-enter your credentials. This can be avoided by deleting ```/etc/hbchecker.txt``` file and start fresh again.
### On Windows
***Use VSCode and press the green play button to run the hbchecker.py file. The project has to be opened at the root directory or it will not run properly.***
Aliases do not work on Windows so you have to run ```python.exe``` and ```hbchecker.py``` together, it's just how windows works. Using VSCode will make this experience a lot easier for you, after all you just push the green play button to run code. The format of the command is ```file/path/to/python.exe file/to/hbchecker.py```.
Example for user 'qbs18': ```C:/Users/qbs18/AppData/Local/Microsoft/WindowsApps/python.exe c:/Users/qbs18/Coding/Github/HBChecker/hbchecker.py```

![Image of prompt](https://i.imgur.com/CK9VBQQ.png)
### How do I run it...
### On Linux
Just run ```hbchecker``` to run it normally. The default behavior will skip tasks that have been marked as done by the checker to reduce time.
### On Windows
***Use VSCode and press the green play button to run the hbchecker.py file. The project has to be opened at the root directory or it will not run.***
Example for user 'qbs18': ```C:/Users/qbs18/AppData/Local/Microsoft/WindowsApps/python.exe c:/Users/qbs18/Coding/Github/HBChecker/hbchecker.py```

### How do I switch projects...
### On Linux
```hbchecker [PROJECT]``` where ```[PROJECT]``` represents a url or project number.Example: ```hbchecker 212``` or ```hbchecker https://intranet.hbtn.io/projects/212```
The script will save the new project url and will not need the extra argument again.
### On Windows
***Use VSCode and press the green play button to run the hbchecker.py file. The project has to be opened at the root directory or it will not run.***
Example for user 'qbs18': ```C:/Users/qbs18/AppData/Local/Microsoft/WindowsApps/python.exe c:/Users/qbs18/Coding/Github/HBChecker/hbchecker.py 212```

### Options:
### -e
Clicks 'Start Test' button and checks the results on every task verifying your grade before the deadline.
### -f
Any files that are pushed to the project repo will be checked against the checker.  hbchecker  will  only  print  out selected  results  based off the user's latest push and know which tasks to check for. If none of the files pushed tow git are required by no task, nothing will show up.

## Common Commands
* ```push``` : Runs 'git push' and then 'hbchecker -f'.
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
| /etc/hbchecker_cookies.pkl    | Stores cookies in a binary file to reduce login time |
| setup.py    | Necessary to install all files as a module with pip locally |

## Notable Downsides vs Doing It Manually
* The login time is averaging around 5 seconds (even with cookies saved) which sucks because for some tasks it takes longer to login than to check the results manually.
* This script is really meant for Vagrant running on Ubuntu and would want full Windows and MacOS support in the future.

## Author
Jonny Wang from NHV Cohort #13
