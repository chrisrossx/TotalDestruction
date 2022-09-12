import os 
import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    os.environ['td_show_debugger'] = "False"
    from TD.editor.editor import App
    app = App()
    app.run()