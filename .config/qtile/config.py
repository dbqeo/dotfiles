# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
# from libqtile.widget import cpu
import os
import subprocess
from typing import List  # noqa: F401

mod = "mod4"
home = os.path.expanduser('~')

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    
    # Grow and shrink windows
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    
    # Open common applications
    Key([mod], "space", lazy.spawn("dmenu_run")),
    Key([mod], "f", lazy.spawn("thunar")),
    Key([mod], "g", lazy.spawn("firefox")),
    Key([mod], "c", lazy.spawn("code")),
    # doesn't work :( Key([mod], "s", lazy.spawn("spotify-adblock")),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # Default config keys that I don't use
    Key([mod, "control"], "r", lazy.restart()),
    # Key([mod], "r", lazy.spawncmd()),

    # Switch to greeter view (lock)
    Key([mod], "l", lazy.spawn("dm-tool switch-to-greeter")),

    # Screenshot
    Key([mod, "shift"], "s", lazy.spawn("xfce4-screenshooter -r -o \"xclip -selection clipboard -t image/png\""))
]

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layout_theme = {
    "margin": 5,
    "border_focus": '#ffffff',
    "border_normal": '#3492e7'
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(),
    layout.MonadWide(**layout_theme),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Source Sans Pro',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

colors = [
    "#36393f", # 0 Gray background color
    "#ffffff", # 1 White
    "#4bb3ee", # 2 Blue
    "#00b067",  # 3 Green
    "#c5cfd1", # 4 Blue-gray
    "#78a0b3",  # 5 Faded blue
    "#78b39b",  # 6 Faded green
    "#ff6060" # 7 testing color
]

# base config for powerline arrows
pl_arrows = {
    "padding": 0,
    "width": 32,
    "fontsize": 65,
}

screens = [
    Screen(
        top=bar.Bar(
            [   
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[0]
                ),
                widget.GroupBox(
                    active = colors[1],
                    inactive = colors[4],
                    rounded = False,
                    margin_x = 0,
                    padding = 5,
                    border_width = 1,
                    highlight_method = "block",
                    this_current_screen_border = colors[3],
                    this_screen_border = colors[6],
                    other_current_screen_border = colors[2],
                    other_screen_border = colors[5],
                    background = colors[0]
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    background = colors[0]
                ),
                widget.WindowName(
                    background=colors[0]
                ),
                widget.Prompt(
                    background = colors[0]
                ),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[2],
                    background=colors[0],
                ),
                widget.Net(
                    interface='enp27s0',
                    padding=10,
                    background = colors[2],
                    format='{down} ↓↑ {up}'
                ),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[3],
                    background=colors[2],
                ),
                widget.CurrentLayout(
                    background=colors[3],
                    margin=0
                ),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[2],
                    background=colors[3],
                ),
                widget.Memory(
                    background=colors[2]
                ),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[3],
                    background=colors[2],
                ),
                widget.CPUGraph(
                    type='box',
                    background=colors[3],
                    border_width=0,
                    graph_color=colors[1],
                    samples=25,
                    frequency=1
                ),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[0],
                    background=colors[3],
                ),
                widget.Systray(background=colors[0]),
                widget.TextBox(
                    **pl_arrows,
                    text="◀",
                    foreground=colors[4],
                    background=colors[0],
                ),
                widget.Clock(
                    format='%Y-%m-%d %a %I:%M %p',
                    foreground='000000',
                    background=colors[4]),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=colors[4]
                ),
            ],
            24,
        ),
        wallpaper='~/wallpapers/summer_sky_rough.png',
        wallpaper_mode='fill'
    ),
   Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.WindowName()
            ], 24
        ),
        wallpaper='~/wallpapers/summer_sky_rough.png',
        wallpaper_mode='stretch'
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod, "mod1"], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([mod, "shift"], "Button1", lazy.window.toggle_floating()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wname': 'tilda'}, # music visualizer
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Autostart
@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

