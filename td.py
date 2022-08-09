import os 

if __name__ == "__main__":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    from TD.app import App
    app = App()
    app.run()
