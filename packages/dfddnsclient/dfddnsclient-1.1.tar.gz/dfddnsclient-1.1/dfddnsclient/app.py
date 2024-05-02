import subprocess
from flask import Flask, jsonify
import requests
import os
import schedule
import time
import sys


if len(sys.argv) != 3:
    print("Usage: python3 app.py <cname> <passkey>")
    sys.exit(1)


app = Flask(__name__)
app.secret_key = os.urandom(24)

#Parameters#######
new_ipv4 = ""
old_ipv4 = ""
cname = sys.argv[1]
passkey = sys.argv[2]
interval = 120
#####################


def get_public_ip():
    global old_ipv4, new_ipv4
    try:
        result = subprocess.run(['curl', '-4', 'ifconfig.me'], capture_output=True, text=True)
        if result.returncode == 0:
            new_ipv4 = result.stdout.strip()
            #print("running...")
            if new_ipv4 != old_ipv4:
                print("ipv4 change detected!")
                return update_dns_record()
                
    except Exception as e:
        return f"Error retrieving public IPv4: {e}"
    return new_ipv4



@app.route('/update_ip', methods=['GET'])
def update_dns_record():
    global cname, old_ipv4, new_ipv4, passkey
    url = "https://ddns.dartfox.xyz/update_ip"

    payload = {
        "cname": cname,
        "passkey": passkey,
        "new_ipv4": new_ipv4
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("ip change detected and cname records updated!")
        old_ipv4 = new_ipv4
        return response.text
    else:
        print(response.text)
    
# Function to perform IP check
schedule.every(interval).seconds.do(get_public_ip)

# Function to start scheduling
@app.route('/start', methods=['GET'])
def start_scheduling():
    global scheduling_running
    if not scheduling_running:
        scheduling_running = True
        print("Scheduling started...")
        while scheduling_running:
            schedule.run_pending()
            time.sleep(30)
        return jsonify({"message":"Scheduling started successfully."}), 200
    else:
        print("Scheduling is already running.")
        return jsonify({"message":"Scheduling is already running."}), 200


scheduling_running = False
start_scheduling()
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3030)
