import os 

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (75, 175)
    from TD.app import App
    app = App()
    app.run()
