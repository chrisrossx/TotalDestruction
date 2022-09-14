import os 
import dotenv
try:
    import screeninfo
    monitors = screeninfo.get_monitors()
    if monitors[0].width >= 3000:
        window_pos = "220,80"
    else:
        window_pos = None
except ModuleNotFoundError:
    window_pos = None

if __name__ == "__main__":

    dotenv.load_dotenv()
    os.environ['td_show_debugger'] = "False"
    if window_pos != None:
        os.environ["SDL_VIDEO_WINDOW_POS"]  = window_pos
    from TD.editor.editor import App
    app = App()
    app.run()