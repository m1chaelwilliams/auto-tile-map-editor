import json

WIN_CONFIG_FILEPATH = 'config/win_config.json'
GRAPHICS_CONFIG_FILEPATH = 'config/graphics_config.json'
EDITOR_CONFIG_FILEPATH = 'config/tiles.json'

with open(WIN_CONFIG_FILEPATH, 'r') as f:
    w_data = json.load(f)

WIN_SIZE = (w_data['WIN_SIZE'][0], w_data['WIN_SIZE'][1])
SCREENWIDTH = WIN_SIZE[0]
SCREENHEIGHT = WIN_SIZE[1]
FPS = w_data['FPS']
TILESIZE = w_data['TILESIZE']
TITLE = w_data['TITLE']

with open(GRAPHICS_CONFIG_FILEPATH, 'r') as f:
    g_data = json.load(f)

CLEAR_GRID = g_data['CLEAR_GRID']
BACKGROUND = g_data['BACKGROUND_IMAGE']
LINE_COLOR = g_data['LINE_COLOR']
COLOR_1 = g_data['COLOR_1']
COLOR_2 = g_data['COLOR_2']