from ast import Delete
from enum import Enum
from re import A
import weakref

from blinker import signal
from pygame import Vector2 
import pygame

from ...enemies.PlaneT8 import EnemyPlaneT8
from .hud import HUDMedal100, HUDMedal70 , HUDMedalHeart, HUDLife
from .level_state import LevelState
from TD.scenes.scene import Scene
from TD.entity import Entity, EntityManager, EntityType, EntityVectorMovement
from TD.gui import GUIPanel, GUILabel, GUISprite
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT, SCREEN_SIZE
from TD.scenes.levels.pause_menu import PauseMenu
from TD.player import PlayerShip
from TD.debuging import game_debugger
from TD.particles.explosions import ExplosionMedium002


class LevelStateMachine:
    def __init__(self, level) -> None:
        self.level = weakref.ref(level)

    @property
    def em(self):
        return self.level().em

    @property
    def player(self):
        return self.level().player

    @property
    def hud(self):
        return self.level().hud

    def start(self):
        pass

    def stop(self):
        pass

    def tick(self, elapsed):
        pass

    def on_event(self, event, elapsed):
        pass

    def pressed(self, pressed, elapsed):
        pass


class DeadState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)

        self.step = 0
        self.step_elapsed = 0.0

    def tick(self, elapsed):
        return super().tick(elapsed)

    def start(self):
        self.player.enabled = False
        self.player.input_enabled = False

        explosion = ExplosionMedium002(self.player.pos)
        explosion.animation_finished_callback = self.on_animation_finished
        signal("scene.add_entity").send(explosion)
        signal("scene.add_entity").send(ExplosionMedium002(self.player.pos + Vector2(-35, 0)))
        signal("scene.add_entity").send(ExplosionMedium002(self.player.pos + Vector2(0, 15)))
        signal("scene.add_entity").send(ExplosionMedium002(self.player.pos + Vector2(-15, -5)))
        signal("scene.add_entity").send(GUISprite(asset_manager.sprites["HUD Hurt"]))
        signal("mixer.play").send("explosion player")

    def tick(self, elapsed):
        self.step_elapsed += elapsed
        if self.step == 1 and self.step_elapsed > 1500:
            signal("scene.exit").send({"condition": "died"})

    def on_animation_finished(self, entity):
        entity.delete()

        self.step += 1
        self.step_elapsed = 0
        self.starting_go = GUILabel("GAME OVER", asset_manager.fonts["lg"], (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        self.starting_go.center_in_rect(SCREEN_RECT)
        signal("scene.add_entity").send(self.starting_go)


class StartingState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)
       
        self.starting_step = 0
        self.starting_elapsed = 0.0
        
    def tick(self, elapsed):
        # Skip for now
        if True:
            self.player.pos.x = 200
            for key, hud in self.hud.items():
                hud.y = 0
            signal("scene.change_state").send(LevelState.PLAYING)
            return

        if self.starting_step == 0:
            
            #Fly in HUD
            for key, hud in self.hud.items():
                hud.y += elapsed * 0.04
                if hud.y >= 0:
                    hud.y = 0
            
            #Fly in Ship 
            self.player.pos.x += elapsed * 0.12
            if self.player.pos.x > 200: 
                self.player.pos.x = 200
                self.starting_step = 1
                self.starting_elapsed = 0.0
                self.starting_go = GUILabel("GO!", asset_manager.fonts["lg"], (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
                self.starting_go.center_in_rect(SCREEN_RECT)
                signal("scene.add_entity").send(self.starting_go)

        elif self.starting_step == 1:
            self.starting_elapsed += elapsed
            if self.starting_elapsed > 500:
                signal("scene.delete_entity").send(self.starting_go)
                signal("scene.change_state").send(LevelState.PLAYING)


class PlayingState(LevelStateMachine):
    def __init__(self, level) -> None:
        super().__init__(level)
        self.runtime = 0.0
        self.timed_add = []

        t8 = EnemyPlaneT8(0)
        t8.path.distance = 100
        t8.velocity = 0.0

        # self.timed_add.append((500, t8))
        # self.timed_add.append((500, EnemyPlaneT8(1)))
        # self.timed_add.append((1000, EnemyPlaneT8(1)))
        # self.timed_add.append((1500, EnemyPlaneT8(1)))
        # from TD.pickups import PickupHeart
        # heart = PickupHeart(Vector2(600,300))
        # self.timed_add.append((0, heart))/
        # import random 
        # from TD.pickups import PickupCoin
        # pos = Vector2(512, 300)
        # for i in range(6):
        #     p = PickupCoin(pos)
        #     signal("scene.add_entity").send(p)


        self.total_enemies = 4
        self.enemies_killed = 0
        self.enemies_missed = 0

        signal("scene.enemy_missed").connect(self.on_enemy_missed)

    def on_enemy_missed(self, enemy):
        self.enemies_missed += 1

    def start(self):
        self.player.input_enabled = True

    def tick(self, elapsed):
        game_debugger.lines[0] = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        self.runtime += elapsed
        self.player.tick(elapsed)

        game_debugger.timeit_start("tick.hitboxes")

        for enemy in self.em.collidetypes(EntityType.PLAYER, EntityType.ENEMY).keys():
            enemy.killed()
            self.enemies_killed += 1
            # self.player.hit()
            self.player.collision()

        for pickup in self.em.collidetypes(EntityType.PLAYER, EntityType.PICKUP).keys():
            pickup.pickedup()

        for enemy, bullets in self.em.collidetypes(EntityType.PLAYERBULLET, EntityType.ENEMY, True).items():
            #First if any bullets are not deleted then kill enemy
            not_deleted = False
            for b in bullets:
                if b.deleted == False: 
                    b.delete()
                    not_deleted = True 
            if not_deleted:
                enemy.killed()
                self.enemies_killed += 1

        for bullets in self.em.collidetypes(EntityType.ENEMYBULLET, EntityType.PLAYER, True).values():
            for b in bullets:
                self.player.hit()
                b.delete()

        game_debugger.timeit_end("tick.hitboxes")

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
                signal("scene.add_entity").send(entity)
            else:
                timed_add.append((time_to_add, entity))
        self.timed_add = timed_add

        if self.enemies_missed / self.total_enemies >= 0.3:
            signal("scene.hud.medal.70").send(False)
        if self.enemies_missed / self.total_enemies > 0.0:
            signal("scene.hud.medal.100").send(False)

    

class Level(Scene):

    """
    Siganls Sent:
    scene.paused -> (paused:boolean)
    
    Signals Listening:
    scene.paused
    scene.exit
    """

    def __init__(self):
        super().__init__()

        self.paused = False
        # self.timed_add = []

        self.state_machines = {
            LevelState.STARTING: StartingState(self),
            LevelState.PLAYING: PlayingState(self),
            LevelState.DEAD: DeadState(self)
        }
        self.state = LevelState.STARTING
        # self.state_machine = DeadState(self)
        self.state_machine = self.state_machines[self.state]
        self.state_machine.start()

        self.pause_menu = PauseMenu(SCREEN_SIZE)
        self.pause_menu.enabled = False
        self.em.add(self.pause_menu)

        signal("scene.paused").connect(self.on_paused)
        signal("scene.exit").connect(self.on_exit)
        signal("scene.change_state").connect(self.change_state)
        
        self.player = PlayerShip()
        self.em.add(self.player)

        game_debugger.timeit_setup("tick.hitboxes", 9, False)
        game_debugger.timeit_setup("scene.draw", 10, False)

        self.hud = {
            "life1": HUDLife(Vector2(10, -32), 1),
            "life2": HUDLife(Vector2(42, -32), 2),
            "life3": HUDLife(Vector2(74, -32), 3),
            "Medal70": HUDMedal70(Vector2(918, -32)),
            "Medal100": HUDMedal100(Vector2(950, -32)),
            "MedalHeart": HUDMedalHeart(Vector2(982, -32)),
        }
        for hud in self.hud.values():
            self.em.add(hud)

    def on_exit(self, data=None):
        print(data)
        signal("game.change_scene").send({
            "scene": "main_menu",
            "return_to_level_select": True,
            "sky_offset": self.background.offset,
        })

    def pressed(self, pressed, elapsed):
        if not self.paused:
            self.player.pressed(pressed, elapsed)
            self.state_machine.pressed(pressed, elapsed)

    def on_paused(self, paused):
        self.paused = paused 

    def on_event(self, event, elapsed):
        if self.paused:
            self.pause_menu.on_event(event, elapsed)
            return
        else:
            self.state_machine.on_event(event, elapsed)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self.paused:
                signal("scene.paused").send(True)
    
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

    @game_debugger.timeit_wrapper("scene.draw")
    def draw(self, elapsed):
        super().draw(elapsed)
