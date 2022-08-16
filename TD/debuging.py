import time 
import functools

from blinker import signal
import pygame 

class GameDebugger:
    def __init__(self):

        self.surface = None
        self.font = None
        self.frame_count = 0
        self.one_second_elapsed = 0
        self.frame_count_surface = None
        self.frame_count_value = 0
        self.lines = [None for i in range(20)]

        self.timeits = {}
        self.timeits_callback = []

        self.show_panel = True 
        self.show_sky = True
        self.show_hitboxes = not True
        self.show_paths = not True
        self.show_bounds = not True 
        self.print_app_timits = not True 

        self.disable_input = 0
        signal("debugger.disable_input").connect(self.on_disable_input)
        signal("debugger.enable_input").connect(self.on_enable_input)

        self.app_timeits = [
            "app.loop",
            "app.on_event",
            "app.pressed",
            "app.scene.tick",
            "app.debugger.tick",
            "app.scene.draw",
            "app.debugger.draw",
            "app.flip",
        ]

        self.timeits_callback.append(self.print_app_timeits_cb)

    def print_app_timeits_cb(self):
        if self.print_app_timits:
            print("-"*53)
            print("{:<22}: {:>8}, {:>8}, {:>9}".format("[APP TIMEITS]", "SECONDS", "FPS", "%"))
            tally = self.timeits["app.loop"]["report_value"]
            for name in self.app_timeits:
                timeit = self.timeits[name]
                v = timeit["report_value"]
                print("- {:<20}: {:>7.6f}, {:>8.1f}, {:>8.1f}%".format(name, v, 1/v, (v/tally)*100))

    def on_disable_input(self, sender):
        self.disable_input += 1

    def on_enable_input(self, sender):
        self.disable_input -= 1

    def load(self):
        self.surface = pygame.Surface((300,300), pygame.SRCALPHA, 32)
        self.font = pygame.font.SysFont("consolas", 12)
        self.frame_count = 0
        self.frame_count_value = 0
        self.one_second_elapsed = 0
        self.frame_count_surface = self.font.render("---", True, (255, 255, 0))

        for timeit in self.app_timeits:
            game_debugger.timeit_setup(timeit)

    def timeit_wrapper(self, name):
        def _decorate(function):
            @functools.wraps(function)
            def wrapped_function(*args, **kwargs):
                self.timeit_start(name)
                function(*args, **kwargs)
                self.timeit_end(name)
            return wrapped_function
        return _decorate


    def tick(self, elapsed):

        self.frame_count += 1
        self.one_second_elapsed += elapsed
        if self.one_second_elapsed >= 1000:
            self.frame_count_value = self.frame_count
            line = "{}".format(str(self.frame_count)) 
            self.frame_count_surface = self.font.render(line, True, (255, 255, 0))
            self.frame_count = 0
            self.one_second_elapsed = 0.0
        
            for name, timeit in self.timeits.items():
                if len(timeit["values"]) > 0:
                    v = sum(timeit["values"]) / len(timeit["values"])
                    timeit["report_value"] = v
                    timeit["report"] = "{}: {:.5f}, {:.1f}".format(name, v, 1/v)
                    timeit["values"] = []
                else:
                    timeit["report"] = "{}: --, --".format(name)
                    timeit["report_value"] = 0.0
                if timeit["render_to_line"]:
                        self.lines[timeit["render_to_line"]] = timeit["report"]
                if timeit["print_out"]:
                    print(timeit["report"])
            for cb in self.timeits_callback:
                cb()

    def timeit_setup(self, name, render_to_line=None, print_out=False):
        self.timeits[name] = {
            "values": [],
            "start": 0,
            "render_to_line": render_to_line,
            "report": "--",
            "report_value": 0.0,
            "print_out": print_out,
        }
        if render_to_line != None :
            self.lines[render_to_line] = "{}: -- - --".format(name)

    def timeit_start(self, name):
        self.timeits[name]["start"] = time.perf_counter()

    def timeit_end(self, name):
        self.timeits[name]["values"].append(time.perf_counter() - self.timeits[name]["start"])

    def on_event(self, event, elapsed):
        if self.disable_input == 0 and event.type == pygame.KEYDOWN:
            if event.key == 96:
                if self.show_panel == None:
                    self.show_panel = 1
                elif self.show_panel == 1:
                    self.show_panel = 2
                else:
                    self.show_panel = None
                # self.show_panel = not self.show_panel

            bypass_show_panel_lock_out = self.show_panel
            # self.show_panel = True 
            if event.key == pygame.K_s:
                if self.show_panel :
                    self.show_sky = not self.show_sky

            if event.key == pygame.K_h:
                if self.show_panel:
                    self.show_hitboxes = not self.show_hitboxes

            if event.key == pygame.K_p:
                if self.show_panel:
                    self.show_paths = not self.show_paths

            if event.key == pygame.K_t:
                if self.show_panel:
                    self.print_app_timits = not self.print_app_timits

            if event.key == pygame.K_e:
                if self.show_panel:
                    from TD.particles.explosions import ExplosionMedium
                    signal("scene.add_entity").send(ExplosionMedium(pygame.Vector2(800,300)))

            if event.key == pygame.K_r:
                if self.show_panel:
                    from TD.particles.explosions import ExplosionMedium002
                    signal("scene.add_entity").send(ExplosionMedium002(pygame.Vector2(800,400)))

            if event.key == pygame.K_b:
                if self.show_panel:
                    self.show_bounds = not self.show_bounds
    
            self.show_panel = bypass_show_panel_lock_out 

    def draw(self, elapsed):
        self.surface.fill((0,0,0,0))
        if self.show_panel:
            if self.show_panel == 1 or self.show_panel == 2:
                if self.frame_count_surface:
                    self.surface.blit(self.frame_count_surface, (10, 10))
            if self.show_panel == 1:
                for i in range(len(self.lines)):
                    line = self.lines[i]
                    if line:
                        #TODO Could optomize this by cacheing rendered text, only update when set
                        surface = self.font.render(line, True, (255, 255, 0))
                        self.surface.blit(surface, (10, (i * 17)+25))

game_debugger = GameDebugger()
