import os 
import time
import functools

import pygame
from pygame import Vector2
from TD import current_scene
from TD.assetmanager import asset_manager
from TD import current_app


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

        if "td_show_debugger" in os.environ and os.environ["td_show_debugger"] == "True":
            self.show_panel = 2
        else:
            self.show_panel = 0
        self.show_sky = False if os.environ.get("td_debugger_sky", "True") == "False" else True
        self.show_hitboxes = not True
        self.show_paths = not True
        self.show_bounds = not True
        self.print_app_timits = not True
        self.god_mode = True
        self.speed = 1.0

        self._disable_input = 0

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

        self.numpad_speed_keys = {
            pygame.K_KP0: 0,
            pygame.K_KP1: 0.1,
            pygame.K_KP2: 0.5,
            pygame.K_KP3: 0.75,
            pygame.K_KP4: 1.0,
            pygame.K_KP5: 1.0,
            pygame.K_KP6: 1.1,
            pygame.K_KP7: 1.25,
            pygame.K_KP8: 1.5,
            pygame.K_KP9: 2.0,
        }

        self.timeits_callback.append(self.print_app_timeits_cb)

        if self.show_panel:
            print("[K_~: show_debugger] ", self.show_panel)
            print("[K_s: show_sky]      ", self.show_sky)
            print("[K_g: show_hitboxes] ", self.show_hitboxes)
            print("[K_p: show_paths]    ", self.show_paths)
            print("[K_t: app_timits]    ", self.print_app_timits)
            print("[K_b: show_bounds]   ", self.show_bounds)
            print("[K_g: god_mode]      ", self.god_mode)
            print("[k_KP#: Speed]       ", self.speed)
            print("[K_p: screenshot]")

    def clear_lines(self):
        self.lines = [None for i in range(20)]
        # pass

    def print_app_timeits_cb(self):
        if self.print_app_timits:
            print("-" * 53)
            print(
                "{:<22}: {:>8}, {:>8}, {:>9}".format(
                    "[APP TIMEITS]", "SECONDS", "FPS", "%"
                )
            )
            tally = self.timeits["app.loop"]["report_value"]
            for name in self.app_timeits:
                timeit = self.timeits[name]
                v = timeit["report_value"]
                print(
                    "- {:<20}: {:>7.6f}, {:>8.1f}, {:>8.1f}%".format(
                        name, v, 1 / v, (v / tally) * 100
                    )
                )

    def disable_input(self):
        self._disable_input += 1

    def enable_input(self):
        self._disable_input -= 1

    def load(self):
        self.surface = pygame.Surface((300, 300), pygame.SRCALPHA, 32)
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
                    timeit["report"] = "{}: {:.5f}, {:.1f}".format(name, v, 1 / v)
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
        if render_to_line != None:
            self.lines[render_to_line] = "{}: -- - --".format(name)

    def timeit_start(self, name):
        self.timeits[name]["start"] = time.perf_counter()

    def timeit_end(self, name):
        self.timeits[name]["values"].append(
            time.perf_counter() - self.timeits[name]["start"]
        )

    def on_event(self, event, elapsed):

        if event.type == pygame.KEYDOWN and event.key == 96:
            if "td_show_debugger" in os.environ and os.environ["td_show_debugger"] == "True":
                if self.show_panel == None:
                    self.show_panel = 1
                elif self.show_panel == 1:
                    self.show_panel = 2
                else:
                    self.show_panel = None

        if self._disable_input == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            # print("Screen SHOT!")
            rect = pygame.Rect(0, 0, 1024, 600)
            sub = current_app.screen.subsurface(rect)
            shot = pygame.Surface((1024, 600))
            shot.blit(sub, (0, 0))
            import uuid 
            filename = "screenshot_{}.png".format(str(uuid.uuid4()))
            print("Saved Screenshot: {}".format(filename))
            pygame.image.save(shot, filename)

        if (
            self._disable_input == 0
            and event.type == pygame.KEYDOWN
            and self.show_panel
        ):


            bypass_show_panel_lock_out = self.show_panel

            if event.key == pygame.K_s:
                self.show_sky = not self.show_sky

            if event.key == pygame.K_h:
                self.show_hitboxes = not self.show_hitboxes

            if event.key == pygame.K_p:
                self.show_paths = not self.show_paths

            if event.key == pygame.K_t:
                self.print_app_timits = not self.print_app_timits

            if event.key == pygame.K_b:
                self.show_bounds = not self.show_bounds

            if event.key == pygame.K_g:
                self.god_mode = not self.god_mode
                print("DEBUGGER.god_mode = {}".format(self.god_mode))

            if event.key in self.numpad_speed_keys.keys():
                index = list(self.numpad_speed_keys.keys()).index(event.key)
                self.speed = list(self.numpad_speed_keys.values())[index]
                print("DEBUGGER.speed: ", self.speed)

            if event.key == pygame.K_u:
                from TD.particles.explosions import ExplosionMedium, ExplosionSmall
                from TD.particles.spoofs import SpoofHitFollow
                from TD.bullets import Missile, Missile002
                from TD.assetmanager import asset_manager
                from TD.pickups import PickupCoin, PickupHeart

                # from TD.entity import Entity
                # current_scene.em.add(ExplosionSmall(Vector2(512,250)))
                # current_scene.em.add(ExplosionMedium(Vector2(512,350)))
                import random

                # a = random.randint(0,359)
                # m = Missile002(Vector2(512, 300), a)
                # current_scene.em.add(m)
                # current_app.mixer.play("missile launch")
                # m = Missile(Vector2(512, 300), 0)
                # current_scene.em.add(m)
                # from TD.bullets import Bullet001
                # for i in range(0,359, 5):
                #     pos = Vector2(random.randint(200,900), random.randint(100,500))
                #     p = PickupCoin(pos)
                #     # bullet = Bullet001([512, 300], i)
                #     current_scene.em.add(p)

                from TD.pickups import PickupUpgrade

                pos = Vector2(512, 300)
                pos2 = Vector2(612, 400)
                for i in range(3):
                    current_scene.em.add(PickupUpgrade(pos))
                    # current_scene.em.add(PickupUpgrade2(pos2))
                # import random

            if event.key == pygame.K_o:
                from TD.scenes.level.dialog import EnemyDialog
                from TD.characters import Dialog, Elle
                d = EnemyDialog(Elle(Dialog.DYING))
                current_scene.em.add(d)

            if event.key == pygame.K_i:
                from TD.particles.explosions import ExplosionMedium, ExplosionSmall
                from TD.particles.spoofs import SpoofHitFollow
                from TD.bullets import Missile, Missile002

                # from TD.entity import Entity
                # current_scene.em.add(ExplosionSmall(Vector2(512,250)))
                # current_scene.em.add(ExplosionMedium(Vector2(512,350)))
                import random

                a = random.randint(0, 359)
                m = Missile(Vector2(512, 300), a)
                current_scene.em.add(m)
                current_app.mixer.play("missile launch 002")

                a = random.randint(0, 359)
                m = Missile002(Vector2(712, 300), a)
                current_scene.em.add(m)
                current_app.mixer.play("missile launch 002")
                # import random
                # for i in range(1000):
                #     a = ExplosionMedium(Vector2(random.randint(100,924), random.randint(100,500)))
                #     a.frame_loop_end = -1
                #     a.frame_duration = -1
                #     a.velocity = 0
                #     current_scene.em.add(a)
                # current_scene.em.add(SpoofHitFollow(Vector2(612,350)))

            self.show_panel = bypass_show_panel_lock_out

    def draw(self, elapsed):
        self.surface.fill((0, 0, 0, 0))
        if self.show_panel:
            if self.show_panel == 1 or self.show_panel == 2:
                if self.frame_count_surface:
                    self.surface.blit(self.frame_count_surface, (10, 10))
                for i in range(1):
                    line = self.lines[i]
                    if line:
                        # TODO Could optomize this by cacheing rendered text, only update when set
                        surface = self.font.render(line, True, (255, 255, 0))
                        self.surface.blit(surface, (10, (i * 17) + 25))
            if self.show_panel == 1:
                for i in range(len(self.lines)):
                    line = self.lines[i]
                    if line:
                        # TODO Could optomize this by cacheing rendered text, only update when set
                        surface = self.font.render(line, True, (255, 255, 0))
                        self.surface.blit(surface, (10, (i * 17) + 25))


game_debugger = GameDebugger()
