import json
from pathlib import Path
from enum import IntEnum
import datetime 

from pygame import Vector2
import pygame

from TD.config import SCREEN_SIZE, SKY_VELOCITY
from TD.entity import EntityManager
from TD.paths import PathFollower
from TD.editor.globals import current_scene, current_level
from TD.editor import gui 
from TD.assetmanager import asset_manager
from TD.editor.editorassets import editor_assets
from TD.enemies.boss_001 import Boss001
from TD.enemies.boss_002 import Boss002
from TD.enemies.boss_003 import Boss003
from TD.enemies.boss_004 import Boss004
from TD.characters import Christopher, Dialog, Elle, MaiAnh, Sawyer
from TD.scenes.level.dialog import EnemyDialog
from TD.scenes.level.music import Music
from TD.pickups import PickupHeart, PickupCoin, PickupUpgrade
from TD import enemies
from TD import guns 

class LevelEntityType(IntEnum):
    ENEMY_CHAIN = 0
    BOSS = 1
    CONTROL = 2

class LevelEntityControlType(IntEnum):
    MUSIC = 0
    END_LEVEL = 1
    ENEMY_DIALOG = 2

class LevelEntity:
    def __init__(self) -> None:
        self.em = EntityManager()
        self.name = ""
        self._time = 0.0

        #Editor State
        self._editor = False 
        self._enabled = True 
        self._active = False
        self.btn_editor = None 
        self.lbl_editor = None
        self.entities = []
        self._selected = False 
        self.previous_times = []

    def undo_time_move(self):
        if len(self.previous_times) > 0:
            old_time = self.previous_times.pop()
            self._time = old_time

    @property
    def time(self):
        return self._time 

    @time.setter
    def time(self, value):
        self.previous_times.append(self._time)
        self._time = round(value, 2)


    def editor_on_event(self, event, elapsed):
        self.em.on_event(event, elapsed)

    def editor_tick(self, elapsed, start_time, end_time, x_offset, freeze_badge_at_start=False):
        self.em.tick(elapsed)
        # Set Position of BTN
        self.btn_editor.pos.x = self.pixel_offset + x_offset - (self.btn_editor.rect.w / 2)
        if freeze_badge_at_start and self.btn_editor.pos.x < 0:
            if self.has_started and len(self.editor_enemy_points) > 0:
                self.btn_editor.pos.x = 0
        self.btn_editor.pos.y = 250
      
        spacing_width = self.lbl_editor.rect.w + 32
        spacing_height = self.lbl_editor.rect.h + 5

        while True:
            rect = self.btn_editor.rect.copy()
            #Add Extra Height and Width to include the text bubble
            rect.width = spacing_width
            rect.h = spacing_height
            # if self.btn_editor.rect.collidelist(current_scene.badge_rects) == -1:
            if rect.collidelist(current_scene.badge_rects) == -1:
                break 
            else:
                # self.btn_editor.pos.y += 21
                self.btn_editor.pos.y += spacing_height + 5
        # current_scene.badge_rects.append(self.btn_editor.rect)
        current_scene.badge_rects.append(rect)

        #Copy Position to lbl
        self.lbl_editor.pos.x = self.btn_editor.rect.right + 4
        self.lbl_editor.pos.y = self.btn_editor.rect.top

        if current_scene.time < self._time:
            self.active = False
        else:
            self.active = True
        
        if current_scene.hide_badge:
            self.lbl_editor.enabled = False
        else:
            self.lbl_editor.enabled = True

    def editor_draw(self, elapsed, surface, start_time, end_time, x_offset):
        self.em.draw(elapsed, surface)

    def editor_mode(self):
        if not self._editor:
            if self.type == LevelEntityType.ENEMY_CHAIN:
                t = "E"
            elif self.type == LevelEntityType.CONTROL:
                t = "C"
            elif self.type == LevelEntityType.BOSS:
                t = "B"
            else:
                t = "X"
            
            self.btn_editor = gui.ButtonEntityBadge(t, (0, 0), (24, 24), align="center")
            self.btn_editor.on_button_1.append(self.on_btn_editor_clicked)
            self.lbl_editor = gui.Label("", (0,0), (200, 48))
            self.lbl_editor.background_color = None
            # self.lbl_editor.background_color = (255, 0, 255, 127)
            self.lbl_editor.valign = "top"
            self.lbl_editor.render()
            self.em.add(self.btn_editor)
            self.em.add(self.lbl_editor)
            self._editor = True
            self.update_badge()


    def on_btn_editor_clicked(self, btn):
        if self.type == LevelEntityType.ENEMY_CHAIN and not current_scene.gui_level_details.btn_show_chains.toggled:
            return 
        if self.type == LevelEntityType.BOSS and not current_scene.gui_level_details.btn_show_boss.toggled:
            return 
        if self.type == LevelEntityType.CONTROL and not current_scene.gui_level_details.btn_show_controls.toggled:
            return 
        if self.selected:
            current_scene.select_level_entity(None)
        else:
            current_scene.select_level_entity(self)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if value != self._selected:
            self._selected = value
            self.btn_editor.selected = self._selected

    @property
    def enabled(self):
        return self._editor
    
    @enabled.setter
    def enabled(self, value):
        if value != self._enabled:
            self._enabled = value 
            self.btn_editor.enabled = value 
            self.lbl_editor.enabled = value 

    @property
    def pixel_offset(self):
        return self._time * SKY_VELOCITY

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value 
        self.btn_editor.active = value 

    def delete(self):
        current_level.delete(self)


class Boss(LevelEntity):
    def __init__(self) -> None:
        super().__init__()
        self.type = LevelEntityType.BOSS
        self.boss = None

    def add_to_level(self, level):
        if self.boss == "Boss 001":
            entity = Boss001()

        if self.boss == "Boss 002":
            entity = Boss002()

        if self.boss == "Boss 003":
            entity = Boss003()

        if self.boss == "Boss 004":
            entity = Boss004()

        time = self.time
        level.add_level_entity(time, entity)
   
    def load(self, entity_data):
        self.name = entity_data["name"]
        self._time = entity_data["time"]
        if "boss" in entity_data:
            self.boss = entity_data["boss"]

    def save(self):
        """dump data into a jsonable object"""
        return {
            "name": self.name, 
            "time": round(self._time, 2),
            "boss": self.boss,
        }
    
    def update_badge(self):
        name = "---" if self.name in [None, ""] else self.name
        text = "{}".format(name)
        self.lbl_editor.text = text

    def editor_draw(self, elapsed, surface, start_time, end_time, x_offset):
        boss_start_offscreen = 100
        points = [Vector2(self.btn_editor.pos.x + SCREEN_SIZE[0] + boss_start_offscreen, 400),]

        if self.boss == "Boss 001":
            pos = points[0] - Vector2(64,64)
            surface.blit(asset_manager.sprites["Boss 001"][1], pos)
            surface.blit(asset_manager.sprites["Boss 001 laser"][0], pos)

        if self.boss == "Boss 002":
            pos = points[0] - Vector2(64,64)
            surface.blit(asset_manager.sprites["Boss 002"][1], pos)
            surface.blit(asset_manager.sprites["Boss 002 launchers"][0], pos)

        if self.boss == "Boss 003":
            pos = points[0] - (Vector2(71, 69) / 2)
            surface.blit(asset_manager.sprites["Boss 003"][0], pos)
            surface.blit(asset_manager.sprites["Boss 003 laser pod"][0], pos + Vector2(19, 65))
            surface.blit(asset_manager.sprites["Boss 003 rail gun"][0], pos + Vector2(25, 44))

        if self.boss == "Boss 004":
            pos = points[0] - (Vector2(71, 69) / 2)
            surface.blit(asset_manager.sprites["Boss 004 top"][0], pos)
            surface.blit(asset_manager.sprites["Boss 004 bottom"][0], pos + Vector2(0, 0))
            surface.blit(asset_manager.sprites["Boss 004 missiles"][0], pos + Vector2(0, 0))


        super().editor_draw(elapsed, surface, start_time, end_time, x_offset)


class Control(LevelEntity):
    def __init__(self) -> None:
        super().__init__()
        self.type = LevelEntityType.CONTROL
        self.control_type = LevelEntityControlType.MUSIC
        self.arguments = ["" for i in range(4)]


    def add_to_level(self, level):

        if self.control_type == LevelEntityControlType.MUSIC:
            entity = Music(self.arguments[0])
            time = self.time 
            level.add_level_entity(time, entity)

        if self.control_type == LevelEntityControlType.ENEMY_DIALOG:
            if self.arguments[0] == "Sawyer":
                character_class = Sawyer
            elif self.arguments[0] == "Christopher":
                character_class = Christopher
            elif self.arguments[0] == "Elle":
                character_class = Elle
            elif self.arguments[0] == "MaiAnh":
                character_class = MaiAnh

            if self.arguments[1] == "TAUNT_1":
                dialog = Dialog.TAUNT_1
            elif self.arguments[1] == "THREAT":
                dialog = Dialog.THREAT
            elif self.arguments[1] == "PAIN":
                dialog = Dialog.PAIN
            elif self.arguments[1] == "DYING":
                dialog = Dialog.DYING

            entity = EnemyDialog(character_class(dialog))
            time = self.time 
            level.add_level_entity(time, entity)

    def load(self, entity_data):
        self.name = entity_data["name"]
        self._time = entity_data["time"]
        self.control_type = entity_data["control_type"]
        self.arguments = entity_data["arguments"]

    def save(self):
        """dump data into a jsonable object"""
        return {
            "name": self.name, 
            "time": round(self._time, 2),
            "control_type": self.control_type,
            "arguments": [i for i in self.arguments],
        }
    
    def update_badge(self):
        name = "---" if self.name in [None, ""] else self.name
        control_type = "None" if self.control_type == None else LevelEntityControlType(self.control_type).name
        text = "{}: {}".format(name, control_type)
        if self.control_type == LevelEntityControlType.ENEMY_DIALOG:
            text += "\n{}, {}".format(self.arguments[0], self.arguments[1])
        if self.control_type == LevelEntityControlType.MUSIC:
            text += "\n{}".format(self.arguments[0])
        self.lbl_editor.text = text


class EnemyChain(LevelEntity):
    def __init__(self):
        super().__init__()
        self.type = LevelEntityType.ENEMY_CHAIN
        self.enemy = None
        self.count = 5
        self.spacing = 1234.5
        self.enemies = []           # Ref to all Enemies spawned from Chain
        self.chain_lost = False     # Keep track if Chain was Lost, avoid audio repeat
        self.guns = []
        self.gun = None
        self.upgrades = []
        self.hearts = []
        self.coins = [i for i in range(10)]

        self._path_index = 255
        self.path = PathFollower(self._path_index)

        self.editor_has_started = False 
        self.editor_enemy_points = []

    def add_to_level(self, level):

        entity_class = self.get_enemy_class()

        for i in range(self.count):
            entity = entity_class(self._path_index)
            entity.chain = self

            #Coins
            entity.drop_coins = True if i in self.coins else False

            #Drops
            drops = []
            if i in self.hearts:
                drops.append(PickupHeart)
            if i in self.upgrades:
                drops.append(PickupUpgrade)
            entity.drops = drops

            #Guns
            if i in self.guns:
                gun_class = self.get_gun_class()
                gun = gun_class(entity)
                entity.set_gun(gun)

            time = self.time + (i * self.spacing)
            level.add_level_entity(time, entity)
            self.entities.append(entity)

    @property
    def path_index(self):
        return self._path_index

    @path_index.setter
    def path_index(self, value):
        self._path_index = value
        self.path.set_new_path(self._path_index)

    def load(self, chain_data):
        self.name = chain_data["name"] if "coins" in chain_data else ""
        self._time = chain_data["time"] if "coins" in chain_data else 0.0
        self.count = chain_data["count"] if "count" in chain_data else 1
        self.spacing = chain_data["spacing"] if "spacing" in chain_data else 400.0
        self.enemy = chain_data["enemy"]  if "enemy" in chain_data else None
        self.guns = chain_data["guns"] if "guns" in chain_data else []
        self.upgrades = chain_data["upgrades"] if "upgrades" in chain_data else []
        self.hearts = chain_data["hearts"] if "hearts" in chain_data else []
        self.coins = chain_data["coins"] if "coins" in chain_data else []
        self.path_index = chain_data["path_index"] if "path_index" in chain_data else None
        self.gun = chain_data["gun"] if "gun" in chain_data else None 

    def save(self):
        """dump data into a jsonable object"""
        return {
            "name": self.name, 
            "time": round(self._time, 2), 
            "count": self.count, 
            "spacing": round(self.spacing, 2),
            "enemy": self.enemy,
            "guns": [g for g in self.guns], 
            "upgrades": [i for i in self.upgrades],
            "hearts": [i for i in self.hearts],
            "coins": [i for i in self.coins], 
            "path_index": self._path_index,
            "gun": self.gun,
        }
    
    def update_badge(self):
        name = "---" if self.name in [None, ""] else self.name
        enemy_name = "None" if self.enemy == None else self.enemy[5:]
        text = "{}: {}-{}@{:0.0f}".format(name, enemy_name, self.count, self.spacing)

        guns = ""
        hearts = ""
        coins = ""
        upgrades = ""
        for i in range(self.count):
            guns += "\u25CF" if i in self.guns else "\u25CC"
            hearts += "\u25CF" if i in self.hearts else "\u25CC"
            upgrades += "\u25CF" if i in self.upgrades else "\u25CC"
            coins += "\u25CF" if i in self.coins else "\u25CC"

        text += "\ng[{}] u[{}]".format(guns, upgrades)
        text += "\nh[{}] c[{}]".format(hearts, coins)
        self.lbl_editor.text = text

    def get_gun_class(self):
        if self.gun == None:
            return None

        if "T8" in self.gun:
            try:
                gun_class = getattr(guns.T8, self.gun)
            except AttributeError:
                gun_class = None
        elif "CX5B" in self.gun:
            try:
                gun_class = getattr(guns.CX5B, self.gun)
            except AttributeError:
                gun_class = None
        elif "HX7" in self.gun:
            try:
                gun_class = getattr(guns.HX7, self.gun)
            except AttributeError:
                gun_class = None
        elif "D2" in self.gun:
            try:
                gun_class = getattr(guns.D2, self.gun)
            except AttributeError:
                gun_class = None
        elif "BT1" in self.gun:
            try:
                gun_class = getattr(guns.BT1, self.gun)
            except AttributeError:
                gun_class = None
        else:
            gun_class = None

        return gun_class


    def get_enemy_class(self):
        if self.enemy == None:
            return None 
        if "T8" in self.enemy:
            try:
                enemy_class = getattr(enemies.T8, self.enemy)
            except AttributeError:
                enemy_class = None
        elif "CX5B" in self.enemy:
            try:
                enemy_class = getattr(enemies.CX5B, self.enemy)
            except AttributeError:
                enemy_class = None
        elif "HX7" in self.enemy:
            try:
                enemy_class = getattr(enemies.HX7, self.enemy)
            except AttributeError:
                enemy_class = None
        elif "D2" in self.enemy:
            try:
                enemy_class = getattr(enemies.D2, self.enemy)
            except AttributeError:
                enemy_class = None
        elif "BT1" in self.enemy:
            try:
                enemy_class = getattr(enemies.BT1, self.enemy)
            except AttributeError:
                enemy_class = None
        else:
            enemy_class = None

        return enemy_class

    def editor_get_enemy_entity(self):
        enemy_class = self.get_enemy_class()
        if enemy_class != None:
            enemy = enemy_class(self.path_index)
            enemy.path.on_end_of_path = []
            enemy.frame_index = 0
            return enemy
        return None 

    def editor_tick(self, elapsed, start_time, end_time, x_offset):

        enemy = self.editor_get_enemy_entity()

        self.has_started = (current_scene.time - self.time) > 0 
        self.editor_enemy_points = []
        freeze_badge_at_start=False
        # still_on_path = False
        if self.has_started and enemy != None:
            freeze_badge_at_start=True
            for i in range(self.count):
                start_time = current_scene.time - self.time - (self.spacing * i)
                if start_time > 0:
                    enemy.path.distance = start_time * enemy.path.velocity
                    enemy.path.tick(0)
                    pos = enemy.path.pos + Vector2(100, 100)
                    if enemy.path.on_path == True:
                        entity_index = i 
                        self.editor_enemy_points.append((entity_index, pos.copy()))
                        # still_on_path = True

        super().editor_tick(elapsed, start_time, end_time, x_offset, freeze_badge_at_start=freeze_badge_at_start)

    def editor_draw(self, elapsed, surface, start_time, end_time, x_offset):
        
        enemy = self.editor_get_enemy_entity()
        
        points = []
        for point in self.path.data.points:
            point = Vector2(point)
            if self.has_started:
                point += (100, 100)
            else:
                point += (x_offset + self.pixel_offset, 100)
            points.append(point)

        if self._selected:
            c = (220, 67, 67)
        elif current_scene.time < self._time:
            c = (80,80,80)
        else:
            c = (87, 87, 255)

        if len(points) > 1 and (not self.has_started or len(self.editor_enemy_points) > 0):
            pygame.draw.lines(surface, c, False, points)
        else:
            #Still set at least one point to draw enemy sprite at
            points = [self.btn_editor.pos, ]

        if self.has_started:
            for i, editor_enemy_point in enumerate(self.editor_enemy_points):
                enemy_index, point = editor_enemy_point
                if enemy_index in self.upgrades and enemy.glow_surface:
                    surface.blit(enemy.glow_surface, point + enemy.glow_offset + enemy.sprite_offset)
                surface.blit(enemy.surface, point + enemy.sprite_offset)
        else:
            if enemy:
                surface.blit(enemy.surface, points[0] + enemy.sprite_offset)


        super().editor_draw(elapsed, surface, start_time, end_time, x_offset)

class LevelData:
    def __init__(self, filename):
        self.filename = filename if filename != None else ""
        self.total_time = (1 * 60) * 1000

        self.base_path = Path(__file__).parent

        self.level_entities = []
        self.level_entities_by_type = []
        for i in range(len(LevelEntityType)):
            self.level_entities_by_type.append([])

        #editor_mode state
        self._editor = False 

        if filename != None:
            self.load()

    def add_to_level(self, level):
        for entity in self.level_entities:
            entity.add_to_level(level)

    def insert_time(self, start, length):
        self.total_time += length 
        for entity in self.level_entities:
            if entity.time >= start:
                entity.time += length

    def delete_time(self, start, length):
        self.total_time -= length 
        for entity in self.level_entities:
            if entity.time >= start:
                entity.time -= length

    @property
    def total_enemies(self):
        count = 0
        for entity in self.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            count += entity.count
        
        count += len(self.level_entities_by_type[LevelEntityType.BOSS])
        return count 


    def get_save_data(self):
        data = {}
        data["total_time"] = self.total_time

        data["chains"] = []
        for entity in self.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            data["chains"].append(entity.save())

        data["boss"] = []
        for entity in self.level_entities_by_type[LevelEntityType.BOSS]:
            data["boss"].append(entity.save())

        data["controls"] = []
        for entity in self.level_entities_by_type[LevelEntityType.CONTROL]:
            data["controls"].append(entity.save())
        
        return data

    def save_temp(self):
        if self.filename == "":
            filename = Path("No_Name.json")
        else:
            filename = Path(self.filename)

        path = self.base_path / "tmp" / filename.name
        print("Save to Temporary Filename:", filename)
        data = self.get_save_data()
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        return Path("tmp") / filename.name

    def save(self):
        if self.filename == "":
            print("Please Enter A Valid Filename")
            return 
        path = self.base_path / self.filename
        print("Save to Filename:", self.filename)

        data = self.get_save_data()

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def save_backup(self, backup_type=""):
        if self.filename == "":
            filename = Path("No_Name.json")
        else:
            filename = Path(self.filename)

        step = datetime.datetime.now().strftime(".%Y%m%d.%H%M%S")
        if backup_type != "":
            step = step + ".{}".format(backup_type)
        filename = filename.parent / Path(filename.stem + step + filename.suffix)

        path = self.base_path / "backups" / filename.name
        print("Save Level to Backup Filename:", filename)
        data = self.get_save_data()
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        path = self.base_path / self.filename

        if not path.exists():
            import sys
            print("[ERROR] Level File Not Found") 
            print(path)
            sys.exit()


        with open(path, "r") as f:
            data = json.load(f)
        
        self.total_time = data["total_time"]
        for entity_data in data["chains"]:
            e = EnemyChain()
            e.load(entity_data)
            self.add(e)

        for entity_data in data["boss"]:
            e = Boss()
            e.load(entity_data)
            self.add(e)

        for entity_data in data["controls"]:
            e = Control()
            e.load(entity_data)
            self.add(e)
        

    def add(self, entity):
        if entity in self.level_entities:
            raise Exception("Entity already added")
        if self._editor:
            entity.editor_mode()


        self.level_entities.append(entity)
        self.level_entities.sort(key=lambda e: e.time )
        self.level_entities_by_type[entity.type].append(entity)
        self.level_entities_by_type[entity.type].sort(key=lambda e: e.time )


    def delete(self, entity):
        self.level_entities = [e for e in self.level_entities if e != entity]
        entity_type = entity.type
        self.level_entities_by_type[entity_type] = [
            e for e in self.level_entities_by_type[entity_type] if e != entity
        ]

    @property
    def pixel_length(self):
        return int(self.total_time * SKY_VELOCITY)

    def change_length(self, total_time):
        self.total_time = total_time

    def editor_mode(self):
        if not self._editor:
            self._editor = True 
            for entity in self.level_entities:
                entity.editor_mode()
        
    def editor_tick(self, elapsed, start_time, end_time, x_offse, entity_type=None):
        if entity_type == None:
            entities = self.level_entities
        else:
            entities = self.level_entities_by_type[entity_type]

        current_scene.badge_rects = []
        
        for entity in entities:
            if entity.enabled == True:
                if entity.time >= start_time and entity.time <= end_time:
                    entity.enabled = True 
                    entity.editor_tick(elapsed, start_time, end_time, x_offse)
                else:
                    entity.enabled = False 


    def editor_draw(self, elapsed, surface, start_time, end_time, x_offse, entity_type=None):
        if entity_type == None:
            entities = self.level_entities
        else:
            entities = self.level_entities_by_type[entity_type]

        for entity in entities:
            if entity.enabled == True and entity.time >= start_time and entity.time <= end_time:
                entity.editor_draw(elapsed, surface, start_time, end_time, x_offse)

    def editor_on_event(self, event, elapsed, entity_type=None):
        if entity_type == None:
            entities = self.level_entities
        else:
            entities = self.level_entities_by_type[entity_type]

        for entity in entities:
            if entity.enabled == True:
                entity.editor_on_event(event, elapsed)
