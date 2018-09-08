"""My qtile config file.

TODO:
- [X] problem somewhere: firefox spawns in 'main' instead of 'main2'
      reason was qtile.cmd_restart() on screen change at first startup.
      For now disabled.
- [ ] DropDowns first appearance are not at the right size
- [ ] test/validate multiscreen configs
"""
import asyncio
from glob import glob
import os
from os.path import expanduser
import random
import re
import socket
import subprocess
import time

from libqtile.config import Key, Screen, Group, ScratchPad, DropDown, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger

from widget.vpn_checker import ConnectionStatus

# ==== qtile parameters
wmname = "LG3D"  # java hack
mod = "mod4"

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
# ==== end qtile params

# ==== local params
# global var used to keep last window object in order to restore its transparency
# when it will loose the focus:
last_focus = None
# first start flag
first_start = True

home_path = expanduser("~")
# ==== end local params


# ==== Config
groups = [ScratchPad("scratchpad", [
              # define a drop down terminal.
              # it is placed in the upper third of screen by default.
              DropDown("term", "urxvt",
                       x=0.2, y=0, width=0.6, height=0.25, opacity=0.7,
                       on_focus_lost_hide=False),
              DropDown("keys", f"urxvt -bg black -e less {home_path}/qtile_shortcuts",
                       x=0.7, y=0.1, width=0.3, height=0.8, opacity=0.7,
                       on_focus_lost_hide=False),
              ]),
          Group("main",  # 1
                layout="monadtall",
                spawn="chromium"),
          Group("main2", # 2
                layout="monadtall",
                spawn="firefox"),
          Group("term",  # 3
                layout="monadwide",
                spawn="urxvtc"),
          Group("dev1",  # 4
                layout="monadtall"),
          Group("dev2",  # 5
                layout="monadtall"),
          Group("term2", # 6
                layout="monadwide"),
          Group("7", layout="max"),
          Group("8", layout="max"),
          Group("9",
                layout="monadtall"),
          Group("10", layout="max"),

          Group("11", layout="monadtall"),
          Group("12", layout="monadtall"),
          Group("13", layout="monadwide"),
          Group("14", layout="monadwide"),
          Group("15", layout="monadwide"),
          Group("16", layout="max"),
          Group("17", layout="max"),
          Group("18", layout="max"),
          Group("19", layout="max"),
          Group("20", layout="max"),
        ]


layout_theme = dict(border_normal='#101010',
                    border_focus="#bb5F0C",
                    border_width=2)


layouts = [
    layout.MonadWide(
        margin=4,
        ratio=0.7,
        min_ratio=.10,
        max_ratio=.90,
        min_secondary_size=200,
        change_ratio=.02,
        change_size=50,
        **layout_theme),
    layout.MonadTall(
        ratio=0.7,
        min_ratio=.10,
        max_ratio=.90,
        min_secondary_size=200,
        change_ratio=.02,
        change_size=50,
        **layout_theme),
    layout.TreeTab(**layout_theme),
    layout.Max(),
    layout.Bsp(),
]


defaut_font_size = 13
defaut_bar_size = 22

widget_defaults = dict(
    font='DejaVu Sans Mono for Powerline',
    foreground="aaaaaa",
    fontsize=defaut_font_size,
    padding=1,
)


def generate_widgets():
    """generate a widget list."""
    widgets = [
        widget.GroupBox(urgent_alert_method='border',
                        urgent_border='FF0000',
                        urgent_text='FF0000',
                        fontsize=defaut_font_size,
                        borderwidth=2,
                        other_screen_border='AAAA40',
                        this_screen_border='AAAA40',
                        this_current_screen_border='FFFF40',
                        other_current_screen_border='FFFF40',
                        inactive="606060",
                        use_mouse_wheel=False,
                        disable_drag=True,),
        widget.Sep(padding=6, height_percent=60),
        widget.Prompt(),
        # widget.Notify(default_timeout=10),
        widget.TaskList(),
        widget.Sep(padding=6, height_percent=60),
        widget.Systray(padding=5),
        widget.Sep(padding=6, height_percent=60),
        # yaourt -S lm_sensors
        widget.ThermalSensor(foreground="aaaaaa",
                             foreground_alert="ee5555",
                             threshold=75,
                             tag_sensor="Package id 0",
                             update_interval=10),
        widget.Sep(padding=6, height_percent=60), ]

    widgets.extend([
        widget.Backlight(backlight_name='intel_backlight',
                         update_interval=1),
        widget.Sep(padding=6, height_percent=60),
        widget.BatteryIcon(),
        widget.Battery(),
        widget.Sep(padding=6, height_percent=60), ])

    widgets.extend([
        widget.Volume(emoji=True,
                      # yaourt -S noto-fonts-emoji
                      font="NotoColorEmoji-Regular",
                      # yaourt -S humanity-icons
                      # theme_path='/usr/share/icons/Humanity/status/22/',
                      # font='Arial',
                      update_interval=1),
        widget.Sep(padding=6, height_percent=60),
        widget.Clock(format='%a %d-%m-%Y %H:%M:%S'),
        widget.Sep(padding=6, height_percent=60), ])

    widgets.extend([
        ConnectionStatus(name="protonvpn", font="NotoColorEmoji-Regular",
                         fmt_ok="\U0001F510", fmt_nok="\U0001F513"), ])

    widgets.extend([
        widget.CurrentLayoutIcon(foreground="00eedd", scale=0.8), ])
    return widgets


screens = [
    Screen(top=bar.Bar(generate_widgets(),
                       size=defaut_bar_size,
                       opacity=0.9)),
    Screen(top=bar.Bar(generate_widgets(),
                       size=defaut_bar_size,
                       opacity=0.9)),
    Screen(top=bar.Bar(generate_widgets(),
                       size=defaut_bar_size,
                       opacity=0.9)),
    ]


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.group.next_window()),  # layout.down()),
    Key([mod, "shift"], "k", lazy.group.prev_window()),  # layout.down()),
    Key([mod], "j", lazy.group.prev_window()),  # layout.up()),
    Key([mod, "shift"], "j", lazy.group.next_window()),  # layout.up()),
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.group.next_window()),
    Key([mod, "shift"], "space", lazy.group.prev_window()),

    # == Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),  # shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),  # shuffle_up()),
    Key([mod, "shift", "control"], "k", lazy.layout.swap_left()),
    Key([mod, "shift", "control"], "j", lazy.layout.swap_right()),

    # == window resizing (most for Monadtall layout)
    Key([mod], "h", lazy.layout.grow()),
    Key([mod, "shift"], "h", lazy.layout.shrink()),
    Key([mod], "l", lazy.layout.shrink()),
    Key([mod, "shift"], "l", lazy.layout.grow()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "f", lazy.layout.flip()),
    Key([mod], "m", lazy.layout.maximize()),
    Key([mod, "control"], "m", lazy.window.toggle_minimize()),

    # == move and update up, down, left, right
    Key([mod], "s", lazy.layout.down()),
    Key([mod], "z", lazy.layout.up()),
    Key([mod], "q", lazy.layout.left()),
    Key([mod], "d", lazy.layout.right()),
    Key([mod, "shift"], "s", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "z", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "q", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "d", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "s", lazy.layout.flip_down()),
    Key([mod, "mod1"], "z", lazy.layout.flip_up()),
    Key([mod, "mod1"], "q", lazy.layout.flip_left()),
    Key([mod, "mod1"], "d", lazy.layout.flip_right()),
    Key([mod, "control"], "s", lazy.layout.grow_down()),
    Key([mod, "control"], "z", lazy.layout.grow_up()),
    Key([mod, "control"], "q", lazy.layout.grow_left()),
    Key([mod, "control"], "d", lazy.layout.grow_right()),
    #Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # == floating and maximise
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "shift"], "m", lazy.window.toggle_maximize()),

    # == opacity control
    Key([mod], "o", lazy.window.down_opacity()),
    Key([mod, "shift"], "o", lazy.window.up_opacity()),
    Key([mod, "control"], "o", lazy.window.opacity(.3)),
    Key([mod, "shift", "control"], "o", lazy.window.opacity(1)),

    # == launch terminal
    Key([mod], "Return", lazy.spawn("urxvtc")),

    # == spawns and qtile commands
    Key([mod], "r", lazy.spawncmd()),
    Key([mod, "shift"], "r", lazy.qtilecmd()),

    Key([mod, "shift"], "c", lazy.window.kill()),

    # == Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),

    # == restart and shutdown qtile
    Key([mod, "shift", "control"], "r", lazy.restart()),
    Key([mod, "shift", "control"], "q", lazy.shutdown()),

    # == volumes
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pulseaudio-ctl up")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pulseaudio-ctl down")),
    Key([], "XF86AudioMute",
        lazy.spawn("pulseaudio-ctl mute")),
    Key([], "XF86AudioPlay",
        lazy.spawn(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify "
            "/org/mpris/MediaPlayer2 "
            "org.mpris.MediaPlayer2.Player.PlayPause")),
    Key([], "XF86AudioStop",
        lazy.spawn("pulseaudio-ctl mute-input")),
    Key([], "XF86AudioNext",
        lazy.spawn(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify "
            "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")),
    Key([], "XF86AudioPrev",
        lazy.spawn(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify "
            "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")),

    # == backlight
    # yaourt -S light-git
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("light -A 5")),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("light -U 5")),

    # == toggle screens
    Key([mod], "twosuperior", lazy.next_screen()),
    Key([mod, "shift"], "twosuperior", lazy.prev_screen()),
    Key([mod], "g", lazy.screen.togglegroup()),
    Key([mod, "shift"], "g", lazy.switchgroup()),

    # == keys for groups
    Key([mod], "u", lazy.next_urgent()),
    Key([mod], "Left", lazy.screen.prev_group(skip_managed=True)),
    Key([mod], "Right", lazy.screen.next_group(skip_managed=True)),

    # keys for FR keymap, strange that "1", "2", does not work....
    # TODO: something to detect keymap and attrib the good keys automatically ?
    # "1"
    Key([mod], "ampersand", lazy.group["main"].toscreen()),
    Key([mod, "shift"], "ampersand", lazy.window.togroup("main")),
    # "2"
    Key([mod], "eacute", lazy.group["main2"].toscreen()),
    Key([mod, "shift"], "eacute", lazy.window.togroup("main2")),
    # "3"
    Key([mod], "quotedbl", lazy.group["term"].toscreen()),
    Key([mod, "shift"], "quotedbl", lazy.window.togroup("term")),
    # "4"
    Key([mod], "apostrophe", lazy.group["dev1"].toscreen()),
    Key([mod, "shift"], "apostrophe", lazy.window.togroup("dev1")),
    # "5"
    Key([mod], "parenleft", lazy.group["dev2"].toscreen()),
    Key([mod, "shift"], "parenleft", lazy.window.togroup("dev2")),
    # "6"
    Key([mod], "minus", lazy.group["term2"].toscreen()),
    Key([mod, "shift"], "minus", lazy.window.togroup("term2")),
    # "7"
    Key([mod], "egrave", lazy.group["7"].toscreen()),
    Key([mod, "shift"], "egrave", lazy.window.togroup("7")),
    # "8"
    Key([mod], "underscore", lazy.group["8"].toscreen()),
    Key([mod, "shift"], "underscore", lazy.window.togroup("8")),
    # "9"
    Key([mod], "ccedilla", lazy.group["9"].toscreen()),
    Key([mod, "shift"], "ccedilla", lazy.window.togroup("9")),
    # "0"
    Key([mod], "agrave", lazy.group["10"].toscreen()),
    Key([mod, "shift"], "agrave", lazy.window.togroup("10")),

    # "11"
    Key([mod, "mod1"], "ampersand", lazy.group["11"].toscreen()),
    Key([mod, "mod1", "shift"], "ampersand", lazy.window.togroup("11")),
    # "12"
    Key([mod, "mod1"], "eacute", lazy.group["12"].toscreen()),
    Key([mod, "mod1", "shift"], "eacute", lazy.window.togroup("12")),
    # "13"
    Key([mod, "mod1"], "quotedbl", lazy.group["13"].toscreen()),
    Key([mod, "mod1", "shift"], "quotedbl", lazy.window.togroup("13")),
    # "14"
    Key([mod, "mod1"], "apostrophe", lazy.group["14"].toscreen()),
    Key([mod, "mod1", "shift"], "apostrophe", lazy.window.togroup("14")),
    # "15"
    Key([mod, "mod1"], "parenleft", lazy.group["15"].toscreen()),
    Key([mod, "mod1", "shift"], "parenleft", lazy.window.togroup("15")),
    # "16"
    Key([mod, "mod1"], "minus", lazy.group["16"].toscreen()),
    Key([mod, "mod1", "shift"], "minus", lazy.window.togroup("16")),
    # "17"
    Key([mod, "mod1"], "egrave", lazy.group["17"].toscreen()),
    Key([mod, "mod1", "shift"], "egrave", lazy.window.togroup("17")),
    # "18"
    Key([mod, "mod1"], "underscore", lazy.group["18"].toscreen()),
    Key([mod, "mod1", "shift"], "underscore", lazy.window.togroup("18")),
    # "19"
    Key([mod, "mod1"], "ccedilla", lazy.group["19"].toscreen()),
    Key([mod, "mod1", "shift"], "ccedilla", lazy.window.togroup("19")),
    # "20"
    Key([mod, "mod1"], "agrave", lazy.group["20"].toscreen()),
    Key([mod, "mod1", "shift"], "agrave", lazy.window.togroup("20")),
    # == other shortcuts:
    Key([mod], "F9", lazy.group['scratchpad'].dropdown_toggle('term')),
    # special binding for the special button on the MX master
    Key(["control", "mod1"], "Tab", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "F10", lazy.spawn("xbacklight -set 10")),
    Key([mod], "F11", lazy.spawn("xbacklight -set 60")),
    Key([mod], "F12", lazy.spawn("slock")),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


# ==== shortcuts ====
def show_shortcuts():
    """Display a list of current shortcuts configuration."""
    key_map = {"mod1": "alt", "mod4": "mod"}
    shortcuts_path = os.path.join(home_path, "qtile_shortcuts")
    shortcuts = open(shortcuts_path, 'w')
    shortcuts.write("{0:25}| {1:25}\n".format("KEYS COMBINATION", "COMMAND"))
    shortcuts.write("{0:50}\n".format("=" * 50))
    for key in keys:
        key_comb = ""
        for modifier in key.modifiers:
            key_comb += key_map.get(modifier, modifier) + "+"
        key_comb += key.key
        shortcuts.write("{0:25}| ".format(key_comb))
        cmd_str = ""
        for command in key.commands:
            cmd_str += command.name + " "
            for arg in command.args:
                cmd_str += "{0} ".format(repr(arg))
        shortcuts.write("{0:25}\n".format(cmd_str[:25]))
    shortcuts.close()
    #return lazy.spawn("urxvtc -e less {0}".format(shortcuts_path))
    return lazy.group['scratchpad'].dropdown_toggle('keys')


keys.append(Key([mod], "F1", show_shortcuts()))
# ==== end shortcuts


# ==== backgrounds - change background regularly =====
def _change_wallpaper():
    """change the wallpaper.

    If you put two files, first one will go to the first monitor, the other to the second, like this:

    $ feh --bg-center path/to/file/for/first/monitor path/to/file/for/second/monitor
    """
    cmd = (f"/usr/bin/feh --bg-fill --randomize {home_path}/backgrounds/* "
           f"{home_path}/backgrounds/* {home_path}/backgrounds/*")
    logger.info("change wallpaper...")
    return subprocess.run(cmd, shell=True)

@lazy.function
def change_wallpaper(qtile):
    """Changes to random wallpapers for the 3 scrrens."""
    return _change_wallpaper()

def auto_wallpaper(loop):
    """Change wallpaper regularly.

    This function is intended to run in background (threaded).
    """
    # while True:
    _change_wallpaper()
    loop.call_later(1800, auto_wallpaper, loop)


keys.append(Key([mod], "w", change_wallpaper))
# ==== end change background


@hook.subscribe.client_new
def dialogs(window):
    """make dialog floating.

    (this does not work always).
    """
    if(window.window.get_wm_type() == 'dialog' or
            window.window.get_wm_transient_for()):
        window.floating = True


# ==== transparency
def change_transparency(window):
    """change window transparency based on his name/type."""
    kls = window.window.get_wm_class()[1].lower()
    logger.debug("Change transparency for window: %s", kls)
    if 'urxvt' in kls:
        window.cmd_opacity(.7)
    elif 'firefox' in kls or 'chromium' in kls:
        window.cmd_opacity(.9)
    else:
        if window.floating and 'urxvt' not in kls:
            # all floating are almost transparent by default (for popups windows)
            window.cmd_opacity(.95)
        else:
            window.cmd_opacity(.8)


@hook.subscribe.client_new
def transparent_window(window):
    """Make new windows a little transparent."""
    change_transparency(window)


@hook.subscribe.client_focus
def client_focus(window):
    """Change transparency on focus."""
    global last_focus

    if last_focus is not None and last_focus != window:
        try:
            change_transparency(last_focus)
        except Exception:
            pass  # ignore if error

    if last_focus != window:
        last_focus = window
        kls = window.window.get_wm_class()[1].lower()
        logger.debug("Change transparency for current window: %s", kls)
        window.cmd_opacity(1)  # current focused window: no transp
# ==== end transparency


# ==== dynamic multi-screen
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    """Restart qtile when a screen change has been detected."""
    # this is a hack: we use this hook to get the current loop and start the screen
    # change schedule using this loop.
    # We ensure scheduling the change only once at startup.
    global first_start

    logger.info("Screen change event. qtile:%s, loop_qtile:%s", 
                qtile, qtile._eventloop)

    if first_start:
        qtile._eventloop.call_later(1, auto_wallpaper, qtile._eventloop)
        first_start = False

    # Handle the real screen change here:
    #qtile.cmd_restart()
    #pass


def detect_screens(qtile):
    """Detect if a new screen is plugged and reconfigure/restart qtile.

    This should not be necessary.
    """

    def setup_monitors(action=None, device=None):
        """
        Add 1 group per screen
        """

        if action == "change":
            # setup monitors with xrandr
            # call("setup_screens")
            lazy.restart()

        nbr_screens = len(qtile.conn.pseudoscreens)
        for i in xrange(0, nbr_screens-1):
            groups.append(Group('h%sx' % (i+5), persist=False))
    setup_monitors()

    import pyudev

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('drm')
    monitor.enable_receiving()

    # observe if the monitors change and reset monitors config
    observer = pyudev.MonitorObserver(monitor, setup_monitors)
    observer.start()
# ==== end dynamic multi-screen


def is_running(process):
    """check if a process is already running (used in run_once).

    TODO: can be removed
    """
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x.decode('utf-8')):
            return True
    return False


def execute_once(process):
    """run a process once.

    TODO: can be removed
    """
    if not is_running(process):
        return subprocess.Popen(process.split())


def execute(process):
    """run a process."""
    return subprocess.Popen(process.split())


@hook.subscribe.startup_once
def startup_once():
    """Start the applications at Qtile startup."""
    # detect_screens(qtile)
    execute("urxvtd -q -o -f")
    execute("compton")
    execute("nm-applet")
    execute("xautolock -time 5 -locker slock "
            "-notify 30 -notifier notify-send")
    execute("xsetroot -cursor_name left_ptr")


@hook.subscribe.startup_complete
def startup_complete(qtile=None):
    #loop = asyncio.get_event_loop()
    #logger.info("Startup complete: qtile:%s, loop:%s", qtile, loop)
    # here the loop is not yet started
    #loop.call_later(5, auto_wallpaper, loop)

    # old thread method:
    #from threading import Thread
    #Thread(target=auto_wallpaper).start()
    pass
