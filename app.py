from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from requests import get
import os,subprocess
from subprocess import Popen, PIPE
import pwd

app = Flask(__name__)
app.secret_key = "A_skdfjPskdfkPdsgllflkdnfkljadklf"

ip = get('https://api.ipify.org').content.decode('utf8')

def makeNewFolder(newpath,user = None):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        if(user != None):
            try:
                pwd.getpwnam(user)
            except KeyError:
                os.system("useradd "+user)

def makeNewFile(file, content):
    f = open(file,"w+")
    f.write(content)
    f.close()

def decodeFolderStructure(folder_structure,location):
    for key in folder_structure.keys():
        location += "/"+key
        keyData = folder_structure[key]
        if str(type(keyData)) != "<class 'str'>" :
            makeNewFolder(location)
            decodeFolderStructure(keyData,location)
        else:
            print(key)
            makeNewFile(location,keyData)

@app.route("/")
def index():
    return ip

@app.route("/send_files_data/<user>", methods=['POST'])
def method_name(user):
    defPath = "cgi-bin/"+user
    makeNewFolder(defPath,user)
    folder_structure = request.json
    decodeFolderStructure(folder_structure,defPath)
    return defPath

@app.route("/get_files_data/<user>")
def get_fild_data(user):
    
    #Setup Files in file system
    defPath = "cgi-bin/"+user
    start_file = defPath+"/run.sh"
    assert os.path.isfile(start_file)
    
    #Setup Enviornment
    pw_record = pwd.getpwnam(user)
    my_env = os.environ.copy()
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'USER'     ]  = user_name

    #Run Subprocess
    pipe = subprocess.Popen(start_file, stdout=PIPE, timeout=15, preexec_fn=os.setuid(pw_record.pw_uid), env=my_env)
    
    #Return Standard Output of Process
    return pipe.stdout


if __name__ == '__main__':
    app.run(port="5001",debug=True)