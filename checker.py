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
import platform
from getpass import getpass
import pickle


def run_checker():
    # Find what OS this script is running on
    os_sys = platform.system()
    if os_sys == 'Windows':
        file_path = "hbchecker.txt"
        cookies_path = "hbchecker_cookies.pkl"
    elif os_sys == 'Linux':
        file_path = "/etc/hbchecker.txt"
        cookies_path = "/etc/hbchecker_cookies.pkl"
    elif os_sys == 'Darwin':
        file_path = "hbchecker.txt"
        cookies_path = "/etc/hbchecker_cookies.pkl"
    else:
        print("HBChecker cannot run on " + os_sys + " just yet.")
        exit(1)

    # Credentials
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
    os_sys = platform.system()

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
    if os_sys == 'Linux':
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=PATH_lin, chrome_options=options)
        print("Chrome driver found on Linux machine.")
    elif os_sys == 'Windows':
        options = Options()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=PATH_win, chrome_options=options)
        print("Chrome driver found on Windows machine")
    else:
        print("Cannot find chromedriver. Please re-run the installation script again.")
        exit(1)

    timeout = 3600

    # Navigate to the application login page
    driver.get("https://intranet.hbtn.io/auth/sign_in")

    # Tracking runtime
    start_time = datetime.now()

    # Attempt to retrieve and load cookies
    try:
        cookies = pickle.load(open(cookies_path, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://intranet.hbtn.io/")
    except:
        # Sign In
        username_text = driver.find_element_by_id("user_login")
        password_text = driver.find_element_by_id("user_password")

        # Enter Login
        print("Logging in as " + username)
        username_text.clear()
        username_text.send_keys(username)
        password_text.clear()
        password_text.send_keys(password)
        login_button = driver.find_element_by_name("commit")
        login_button.click()

        # Invalid Credentials
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'student-home'))
            WebDriverWait(driver, 10).until(element_present)
        except Exception as e:
            print("Invalid Credentials")
            os.remove(file_path)
            driver.quit()
            run_checker()
            exit(1)
    print("\nLOGIN SUCCESSFUL\n")
    driver.get(PROJ_NUM)

    # Checks if given url is a valid project
    try:
        project_page = driver.find_element_by_xpath("//article")
        project_name = project_page.find_element_by_xpath("//h1")
    except Exception as e:
        print("Tried getting URL "+PROJ_NUM)
        print(e)
        driver.quit()
        exit(1)
    try:
        print("Project selected: " + project_name.text + "\n")
    except:
        print("Could not get project name...\n")
    
    # Save Cookies for next future session
    pickle.dump(driver.get_cookies() , open(cookies_path,"wb"))
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
                            break
                    if check_task == True:
                        break
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
        button_count = -1
        print()
        
        # Checking Task
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
                    button_count += 1
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
                continue
 
            # Print the Task Name
            print("-" * max_width)
            if "advanced" in task_type:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
            else:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
            print("-" * max_width)



            check_code_button[button_count].click()

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
                        wait.until(EC.visibility_of(start_test_button[button_count]))
                        results_loaded = True
                    except KeyboardInterrupt:
                        sys.exit(1)
                    except:
                        for a in range(0, len(ascii_animation)):
                            print("Waiting for checker {}".format(ascii_animation[a]), end="\r")
                            time.sleep(0.3/len(ascii_animation))
                    counter += 1
                if results_loaded == False:
                    start_test_button[button_count].click()
            except:
                results_loaded = False

            # Setting up for popup box
            wait = WebDriverWait(driver, timeout)
            result_box = task_popup[button_count].find_element_by_class_name("result")
            req_box = result_box.find_elements_by_class_name("requirement")
            check_box = result_box.find_elements_by_class_name("code")

            # Get the first valid commit id
            if str(commit_id).isdigit():
                try:
                    commit_id = result_box.find_elements_by_tag_name("code")[0].text
                except:
                    pass
            output_length = 0
            total_temp = 0
            earned_temp = 0
            code_check_mark = "\033[5;30;42m"+"[+]"+"\033[0m"
            code_x_mark = "\033[5;30;41m"+"[-]"+"\033[0m"
            req_check_mark = "\033[5;32;40m"+"[+]"+"\033[0m"
            req_x_mark = "\033[5;31;40m"+"[-]"+"\033[0m"
            q_mark = "[?]"

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
                    output_text = "{}:{} ".format(req_box[num].text, q_mark)
                output_length += len(output_text) - 14
                if output_length > max_width:
                    print()
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
                    output_text = "{}:{} ".format(check_box[num].text, q_mark)
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
            close_button = task_popup[button_count].find_element_by_class_name('close')
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

            # Got some tasks wrong
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

            # Every check is correct
            elif earned_temp == total_temp:
                sys.stdout.write("\033[F" * (new_line_count))
                for a in range(0, new_line_count):
                    print(' ' * max_width, end='\r')
                    print()
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                if "advanced" in task_type:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
                else:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
                print("-" * max_width)

            # Unknown
            else:
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                notice = "    \033[5;30;44mUKNOWN\033[0m"
                if "advanced" in task_type:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) +"\033[5;30;45m"+task_type.upper()+"\033[0m |")
                else:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) + task_type.upper()+" |")
                print("-" * max_width)
                show_score = False

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
        if man_total == 0:
            man_score = '100.0'
        else:
            man_score = str(man_earned/man_total*100)
        if adv_total == 0:
            adv_score = '100.0'
        else:
            adv_score = str(adv_earned/adv_total*100)
        if man_total == 0 and adv_total == 0:
            total_score = '100.0'
        else:
            total_score = str((man_earned + adv_earned)/(man_total + adv_total)*100)
        if man_score == '100.0':
            man_score = '100'
        else:
            man_score = str(man_score)[:2]
        if adv_score == '100.0':
            adv_score = '100'
        else:
            adv_score = str(adv_score)[:2]
        if total_score == '100.0':
            total_score = '100'
        else:
            total_score = str(total_score)[:2]
        print("Mandatory: {}/{} => {}{}".format(man_earned, man_total, man_score,'%'))
        print("Advanced:  {}/{} => {}{}".format(adv_earned, adv_total, adv_score, '%'))
        print("Total:     {}/{} => {}{}".format(man_earned + adv_earned, man_total + adv_total, total_score, '%'))
        if commit_id != 'Not Found':
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
