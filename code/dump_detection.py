import os
import subprocess
import time
import psutil

CORE_DUMP_FILENAME = "core"

def get_nginx_conf_path():
    nginx_path = subprocess.getstatusoutput('which nginx')[1]
    conf_path = ""

    match nginx_path:
        case "/usr/sbin/nginx":
            conf_path = "/etc/nginx/nginx.conf"
        case _:
            conf_path = "."

    return conf_path

def get_dump_path():
    conf_path = get_nginx_conf_path()
    with open(conf_path, "r") as file:
        for line in file:
            line = line.split("#", 1)[0].strip()
            if line.startswith("working_directory"):
                return line.split(None, 1)[1].rstrip(";")
    print("Core Dump generation is not enabled in the conf file")
    return None

def locate_dump(dump_path, dump_name):
    if os.path.exists(os.path.join(dump_path,dump_name)):
        print("Core Dump found")
        return True
    else:
        print("Core Dump not found")
        return False

def periodic_scan(dump_path):
    dump_found = False

    while not dump_found:
        dump_found = locate_dump(dump_path, CORE_DUMP_FILENAME)
        time.sleep(5)

def get_master_pid():
    while True:
        try:
            pids = subprocess.getstatusoutput("pidof nignx")[1]
            master_pid = int(pids.split(" ")[0])
            return master_pid
        except:
            print("NGINX is not running. Will try searching again...")
            time.sleep(5)


def event_based_check():
    master_pid = get_master_pid()
    print(f"Monitoring NGINX (Master Process: {master_pid})")
    
    nginx_process = psutil.Process(master_pid)
    while nginx_process.is_running():
        time.sleep(1)
    print("NGINX has crashed")

    dump_path = get_dump_path()

    if locate_dump(dump_path, CORE_DUMP_FILENAME):
        pass



if __name__ == '__main__':
    
    dump_path = get_dump_path()
    periodic_scan(dump_path)
    print("Dump found")
    