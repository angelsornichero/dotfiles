# This script change the colors
# Is used in CurrentTheme widget

import os
import json
from libqtile.command.client import CommandClient, InteractiveCommandClient

c = CommandClient()
i = InteractiveCommandClient()

def main(): 
    with open('/home/user/.config/qtile/theme.json') as theme:
        specific_theme = json.load(theme)
        text = specific_theme['theme']
    
    themes_dir = os.listdir('/home/user/.config/qtile/themes')
    next_index = themes_dir.index(text + '.json') + 1
    if next_index >= len(themes_dir):
        next_index = 0
    next_theme = themes_dir[next_index]
    with open('/home/angel/.config/qtile/theme.json', 'w') as theme_json:
        json.dump({"theme": next_theme.replace('.json', '')}, theme_json, indent=4)
    os.system(f'notify-send -t 2000 "Theme changed to {next_theme.replace(".json", "")}"')
    os.system('qtile cmd-obj -o cmd -f reload_config')
    
    

if __name__ == '__main__':
    main()
