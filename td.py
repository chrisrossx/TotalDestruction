from email.policy import default
import os 
import click 
import dotenv



@click.command()
@click.option("--file", default=None, help="Load Level File Directly for Debugging")
@click.option("--start", default=0, help="start debugging at given time")
def app(file, start):
    """
    Total Destruction by Christopher Ross
    """
    dotenv.load_dotenv()
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (75, 175)
    from TD.app import App
    start = None if file == None else start
    app = App(file, start)
    app.run()


if __name__ == "__main__":
    app()
