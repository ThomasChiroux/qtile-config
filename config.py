"""my qtile config file."""
import os
import re
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from widget.vpn_checker import ConnectionStatus

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
wmname = "qtile"


def get_current_kb_layout():
    """return the detected keyboard layout."""
    s = subprocess.Popen(["setxkbmap", "-print"], stdout=subprocess.PIPE)
    lines = s.stdout.readlines()
    for line in lines:
        if b"xkb_geometry" in line:
            return line.decode('utf-8').split('"')[1].split('(')[0]


kb_layout = get_current_kb_layout()


groups = [Group("main",
                layout="monadtall",
                spawn="firefox-developer"),  # spawn="chromium"
          Group("main2",
                layout="monadtall",
                spawn="firefox"),
          Group("term",
                layout="monadwide",
                spawn="urxvtc"),
          Group("dev1",
                layout="monadtall"),
          Group("dev2",
                layout="monadtall"),
          Group("term2",
                layout="monadwide"),
          Group("7", layout="max"),
          Group("8", layout="max"),
          Group("sip",
                layout="monadtall",
                spawn="linphone"), ]


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
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod, "shift", "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift", "control"], "j", lazy.layout.shuffle_up()),

    # == window resizing (most for Monadtall layout)
    Key([mod], "h", lazy.layout.grow()),
    Key([mod, "shift"], "h", lazy.layout.shrink()),
    Key([mod], "l", lazy.layout.shrink()),
    Key([mod, "shift"], "l", lazy.layout.grow()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "f", lazy.layout.flip()),
    Key([mod], "m", lazy.layout.maximize()),
    Key([mod, "control"], "m", lazy.window.toggle_minimize()),

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

    # special binding for the special button on the MX master
    Key(["control", "mod1"], "Tab", lazy.spawn("urxvtc")),

    # == spawns and qtile commands
    Key([mod], "r", lazy.spawncmd()),
    Key([mod, "shift"], "r", lazy.qtilecmd()),

    Key([mod, "shift"], "c", lazy.window.kill()),

    # == Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),

    # == restart and shutdown qtile
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

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
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("xbacklight -dec 10")),

    # == toggle screens
    Key([mod], "s", lazy.next_screen()),
    Key([mod, "shift"], "s", lazy.prev_screen()),
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
    Key([mod], "ccedilla", lazy.group["sip"].toscreen()),
    Key([mod, "shift"], "ccedilla", lazy.window.togroup("9")),

    # == other shortcuts:
    Key([mod], "F12", lazy.spawn("slock")),

]


layout_theme = dict(border_normal='#101010',
                    border_focus="#bb5F0C",
                    border_width=2)

layouts = [
    layout.MonadWide(
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
]

widget_defaults = dict(
    font='DejaVu Sans Mono for Powerline',
    foreground="aaaaaa",
    fontsize=20,
    padding=1,
)

screens = [
    Screen(top=bar.Bar(
        [
            widget.GroupBox(urgent_alert_method='border',
                            fontsize=20,
                            borderwidth=3,
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
            widget.ThermalSensor(foreground="aaaaaa",
                                 foreground_alert="ee5555",
                                 threshold=75,
                                 tag_sensor="Physical id 0"),
            widget.Sep(padding=6, height_percent=60),
            widget.Backlight(backlight_name='intel_backlight',
                             update_interval=1),
            widget.Sep(padding=6, height_percent=60),
            widget.BatteryIcon(),
            widget.Sep(padding=6, height_percent=60),
            widget.Volume(emoji=True,
                          font="NotoColorEmoji-Regular",
                          # yaourt -S humanity-icons
                          # theme_path='/usr/share/icons/Humanity/status/22/',
                          # font='Arial',
                          update_interval=1),
            widget.Sep(padding=6, height_percent=60),
            widget.Clock(format='%a %d-%m-%Y %H:%M:%S'),
            widget.Sep(padding=6, height_percent=60),
            ConnectionStatus(name="NewLinkCare", font="NotoColorEmoji-Regular",
                             fmt_ok="\U0001F510", fmt_nok="\U0001F513"),
            ConnectionStatus(name="protonvpn", font="NotoColorEmoji-Regular",
                             fmt_ok="\U0001F510", fmt_nok="\U0001F513"),
            widget.CurrentLayoutIcon(foreground="00eedd", scale=0.8),
        ],
        size=32, opacity=0.9,)),
    Screen(top=bar.Bar(
        [
            widget.GroupBox(urgent_alert_method='border',
                            fontsize=11,
                            borderwidth=3,
                            inactive="606060",
                            use_mouse_wheel=False,
                            disable_drag=True),
            widget.Sep(padding=6, height_percent=60),
            widget.Prompt(),
            # widget.Notify(default_timeout=10),
            widget.TaskList(),
            widget.Systray(),  # icon_size=14, padding=20),
            widget.Sep(padding=6, height_percent=60),
            widget.Volume(emoji=True,
                          font="NotoColorEmoji-Regular",
                          # yaourt -S humanity-icons
                          # theme_path='/usr/share/icons/Humanity/status/22/',
                          # font='Arial',
                          update_interval=1),
            widget.Sep(padding=6, height_percent=60),
            widget.Clock(format='%a %d-%m-%Y %H:%M:%S'),
            widget.Sep(padding=6, height_percent=60),
            ConnectionStatus(name="NewLinkCare", font="NotoColorEmoji-Regular",
                             fmt_ok="\U0001F510", fmt_nok="\U0001F513"),
            ConnectionStatus(name="protonvpn", font="NotoColorEmoji-Regular",
                             fmt_ok="\U0001F510", fmt_nok="\U0001F513"),
            widget.CurrentLayoutIcon(foreground="00eedd", scale=0.8),
        ],
        size=20, opacity=0.9,)),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


def show_shortcuts():
    """Display a list of current shortcuts configuration."""
    key_map = {"mod1": "alt", "mod4": "mod"}
    shortcuts_path = "{0}/{1}".format(os.environ["HOME"], "qtile_shortcuts")
    shortcuts = open("{0}".format(shortcuts_path), 'w')
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
        shortcuts.write("{0:25}\n".format(cmd_str))
    shortcuts.close()
    return lazy.spawn("urxvtc -e less {0}".format(shortcuts_path))


keys.append(Key([mod], "F1", show_shortcuts()))


@hook.subscribe.client_new
def dialogs(window):
    """make dialog floating.

    (this does not work always).
    """
    if(window.window.get_wm_type() == 'dialog' or
            window.window.get_wm_transient_for()):
        window.floating = True


@hook.subscribe.client_new
def transparent_terms(window):
    """Make terminal and sublime a little transparent."""
    if 'urxvt' in window.name or 'subl' in window.name:
        window.cmd_opacity(.9)


@hook.subscribe.client_new
def cinelerra_dialogues(window):
    """hook for cinelerra."""
    if "Cinelerra" in window.name:
        window.floating = True


def is_running(process):
    """check if a process is already running (used in run_once)."""
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x.decode('utf-8')):
            return True
    return False


def execute_once(process):
    """run a process once."""
    if not is_running(process):
        return subprocess.Popen(process.split())


@hook.subscribe.startup
def startup():
    """Start the applications at Qtile startup."""
    # subprocess.Popen("sleep 3".split())
    execute_once("urxvtd -q -o -f")
    execute_once("nm-applet")
    # execute_once("compton")
    # execute_once("feh --bg-fill --randomize ~tchiroux/backgrounds/*")
    # execute_once("touchegg")
    execute_once("xautolock -time 5 -locker slock "
                 "-notify 30 -notifier notify-send")
    execute_once("xsetroot -cursor_name left_ptr")
