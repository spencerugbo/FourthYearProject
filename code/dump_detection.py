import os
import time

def get_dump_path():
    with open('nginx.conf', 'r') as file:
        for line in file:
            line = line.split('#', 1)[0].strip()
            if line.startswith('working_directory'):
                return line.split(None, 1)[1].rstrip(';')
    return None

def locate_dump(dump_path, dump_name):
    if os.path.exists(dump_path):
        return True
    else:
        return False

def periodic_scan(dump_path):
    dump_found = False

    while not dump_found:
        dump_found = locate_dump(dump_path)
        time.sleep(5)


def event_based_check():
    pass


if __name__ == '__main__':
    
    dump_path = get_dump_path()
    periodic_scan(dump_path)
    print("Dump found")
    