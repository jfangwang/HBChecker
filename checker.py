#!/usr/bin/python3
import os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import datetime
from helper_functions import *
import time
from getpass import getpass


def run_checker():
    # Credentials
    file_path = "/etc/hbchecker.txt"
    credentials = get_credentials()
    if credentials == 1:
        exit(1)
    elif credentials == 2:
        exit(1)
    else:
        username = credentials[0]
        password = credentials[1]
        PROJ_NUM = credentials[2]
    # print("username: "+username+"\npassword: "+password+"\nproj_num: "+PROJ_NUM)
    # exit(1)

    # get the path of ChromeDriverServer
    # Pathing on windows
    PATH_win = os.getcwd() + '\\chromedriver.exe'
    #Pathing on Linux
    PATH_lin = '/usr/local/bin/chromedriver'
    # Fetch Saved Project Number
    pre_url = "https://intranet.hbtn.io/projects/"
    pre_url2 = "http://intranet.hbtn.io/projects/"
    check_every_task = False
    check_files_changed = False
    os_sys = "idk"

    # Flags to run
    flags_dict = get_flags()
    check_every_task = flags_dict['check_every_task']
    check_files_changed = flags_dict['check_files_changed']
    if check_every_task == True:
        print("-e flag: Checking every task with the checker")
    if check_files_changed == True and check_every_task == False:
        print("-f flag: Only checking tasks contiaining files you changed")
    if check_files_changed == True and check_every_task == True:
        print("-f flag overriden by -e flag, still checking every task")
    HOME = "https://intranet.hbtn.io/"
    URL = PROJ_NUM
    # create a new Chrome session
    # driver = webdriver.Chrome(executable_path=PATH_lin, chrome_options=options)
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=PATH_lin, chrome_options=options)
        print("Chrome driver found on Linux machine.")
        os_sys = 'lin'
    except:
        try:
            options = Options()
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=PATH_win, chrome_options=options)
            print("Chrome driver found on Windows machine")
            os_sys = 'win'
        except:
            print("Check if chromedriver or chromedriver.exe is in this directory")
            exit(1)

    # Navigate to the application login page
    driver.get("https://intranet.hbtn.io/auth/sign_in")

    # Sign In
    username_text = driver.find_element_by_id("user_login")
    password_text = driver.find_element_by_id("user_password")

    # Tracking runtime
    start_time = datetime.now()

    # Enter Login
    print("Attempting to login as " + username)
    username_text.clear()
    username_text.send_keys(username)
    password_text.clear()
    password_text.send_keys(password)
    login_button = driver.find_element_by_name("commit")
    login_button.click()
    timeout = 3600

    # Invalid Credentials
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'student-home'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Invalid Credentials")
        os.remove(file_path)
        # Make function to request new login info
        driver.quit()
        run_checker()
        exit(1)

    print("\nLOGIN SUCCESSFUL\n")
    driver.get(URL)

    # Checks if given url is a valid project
    try:
        project_page = driver.find_element_by_xpath("//article")
        project_name = project_page.find_element_by_xpath("//h1")
    except:
        print("Project " + PROJ_NUM + " is not a project")
        driver.quit()
        exit(1)
    try:
        print("Project selected: " + project_name.text + "\n")
    except:
        print("Could not get project name...\n")

    # Setting up locators for selenium
    check_code_button = driver.find_elements_by_xpath("//button[contains(text(),'Check your code')]")
    task_popup = driver.find_elements_by_class_name("task_correction_modal")
    task_box = driver.find_elements_by_class_name("task-card")
    start_test_button = driver.find_elements_by_xpath("//button[contains(text(),'Start a new test')]")
    wait = WebDriverWait(driver, timeout)
    before_tests_time = datetime.now()
    login_time = before_tests_time - start_time
    clicked_check_code_button = 0
    button_count = 0

    # Check if tasks can check code, start test, and close the task.
    if len(check_code_button) == len(task_popup) == len(start_test_button) and len(check_code_button) > 0:
        # Click every task and check results
        for count in range(0, len(start_test_button)):
            task_name = task_box[count].find_element_by_class_name("panel-title").text
            files_needed = task_box[count].find_element_by_class_name("list-group-item")
            files_required = files_needed.find_elements_by_tag_name('li')
            git_repo = "idk"
            git_dir = "idk"
            git_files = []
            temp = []
            check_task = False
            # Gets the repo, dir, and files required for the task
            for a in files_required:
                if 'GitHub repository' in a.text:
                    git_repo = a.text.replace('GitHub repository: ', '')
                if 'Directory' in a.text:
                    git_dir = a.text.replace('Directory: ', '')
                if 'File' in a.text:
                    temp = a.text.replace('File: ', '').split(",")
                    for a in temp:
                        git_files.append(a.replace(' ', ''))

            # Checks if task box has a check code button
            button_list = task_box[count].find_elements_by_tag_name("button")
            has_check_code_button = False
            task_completed = False
            for item in button_list:
                if "Check your code" in item.text:
                    has_check_code_button = True
                    button_count += 1
            
            # f Flag enabled: Run the test if user's file has been changed
            # in this task.
            if check_files_changed == True:
                for user_files in get_files_changed()[1:]:
                    for req_files in git_files:
                        if req_files in user_files:
                            check_task = True
                if check_task == False and check_every_task == False:
                    continue
            
            # Don't start test if already completed
            if "Done" in button_list[0].text and\
               "yes" in button_list[0].get_attribute("class") and\
               check_every_task == False and check_task == False:
                continue
            if has_check_code_button:
                button_count = button_count - 1
                button_list = task_box[button_count].find_elements_by_tag_name("button")
                check_code_button[button_count].click()
                clicked_check_code_button += 1
                wait.until(EC.visibility_of(start_test_button[button_count]))
                start_test_button[button_count].click()
                close_button = task_popup[button_count].find_element_by_class_name('close')
                close_button.click()
                wait.until(EC.invisibility_of_element(close_button))
                b = "Starting tests [." + "." * count + " " * (len(task_popup) - count - 1) + "]"
                print(b, end="\r")
                button_count = button_count + 1
        print("\nClicked {:s} buttons".format(str(clicked_check_code_button)))

        # Setting up important variables
        task_type = "mandatory"
        man_total = 0
        man_earned = 0
        adv_total = 0
        adv_earned = 0
        commit_id = 0
        col, row = os.get_terminal_size()
        max_width = col
        count = 0
        show_score = True
        avg_task_time = []
        print()
        
        for task_count in range(0, len(task_box)):
            new_line_count = 0
            output_length = 0
            results_loaded = True
            task_name = task_box[task_count].find_element_by_class_name("panel-title").text
            task_type = task_box[task_count].find_element_by_class_name("label").text
            files_needed = task_box[task_count].find_element_by_class_name("list-group-item")
            files_required = files_needed.find_elements_by_tag_name('li')
            start_task_time = datetime.now()
            git_repo = "idk"
            git_dir = "idk"
            git_files = []
            temp = []
            check_task = False

            # Gets the repo, dir, and files required for the task
            for a in files_required:
                if 'GitHub repository' in a.text:
                    git_repo = a.text.replace('GitHub repository: ', '')
                if 'Directory' in a.text:
                    git_dir = a.text.replace('Directory: ', '')
                if 'File' in a.text:
                    temp = a.text.replace('File: ', '').split(",")
                    for a in temp:
                        git_files.append(a.replace(' ', ''))

            # Checks if task box has a check code button
            button_list = task_box[task_count].find_elements_by_tag_name("button")
            has_check_code_button = False
            task_completed = False
            for item in button_list:
                if "Check your code" in item.text:
                    has_check_code_button = True
                if "Done" in button_list[0].text and "yes" in button_list[0].get_attribute("class") and check_every_task == False:
                    task_completed = True

            # Check if user's task files are recently pushed to git
            # and needs to be checked. It only accounts for spefic files, not
            # directories as of now.
            if check_files_changed == True:
                for user_files in get_files_changed()[1:]:
                    for req_files in git_files:
                        # print("req_files: " + req_files)
                        # print("user_files: " + user_files)
                        # print()
                        if req_files in user_files:
                            check_task = True
                if check_task == False and check_every_task == False:
                    continue
            
            # Skip task if task cannot check code
            if has_check_code_button == False:
                # sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                notice = "   \033[5;30;43mMANUAL QA REVIEW\033[0m"
                if "advanced" in task_type:
                    print("| " + task_name + notice + (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) +"\033[5;30;45m"+task_type.upper()+"\033[0m |")
                else:
                    print("| " + task_name + notice + (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) + task_type.upper()+" |")
                print("-" * max_width)
                continue
 
            # Don't check if task is completed
            if task_completed == True and check_task == False:
                # sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                if "advanced" in task_type:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
                else:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
                print("-" * max_width)
                try:
                    commit_id += 1
                except:
                    pass
                continue
 
            # Print the Task Name
            print("-" * max_width)
            if "advanced" in task_type:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
            else:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
            print("-" * max_width)



            check_code_button[task_count].click()

            # wait for the results to load
            try:
                # wait.until(EC.visibility_of(start_test_button[count]))
                ascii_animation = [
                    '...',
                    'o..',
                    'Oo.',
                    'oOo',
                    '.oO',
                    '..o',
                    '...'
                ]
                counter = 0
                results_loaded = False
                wait = WebDriverWait(driver, 0.7)
                while counter < timeout and results_loaded == False:
                    try:
                        wait.until(EC.visibility_of(start_test_button[task_count]))
                        results_loaded = True
                    except KeyboardInterrupt:
                        sys.exit(1)
                    except:
                        for a in range(0, len(ascii_animation)):
                            print("Waiting for checker {}".format(ascii_animation[a]), end="\r")
                            time.sleep(0.3/len(ascii_animation))
                    counter += 1
                if results_loaded == False:
                    start_test_button[task_count].click()
            except:
                results_loaded = False

            # Setting up for popup box
            wait = WebDriverWait(driver, timeout)
            result_box = task_popup[task_count].find_element_by_class_name("result")
            req_box = result_box.find_elements_by_class_name("requirement")
            check_box = result_box.find_elements_by_class_name("code")

            # Get the first valid commit id
            if task_count == commit_id:
                try:
                    commit_id = result_box.find_elements_by_tag_name("code")[0].text
                except:
                    commit_id += 1
                    pass
            output_length = 0
            total_temp = 0
            earned_temp = 0
            code_check_mark = "\033[5;30;42m"+"[+]"+"\033[0m"
            code_x_mark = "\033[5;30;41m"+"[-]"+"\033[0m"
            req_check_mark = "\033[5;32;40m"+"[+]"+"\033[0m"
            req_x_mark = "\033[5;31;40m"+"[-]"+"\033[0m"

            # Going throught each check in the task

            # Requirement Checks
            for num in range(0, len(req_box)):
                total_temp += 1
                class_names = req_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{} ".format(req_box[num].text, req_check_mark)
                elif "fail" in class_names:
                    output_text = "{}:{} ".format(req_box[num].text, req_x_mark)
                else:
                    print("unknown")
                    pass
                output_length += len(output_text) - 14
                if output_length > max_width:
                    print("\n")
                    new_line_count += 1
                    output_length = len(output_text)
                print(output_text, end='')
            # Print new line if there are any req checks
            if total_temp > 0:
                print()
                new_line_count += 1

            # Code Checks
            output_length = 0
            for num in range(0, len(check_box)):
                total_temp += 1
                class_names = check_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{} ".format(check_box[num].text, code_check_mark)
                elif "fail" in class_names:
                    output_text = "{}:{} ".format(check_box[num].text, code_x_mark)
                else:
                    print("unknown")
                    pass
                output_length += len(output_text) - 14
                if output_length > max_width:
                    print()
                    new_line_count += 1
                    output_length = len(output_text)
                print(output_text, end='')

            # Print new line if there are any code checks
            if total_temp > 0:
                print()
                new_line_count += 1

            # Close the task
            close_button = task_popup[task_count].find_element_by_class_name('close')
            wait.until(EC.visibility_of(close_button))
            close_button.click()
            end_task_time = datetime.now()
            avg_task_time.append(end_task_time - start_task_time)
            task_timer = str((end_task_time - start_task_time).total_seconds())[:-4]
            task_timer = "waited "+task_timer+" seconds"

            # Keeps count of total checks in project
            if "mandatory" in task_type:
                man_total += total_temp
                man_earned += earned_temp
            else:
                adv_total += total_temp
                adv_earned += earned_temp
            if earned_temp != total_temp:
                if "advanced" in task_type:
                    sys.stdout.write("\033[F" * (new_line_count + 2))
                    print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-len(task_timer)-6))+task_timer+"  \033[5;30;45m"+ task_type.upper()+"\033[0m |")
                else:
                    sys.stdout.write("\033[F" * (new_line_count + 2))
                    print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-len(task_timer)-6))+task_timer+"  "+task_type.upper()+" |")
                sys.stdout.write("\033[E" * (new_line_count + 2))
                print("**Missing {:d}**".format(total_temp - earned_temp))


            # If results did not load
            elif results_loaded == False:
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                notice = "    \033[5;30;44mCHECKER TOOK TOO LONG\033[0m"
                if "advanced" in task_type:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) +"\033[5;30;45m"+task_type.upper()+"\033[0m |")
                else:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) + task_type.upper()+" |")
                print("-" * max_width)
                show_score = False
            # Assume every check is correct
            else:
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                if "advanced" in task_type:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
                else:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
                print("-" * max_width)

            # Wait until task has closed
            wait.until(EC.invisibility_of_element(close_button))
            count += 1

        # Checked every task at this point

        # Print out results
        if str(commit_id).isdigit():
            commit_id = "Not Found"
        print('\n\n')
        if show_score == False:
            print("\033[5;30;44mSCORES ARE NOT COMPLETE, CHECK ONLINE FOR COMPLETE SCORE\033[0m")
        print("Mandatory: {}/{}".format(man_earned, man_total))
        print("Advanced: {}/{}".format(adv_earned, adv_total))
        print("Total: {:d}/{:d}".format(man_earned + adv_earned, man_total + adv_total))
        print("Used commit id: " + commit_id)
    # There are no check_code_buttons
    elif len(check_code_button) == 0:
        print("=============================")
        print("Checker is not out yet silly.")
        print("=============================")
    else:
        print("This script is unable to run this project.")
    end_time = datetime.now()
    check_tests_time = end_time - before_tests_time
    runtime = end_time - start_time


    print("This script ran in {} seconds. Took {}s to login, {}s to check the results".format(str(runtime.total_seconds())[:-4],
                                                                                              str(login_time.total_seconds())[:-4],
                                                                                              str(check_tests_time.total_seconds())[:-4]
                                                                                              ))
    print()
    driver.quit()
