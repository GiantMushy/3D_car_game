from GameManager import GameManager

if __name__ == "__main__":
    view_settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}
    game_settings = {"track_number": 0, "min_len": 12, "max_len": 24}
    game = GameManager(view_settings=view_settings, game_settings=game_settings)
    game.start()