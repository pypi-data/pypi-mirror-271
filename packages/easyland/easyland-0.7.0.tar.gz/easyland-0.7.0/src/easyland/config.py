import easyland.command as Command 
import easyland.daemon as Daemon
import easyland.idle as Idle
from easyland.log import logger

class Config:
    def __init__(self):
        self.timeouts = [] 
        # if callable(getattr(self, 'set_idle_config', None)):
        #     self.set_idle_config()

        # self.current_timeout_commands = []
        # self.current_resume_commands = []

        self.command = Command.Command()
        self.daemon = Daemon.Daemon(self, ['hyprland', 'idle', 'systemd'])
        self.setup_idle()
    
    def setup_idle(self):
        if callable(getattr(self, 'idle_config', None)):
           config = self.idle_config()
           idle = Idle.Idle(config)
           idle.setup()

