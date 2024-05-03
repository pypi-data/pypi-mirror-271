import subprocess
import threading
import re
import time
import sys
from easyland.log import logger

class Daemon():

    def __init__(self, config):
        self.config = config 
        listeners = self.get_listeners()
        logger.info('Starting easyland daemon')
        # self.last_event_time = time.time()
        # if 'hyprland' in watchers:
        #     hyprland_thread = threading.Thread(target=self.launch_hyprland_daemon)
        #     hyprland_thread.start()
        # if 'systemd' in watchers:
        #     systemd_thread = threading.Thread(target=self.launch_systemd_login_daemon)
        #     systemd_thread.start()
    
    def get_listeners(self):
        if hasattr(self.config, 'listeners'):
            return self.config.listeners
        else:
            logger.error('No listeners defined in the config file')
            sys.exit(1)


    def call_handler(self, handler, *argv): 
        func = getattr(self.config, handler, None)
        if callable(func):
            func(*argv)
    
    def launch_hyprland_daemon(self):
        logger.info('Launching hyprland daemon')
        cmd = "socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        while True:
            for line in iter(ps.stdout.readline, ""):
                self.last_event_time = time.time()
                decoded_line = line.decode("utf-8")
                if '>>' in decoded_line:
                    data = decoded_line.split('>>')
                    self.call_handler('on_hyprland_event', data[0], data[1])

    def launch_systemd_login_daemon(self):
        logger.info('Launching systemd daemon')
        cmd = "gdbus monitor --system --dest org.freedesktop.login1"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        while True:
            for line in iter(ps.stdout.readline, ""):
                decoded_line = line.decode("utf-8").strip()
                res = re.match(r'(.+?): ([^\s]+?) \((.*?)\)$', decoded_line)
                if res:
                    sender = res.group(1)
                    name = res.group(2)
                    payload = res.group(3)

                    if 'Properties' not in name:
                        signal_name = name.split('.')[-1]
                        f = 'on_' + signal_name 
                        self.call_handler(f, payload)
                        self.call_handler('on_systemd_event', sender, signal_name, payload)
   

