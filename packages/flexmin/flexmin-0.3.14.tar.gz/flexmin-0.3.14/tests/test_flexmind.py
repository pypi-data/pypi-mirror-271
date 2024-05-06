debug = None
import shlex, subprocess, os, yaml, re, getpass, xmlrpc.client, shutil, time, datetime, uuid
import traceback
from utils import output_prep
from base64 import decodestring


#modroot = os.path.join(request.folder,"modules")
script = 'No script specified'
script_type = None

script = "sys_diskusage.sh"

# run script
service = xmlrpc.client.Server('http://localhost:8000') 

if service.taskClear():
    print("Flexmin service clear of historical tasks, ready to go.")
else:
    print("Flexmin service still has old tasks, aborting.")
    exit()

params = {}
out = ""
output = None
err = ""
mod = None
task_auth = dict()
fm_vars = dict()

task_session = str(uuid.uuid4())
print("Session ID: " + task_session)
task_auth['session_id'] = task_session
task_auth['username'] = 'flexmin'
task_auth['password'] = 'password'
task_auth['client_ip'] = 'localhost'

validLabels = 'Title|Author|Date|Version|Description|Requirements|Usage|Note|Task|ToDo'
# regular expression to find labels and their values (if on same line)
# comment text is 1st group (e.g. REM or #), label text is 2nd group, value is 3rd.
validComments = 'REM|echo|#'
strInfo = '^(' + validComments + ')\s([\s\w]+.*)'
reInfo = re.compile(strInfo,re.IGNORECASE)
reTags = re.compile('^\s+tags:\s([\s\w,]+)')


print("Scripts Available Here:")
infoLines = ["tasks:"]
scripts = service.getScripts()
for s in scripts:
    infoLines.append("  - script: " + os.path.basename(s))
    infoDone = False
    tags = None
    with open(s) as f:
        for line in f:
            e = reInfo.search(line)
            if e:
                infoLines.append("    " + e.group(2))
            else:
                if line.strip() == "":
                    break # empty line ends this loopout = service.getScripts()
print("\n".join(infoLines))
print("")

print("Run short test script:")
fm_vars['FM_TASKID'] = 1
out = service.runyaml("test_task.sh", fm_vars, task_auth)
print(out)
print("")

print("Test flexmin variables:")
fm_vars['FM_TASKID'] = 2
out = service.runyaml("test_variables.sh", fm_vars, task_auth)
print(out)
print("")

print("Test flexmin variables:")
fm_vars['FM_TASKID'] = 3
out = service.runyaml("test_variables.py", fm_vars, task_auth)
print(out)
print("")

print("Run long running test:")
taskid = 4
fm_vars['FM_TASKID'] = taskid
out = service.runyaml("test_longtask.sh 4 localhost", fm_vars, task_auth)
output = yaml.load(out)
if 'task' in output and 'line' in output['task']:
    line = output['task']['line']
    print(out)
    done = False
    while not done:
        done = service.completed(taskid)
        state, lines = service.stateUpdate(taskid,line)
        if not done:
            if state: print("\n".join(state))
            time.sleep(0.25)
            line = lines
print("")

print("Show text file input via parameter file:")
fm_vars['FM_TASKID'] = 5
text = """
This is a multiple line text
Line 2
Line 3
etc
"""
service.writeTaskDataFile(5, "test_longdata.sh", 1, 'w', text)
out = service.runyaml("test_longdata.sh file", fm_vars, task_auth)
print(out)
print("")

print("Service Task List")
print(service.tasklist())
