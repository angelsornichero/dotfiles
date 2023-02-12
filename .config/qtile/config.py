# Qtile 
# http://www.qtile.org/

# Angel Sornichero
# https://github.com/angelsornichero/

import psutil
import os
import re
import socket
import subprocess
from libqtile import *
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List
from libqtile.widget import *
from path_qtile import qtile_path
import subprocess
import json
from widgets.NextTheme import CurrentTheme


def load_colors():
    with open("/home/user/.config/qtile/theme.json", "r") as theme:
        theme_name = json.load(theme)
    with open("/home/user/.config/qtile/themes/" + theme_name['theme'] + '.json', "r") as colors:
        return json.load(colors)

colors = load_colors()

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "f", lazy.spawn('firefox'), desc="shows firefox"),
    Key([mod], "m", lazy.spawn('rofi -show drun -show-icons'), desc="shows rofi"),
    Key([mod, "control"], "w", lazy.spawn('random-wallpaper'), desc='Change wallpaper'),
    Key([mod], "s", lazy.spawn("scrot /home/path/to/your/screenshots")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),
]

# Nerd Fonts icons: https://www.nerdfonts.com/cheat-sheet
groups = [
    Group("", matches=[Match(wm_class=['firefox'])]),
    Group(""),
    Group(""),
    Group(""),
    Group(""),
    Group("")  
]


for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layouts = [
    layout.MonadTall(
        border_width=1,
        margin=7,
        border_focus=colors["focus"]
    ),
    layout.Max(),
]

def separator(bg = '#ffffff'):
    return widget.Sep(
        linewidth=0,         
        padding=7,
        background=bg
    )

def powerline(bg='#ffffff', fg='#ffffff'):
    return widget.TextBox(
            text='',
            fontsize=50,
            padding=-6,
            foreground=fg,
            background=bg
        )

widget_defaults = dict(
    font="Hack NF",
    fontsize=12,
    padding=5
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    padding_x=20,
                    foreground=colors['text'],
                    inactive=colors['inactive_groups'],
                    highlight_method="block",
                    fontsize=20,
                    this_current_screen_border=colors["focus"],                    
                    rounded=False,
                ),
                widget.WindowName(),

                powerline(colors['grey'], colors['dark-grey'] ),
                
                widget.Systray(background=colors['dark-grey']),
                
                separator(colors['dark-grey']),
                
                powerline(colors['dark-grey'], colors['blue'] ),
                

                widget.TextBox(text=' ', fontsize=30, background=colors['blue']),
                
                widget.CheckUpdates(
                    padding=10,
                    fontsize=18,
                    no_update_string='No updates',
                    display_format='{updates}',
                    update_interval=60,
                    distro="Arch_checkupdates",
                    background=colors['blue']
                ),
                separator(colors['blue']),
                
                powerline(colors['blue'], colors['purple'] ),
                
                widget.TextBox(text='󰟾 ', background=colors['purple'], fontsize=30),
                CurrentTheme(fontsize=15,background=colors['purple']),
                
                separator(colors['purple']),

                powerline(colors['purple'], colors['current-layout'] ),

                widget.CurrentLayoutIcon(scale=0.75, background=colors["current-layout"]),

                widget.CurrentLayout(background=colors["current-layout"]),

                separator(colors['current-layout']),
                
                powerline(colors['current-layout'], colors['yellow'] ),
                
                widget.TextBox(background=colors['yellow'], text=' ', fontsize=20, foreground=colors['text']),

                widget.Clock(format="%H:%M - %d/%m/%Y ", background=colors['yellow'], fontsize=17, foreground=colors['text']),
            ],
            35,
            background=colors["grey"],
            opacity=1,
            foreground=colors['text']

        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
