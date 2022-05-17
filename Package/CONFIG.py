import numpy as np

# Thiết lập chung
TILESIZE = 30
WIDTH = 1280
HEIGHT = 720

FPS = 50
BLACK = (0, 0, 0)

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
NUMBER_AMMO = 60
UI_FONT = './Assets/Font/Fairfax.ttf'
UI_FONT_SIZE = 18

UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'

# UI COLOR
HEALTH_COLOR = 'red'
AMMO_COLOR = 'gold'

# Load dữ liệu map


def load_map(path):
    map_data = np.genfromtxt(path, delimiter=',')
    return map_data


player_stats = {
    'health': 100,
    'number_ammo': 30,
    'attack': 50,
    'speed': 5,
    'range_attack': 8
}

enemy_stats = {
    'normal': {    
        'health': 150,
        'damage': 75,
        'speed': 3,
        'attack_radius': 20,
        'notice_radius': 100,
    },
    'boss': {
        'health': 550,
        'damage': 175,
        'speed': 5,
        'attack_radius': 25,
        'notice_radius': 100,
    }
}
