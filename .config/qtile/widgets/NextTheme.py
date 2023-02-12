# My custom widget for show the current theme, it uses theme-controller

from libqtile import bar, hook
from libqtile.log_utils import logger
from libqtile.widget import base
import json
import os
from libqtile.lazy import lazy
from libqtile.command import lazy

class CurrentTheme(base._TextBox):
    """
    Display the current theme
    """

    def __init__(self, **config):
        super().__init__("Hey", **config)
        self.show_current_theme()
        self.add_callbacks(
            {
                'Button1': lazy.spawn('python /home/user/.config/qtile/lib/theme_controller.py'),
            }
        )


    def show_current_theme(self): 
        with open('/home/angel/.config/qtile/theme.json') as theme:
            specific_theme = json.load(theme)
            self.text = specific_theme['theme']

    def next_theme(self):
        themes_dir = os.listdir('/home/angel/.config/qtile/themes')
        current_theme = themes_dir[themes_dir.index(self.text + '.json') + 1]
        os.system(f'notify-send -t 100 "Theme changed to {current_theme}"')
        
