#COMMAND LINES:

#TO upack ddns client
tar -xzvf dfddnsclient-1.2.tar.gz

#TO SET UP AND BUILD DARFOX DDNS CLIENT
cd dfddnsclient-1.2
python3 setup.py sdist

#TO ACTIVATE DARTFOX DDNS CLIENT
python3 dfddnsclient/app.py <your cname> <your pass key>
