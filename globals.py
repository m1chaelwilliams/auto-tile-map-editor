import json

class Globals:
    # window
    TILESIZE: int = 50
    SCREENWIDTH: int = 1280
    SCREENHEIGHT: int = 720
    FPS: int = 60
    TITLE: str = "Sphere's Tilemap Editor V2"

    # graphics
    CLEAR_GRID = False
    BACKGROUND = "assets/berkbg.jpg"
    LINE_COLOR = "WHITE"
    COLOR_1 = "#282828"
    COLOR_2 = "black"

    WIN_CONFIG_FILEPATH = 'config/win_config.json'
    GRAPHICS_CONFIG_FILEPATH = 'config/graphics_config.json'
    EDITOR_CONFIG_FILEPATH = 'config/tiles.json'

    @staticmethod
    def init():
        # win config
        with open(Globals.WIN_CONFIG_FILEPATH, 'r') as f:
            w_data = json.load(f)

        try:
            Globals.TILESIZE = w_data['TILESIZE']
            WIN_SIZE = w_data['WIN_SIZE']
            Globals.SCREENWIDTH = WIN_SIZE[0]
            Globals.SCREENHEIGHT = WIN_SIZE[1]
            Globals.FPS = w_data['FPS']
            Globals.TITLE = w_data['TITLE']
        except:
            print('Window config file did not contain all necessary configurations, using defaults for the remainder.')

        # graphics config
        with open(Globals.GRAPHICS_CONFIG_FILEPATH, 'r') as f:
            g_data = json.load(f)

        try:
            Globals.CLEAR_GRID = g_data['CLEAR_GRID']
            Globals.BACKGROUND = g_data['BACKGROUND_IMAGE']
            Globals.LINE_COLOR = g_data['LINE_COLOR']
            Globals.COLOR_1 = g_data['COLOR_1']
            Globals.COLOR_2 = g_data['COLOR_2']
        except:
            print('Graphics config file did not contain all necessary configurations, using defaults for the remainder.')


        