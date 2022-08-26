from pygame import Vector2 
import pygame

from .hud import HUDMedal100, HUDMedal70 , HUDMedalHeart, HUDLife
from .level_state import LevelState, LevelStateMachine
from TD.scenes.scene import Scene
from TD.entity import Entity, EntityManager, EntityType, EntityVectorMovement
from TD.gui import GUIPanel, GUILabel, Sprite
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT, SCREEN_SIZE
from TD.scenes.levels.pause_menu import PauseMenu
from TD.player import PlayerShip
from TD.debuging import game_debugger
from TD.particles.explosions import ExplosionMedium
from TD import current_app, current_scene


class DeadState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)

    def start(self):
        super().start()
        self.player.enabled = False
        self.player.input_enabled = False

        explosion = ExplosionMedium(self.player.pos)
        # explosion.animation_finished_callback = self.on_animation_finished
        current_scene.em.add(explosion)
        current_scene.em.add(ExplosionMedium(self.player.pos + Vector2(-35, 0)))
        current_scene.em.add(ExplosionMedium(self.player.pos + Vector2(0, 15)))
        current_scene.em.add(ExplosionMedium(self.player.pos + Vector2(-15, -5)))
        self.red_sprite = Sprite(asset_manager.sprites["HUD Hurt"])
        self.red_sprite.surface.set_alpha(50)
        current_scene.em.add(self.red_sprite)
        current_app.mixer.play("explosion player")

    def tick_step_003(self, elapsed):
        current_scene.exit({"condition": "died"})

    def tick_step_002(self, elapsed):
        #Fade out Level Complete Label
        x = 500
        l = ((x - self.step_elapsed) / x ) * 255
        if l > 255:
            l = 255
        self.game_over.surface.set_alpha(l)
        l = ((x - self.step_elapsed) / x ) * 50
        if l > 50:
            l = 50
        self.red_sprite.surface.set_alpha(l)

        #Fly out HUD
        hud_y = 0 # A little lazy but all HUDs are at same Y values
        for key, hud in self.hud.items():
            hud.y -= elapsed * 0.06
            hud_y = hud.y

        #Make sure both the player and HUD are off screen
        if self.step_elapsed >= x and hud_y <= -32:
            self.next_step()

    def tick_step_001(self, elapsed):
        if self.step_elapsed >= 1000:
            self.next_step()

    def tick_step_000(self, elapsed):
        if self.step_elapsed >= 500:
            self.next_step()
            self.game_over = GUILabel("GAME OVER", asset_manager.fonts["lg"], (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
            self.game_over.center_in_rect(SCREEN_RECT)
            current_scene.em.add(self.game_over)

    # def on_animation_finished(self, entity):
    #     entity.delete()
    #     self.next_step()



class WonState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)

    def start(self):
        super().start()
        self.player.input_enabled = False
        self.step_elapsed = 0.0
        self.lbl_complete = GUILabel("LEVEL COMPLETE", asset_manager.fonts["lg"], (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        self.lbl_complete.center_in_rect(SCREEN_RECT)
        self.player.velocity = 0 
        self.player.heading = Vector2(1, 0)

    def tick_step_000(self, elapsed):
        #Enjoy Victory for a pause! 
        if self.step_elapsed > 1500:
            current_scene.em.add(self.lbl_complete)
            self.player.velocity = 0.2
            self.next_step()

    def tick_step_001(self, elapsed):
        #Fly out Player and HUD
        self.player.pos += self.player.heading * self.player.velocity
        
        #Fly out HUD
        hud_y = 0 # A little lazy but all HUDs are at same Y values
        for key, hud in self.hud.items():
            hud.y -= elapsed * 0.04
            hud_y = hud.y

        #Make sure both the player and HUD are off screen
        if self.player.pos.x >= 1050 and hud_y <= -32:
            self.next_step()

    def tick_step_002(self, elapsed):
        #Fade out Level Complete Label
        x = 500
        l = ((x - self.step_elapsed) / x ) * 255
        if l > 255:
            l = 255
        self.lbl_complete.surface.set_alpha(l)
        if self.step_elapsed >= x:
            current_scene.exit({"condition": "won"})
                

class StartingState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)
      
    def tick_step_000(self, elapsed):
        # Skip for now
        if not False:
            self.player.pos.x = 200
            for key, hud in self.hud.items():
                hud.y = 0
            current_scene.change_state(LevelState.PLAYING)
            return
        
        #Fly in HUD
        for key, hud in self.hud.items():
            hud.y += elapsed * 0.04
            if hud.y >= 0:
                hud.y = 0
        
        #Fly in Ship 
        self.player.pos.x += elapsed * 0.12
        if self.player.pos.x > 200: 
            self.player.pos.x = 200
            self.next_step()
            self.starting_go = GUILabel("GO!", asset_manager.fonts["lg"], (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
            self.starting_go.center_in_rect(SCREEN_RECT)
            current_scene.em.add(self.starting_go)

    def tick_step_001(self, elapsed):
        if self.step_elapsed > 500:
            current_scene.em.delete(self.starting_go)
            current_scene.change_state(LevelState.PLAYING)

class PlayingState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)
        self.runtime = 0.0
        self.timed_add = []

        self.total_enemies = 4
        self.enemies_missed = 0

        # TODO

    def enemy_missed(self, enemy):
        self.enemies_missed += 1
        print("enemy missed")
        if self.enemies_missed / self.total_enemies >= 0.3:
            self.hud["medal70"].invalid()
            # TODO
            # signal("scene.hud.medal.70").send(False)
        if self.enemies_missed / self.total_enemies > 0.0:
            self.hud["medal100"].invalid()
            # TODO
            pass
            # signal("scene.hud.medal.100").send(False)

    def start(self):
        super().start()
        self.player.input_enabled = True

    def tick_step_000(self, elapsed):
        game_debugger.lines[0] = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        self.runtime += elapsed
        self.player.tick(elapsed)

        # for enemy in self.em.collidetype(self.player, EntityType.ENEMY):
            # self.player.collision(enemy)
            # enemy.collision(player)

        for pickup in self.em.collidetype(self.player, EntityType.PICKUP):
            pickup.pickedup()

        for enemy, bullets in self.em.collidetypes(EntityType.ENEMY, EntityType.PLAYERBULLET, True).items():
            bullet = bullets[0]
            if not bullet.deleted:
                bullet.delete()
                enemy.hit(bullet)
        
        for bullet in self.em.collidetype(self.player, EntityType.ENEMYBULLET):
            if not bullet.deleted:
                self.player.hit(bullet)
                bullet.delete()

        # game_debugger.timeit_end("tick.hitboxes")

        #Magnet Effect for pickups
        for i, pickup in enumerate(self.em.entities_by_type[EntityType.PICKUP]):
            d = self.player.pos.distance_to(pickup.pos)
            if d < 200:
                p3 = self.player.pos - pickup.pos
                p3.normalize_ip()
                # https://www.geogebra.org/calculator/jy4vgb2b
                v = 0.00001 * (200-d)**2
                pickup.set_magnet_force(p3, v)
            else:
                pickup.set_magnet_force(Vector2(0.0, 0.0), 0.0)

        timed_add = []
        for time_to_add, entity in self.timed_add:
            if time_to_add <= self.runtime:
                current_scene.em.add(entity)
            else:
                timed_add.append((time_to_add, entity))
        self.timed_add = timed_add
    

class Level(Scene):

    """
    """

    level = None

    def __init__(self):
        super().__init__()

        self.paused = False
        # self.timed_add = []

        self.player = PlayerShip()
        self.total_coins = 0
        self.enemies_killed = 0
        # current_player.__wrapped__ = self.player

        self.em.add(self.player)

        self.state_machines = {
            LevelState.STARTING: StartingState(self),
            LevelState.PLAYING: PlayingState(self),
            LevelState.DEAD: DeadState(self),
            LevelState.WON: WonState(self),
        }
        self.state = LevelState.STARTING
        self.state_machine = self.state_machines[self.state]

        self.pause_menu = PauseMenu(SCREEN_SIZE)
        self.pause_menu.enabled = False
        self.em.add(self.pause_menu)

        # game_debugger.timeit_setup("tick.hitboxes", 9, False)
        # game_debugger.timeit_setup("scene.draw", 10, False)

        self.hud = {
            "life1": HUDLife(Vector2(10, -32), 1),
            "life2": HUDLife(Vector2(42, -32), 2),
            "life3": HUDLife(Vector2(74, -32), 3),
            "medal70": HUDMedal70(Vector2(918, -32)),
            "medal100": HUDMedal100(Vector2(950, -32)),
            "medalheart": HUDMedalHeart(Vector2(982, -32)),
        }
        for hud in self.hud.values():
            self.em.add(hud)

        
        #Load The Level Data
        self.load()

        # Cound Total Enemies
        self.total_enemies = len(self.em.entities_by_type[EntityType.ENEMY])
        for time, entity in self.state_machines[LevelState.PLAYING].timed_add:
            if entity.type == EntityType.ENEMY:
                self.total_enemies += 1

    def enemy_missed(self, enemy):
        self.state_machines[LevelState.PLAYING].enemy_missed(enemy)

    def on_start(self):
        self.state_machine.start()

    def add_level_entity(self, time, entity):
        self.state_machines[LevelState.PLAYING].timed_add.append((time, entity))

    def exit(self, data=None):

        if data["condition"] in ["won", "died"]:
            #Save State
            finished = True if data["condition"] == "won" else False
            medalHeart = not self.player.been_hit
            if self.total_enemies > 0:
                enemies = self.enemies_killed / self.total_enemies
            else:
                enemies = 0
            if self.total_coins > 0:
                coins = self.player.coins / self.total_coins
            else:
                coins = 0
            current_app.save_data.set_level_data(self.level, {
                "finished": finished,
                "medalHeart": medalHeart,
                "enemies": enemies,
                "coins": coins,

            })
            current_app.save_data.save()

        current_app.change_scene({
            "scene": "main_menu",
            "return_from_level": True,
            "level_data": {
                "condition": data["condition"],
                "level": self.level,
            },
            "sky_offset": self.background.offset,
        })

    def hud_lives(self, health):
        self.hud["life1"].lives(health)
        self.hud["life2"].lives(health)
        self.hud["life3"].lives(health)
        
    def hud_been_hit(self):
        self.hud["medalheart"].invalid()

    def pressed(self, pressed, elapsed):
        if not self.paused:
            self.player.pressed(pressed, elapsed)
            self.state_machine.pressed(pressed, elapsed)

    def on_paused(self, paused):
        self.paused = paused 

    def pause(self):
        self.paused = True
        self.pause_menu.show()

    def unpause(self):
        self.paused = False 
        self.pause_menu.hide()

    def on_event(self, event, elapsed):
        if self.paused:
            self.pause_menu.on_event(event, elapsed)
            return
        else:
            self.state_machine.on_event(event, elapsed)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self.paused:
                self.pause()
    
    def change_state(self, state):
        self.state_machine.stop()
        self.state = state 
        self.state_machine = self.state_machines[self.state]
        self.state_machine.start()

    def tick(self, elapsed):
        #Don't call super, we will update EntityManager and Backfround ourselves if not paused
        if self.paused:
            self.pause_menu.tick(elapsed)
        else:        
            self.background.tick(elapsed)
            self.em.tick(elapsed)
            self.state_machine.tick(elapsed)

        # game_debugger.lines[0] = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        game_debugger.lines[1] = "Entities:         {}".format(str(len(self.em.entities)))
        game_debugger.lines[2] = "- Particles:      {}".format(str(len(self.em.entities_by_type[EntityType.PARTICLE])))
        game_debugger.lines[3] = "- Enemies:        {}".format(str(len(self.em.entities_by_type[EntityType.ENEMY])))
        game_debugger.lines[4] = "- Enemy Bullets:  {}".format(str(len(self.em.entities_by_type[EntityType.ENEMYBULLET])))
        game_debugger.lines[5] = "- Player Bullets: {}".format(str(len(self.em.entities_by_type[EntityType.PLAYERBULLET])))
        game_debugger.lines[6] = "- Pickups:        {}".format(str(len(self.em.entities_by_type[EntityType.PICKUP])))
        game_debugger.lines[7] = "- GUI:            {}".format(str(len(self.em.entities_by_type[EntityType.GUI])))
        game_debugger.lines[8] = "- DIALOG:         {}".format(str(len(self.em.entities_by_type[EntityType.DIALOG])))

    # @game_debugger.timeit_wrapper("scene.draw")
    def draw(self, elapsed):
        super().draw(elapsed)
