from libs.Log import logger
# from libs.Config import Config

# class Main(Config):


listeners = ['hyprland', 'systemd_logind', 'idle']
logger.info('test')
def idle_config():
    return [
        # [2, ['ls'], ['ls /tmp']],
        # [10, ['ls'], ['ls /tmp']],
        [150, ['brightnessctl -s set 0'], ['brightnessctl -r']],
        [600, ['pidof hyprlock || hyprlock']],
        [720, ['hyprctl dispatch dpms off'], ['hyprctl dispatch dpms on']]
    ]

#
# This callback is called when an hyprland IPC event is received
#
# def on_hyprland_event(event, argument):
#     if event in [ "monitoradded", "monitorremoved" ]:
#         logger.info('Handling hyprland event: ' + event)
#         self.set_monitors()

#
# This callback is called when the Systemd event PrepareForSleep is received 
##
#def on_PrepareForSleep(payload):
#    if 'true' in payload:
#        logger.info("Locking the screen before suspend")
        # self.command.shell_command("hyprlock")

#
# Method to set monitors
#
# def set_monitors():
#     logger.info('Setting monitors')
#     if self.command.get_monitor(description="HP 22es") is not None:
#         self.command.hyprctl_command('keyword monitor "eDP-1,disable"')
#     else:
#         self.command.hyprctl_command('keyword monitor "eDP-1,preferred,auto,2"')
#         self.command.shell_command("brightnessctl -s set 0")
