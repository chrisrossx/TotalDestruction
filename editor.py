
import os 

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (10, 90)
    from TD.editor.editor import App
    app = App()
    app.run()