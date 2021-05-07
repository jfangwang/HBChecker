sudo apt-get update
echo "-------------------"
echo "Installing Selenium"
echo "-------------------"
sudo apt-get -y install python3-pip
sudo pip3 install selenium

echo "------------------------------"
echo "Installing Java, Chrome-stable"
echo "------------------------------"
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update 
sudo apt-get -y install openjdk-7-jre google-chrome-stable xvfb unzip firefox
echo "-------------------"
echo "Installing Selenium"
echo "-------------------"
SELENIUM_VERSION=$(curl "https://selenium-release.storage.googleapis.com/" | perl -n -e'/.*<Key>([^>]+selenium-server-standalone[^<]+)/ && print $1')
wget "https://selenium-release.storage.googleapis.com/${SELENIUM_VERSION}" -O selenium-server-standalone.jar
sudo mv selenium-server-standalone.jar /usr/local/bin
echo "------------------------"
echo "Installing Chrome Driver"
echo "------------------------"
CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo rm chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin
export DISPLAY=:10
sudo pip3 install --upgrade --ignore-installed urllib3

echo "-----------------------"
echo "Configuring Bashrc File"
echo "-----------------------"
hbchecker=hbchecker.py:run
sudo pip3 install -e $(pwd)
echo "alias hbchecker='sudo hbchecker'" >> ~/.bashrc
echo "alias push='git push && sudo hbchecker -f'" >> ~/.bashrc
echo "----------------"
echo "Adding Man Pages"
echo "----------------"
sudo mkdir -p /usr/local/man/man1/
sudo cp hbchecker /usr/local/man/man1/hbchecker.1
sudo gzip /usr/local/man/man1/hbchecker.1
sudo rm hbchecker
sudo cp push /usr/local/man/man1/push.1
sudo gzip /usr/local/man/man1/push.1
sudo rm push
echo "------------------------------------------------------------------------------"
echo "INSTALLATION COMPLETE, RESTART TERMINAL OR RUN 'source ~/.bashrc' FOR COMMANDS"
echo "------------------------------------------------------------------------------"
