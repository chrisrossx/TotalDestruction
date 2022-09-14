import sys 
import getopt

import pygame
from pygame import Vector2
from TD.assetmanager import asset_manager
from TD.config import SCREEN_SIZE

from TD.editor.level_scene import SceneLevel

# from TD.globals import current_app, current_scene
from TD.editor.globals import current_app, current_scene, scene_level, current_level
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.editor.editorassets import editor_assets

class App:
    """
    Total Destruction Level Editor Main Loop
    """

    def __init__(self):
        current_app.__wrapped__ = self
        self.size = EDITOR_SCREEN_SIZE

        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "")
        if len(args) != 1:
            self.arg_filename = None
        else:
            self.arg_filename = args[0]

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Level Editor")
        self.font = pygame.font.Font(None, 18)
        self.font = pygame.font.SysFont("Consolas", 12)

        asset_manager.load()
        editor_assets.load()

        self.running = True
        self.frame_count_value = 0
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = asset_manager.fonts["xs"].render("---", True, (255,255,0))

    def exit(self):
        """
        Stop the main game loop
        """
        self.running = False

    # def change_scene(self, scene_name):
    #     """
    #     Transition to a new scene. 
    #     data
    #     """
    #     self.scene.deactivate()
    #     if scene_name == "level":
    #         self.scene = self.scene_level
    #     self.scene.activate()

    def _set_scene(self, scene):
        """
        Set the scene and start it. ALso set the singleton proxy
        """
        self.scene = scene
        current_scene.__wrapped__ = self.scene 
        self.scene.on_start()

    def run(self):
        try:
            self._run()
        except Exception as e:
            try:
                current_level.save_backup("crashed_editor")
            except:
                print("Failed to save level backup")
                
            raise e

    def _run(self):

        self._set_scene(SceneLevel(self.arg_filename))
        # self._set_scene(MainMenu())
        # self._set_scene(TestScene())
        
        self.clock.tick()
        self.running = True

        while 1:
            elapsed = self.clock.tick(60)

            self.frame_count_elapsed += elapsed
            self.frame_count += 1
            if self.frame_count_elapsed >= 1000:
                self.frame_count_elapsed = 0
                self.frame_count_surface = asset_manager.fonts["xs"].render("{:03.0f}".format(self.frame_count), True, (255,255,0))
                self.frame_count = 0

            # --------------------
            # Event Handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if hasattr(self.scene, "level"):
                        self.scene.level.save_backup("closed_editor")
                    self.running = False
                    break
                self.scene.on_event(event, elapsed)
            
            pressed = pygame.key.get_pressed()
            self.scene.pressed(pressed, elapsed)

            if self.running:
                # --------------------
                # Tick            
                self.scene.tick(elapsed)

                # --------------------
                # Draw            
                self.scene.draw(elapsed)

                # --------------------
                # BLit to Screen     
                self.screen.blit(self.scene.surface, (0,0))
                self.screen.blit(self.frame_count_surface, (3,3))
                pygame.display.flip()

            else:
                break

        
        #Be Friendly 
        print("Thank you, come again!")
