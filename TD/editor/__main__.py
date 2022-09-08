import os 

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (220, 80)
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (5, 80)
    from TD.editor.editor import App
    app = App()
    app.run()