import os
import pyxel
import json

from enemy import Enemy
from gunshot import Gunshot
from player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
from shared_constants import ENEMY_WIDTH, ENEMY_HEIGHT

enemies = []
bullets = []
gunshots = []

SCENE_TITLE = 0
SCENE_GAME = 1
SCENE_GAMEOVER = 2

debug_mode = False


def load_image(filename):
    filepath = os.path.dirname(os.getcwd())
    pyxel.images[0].load(0, 0, os.path.join(filepath, filename))

    # Enemy and player images
    pyxel.images[0].set(
        0,
        0,
        [
            "00c00c00",
            "0c7007c0",
            "0c7007c0",
            "c703b07c",
            "77033077",
            "785cc587",
            "85c77c58",
            "0c0880c0",
        ],
    )
    pyxel.images[0].set(
        8,
        0,
        [
            "00088000",
            "00ee1200",
            "08e2b180",
            "02882820",
            "00222200",
            "00012280",
            "08208008",
            "80008000",
        ],
    )

    # Bullet gunshots
    pyxel.sounds[0].set("a3a2c1a1", "p", "7", "s", 5)
    pyxel.sounds[1].set("a3a2c2c2", "n", "7742", "s", 10)
    pyxel.sounds[2].set("c3e3g3c4", "t", "5555", "s", 10)


def delete_all_inactive_or_dead_entities():
    for i in range(len(enemies) - 1, -1, -1):
        if not enemies[i].active:
            del enemies[i]

    for i in range(len(bullets) - 1, -1, -1):
        if not bullets[i].active:
            del bullets[i]

    for i in range(len(gunshots) - 1, -1, -1):
        if not gunshots[i].active:
            del gunshots[i]


class Game:
    def __init__(self):
        pyxel.init(120, 160, title="Fall of the Foes")
        filepath = os.path.dirname(os.getcwd())
        with open(os.path.join(filepath, "assets/sounds/music.json"), "rt") as fin:
            self.music = json.loads(fin.read())
        for ch, sound in enumerate(self.music):
            pyxel.sounds[ch].set(*sound)
            pyxel.play(ch, ch, loop=True)
        load_image("assets/images/background.png")
        pyxel.blt(0, 0, 0, 0, 0, 120, 160)
        self.enemy_spawn_timer = 0
        self.scene = SCENE_TITLE
        self.score = 0
        self.player = Player(pyxel.width / 2, pyxel.height - 20)
        self.level = 1
        self.enemy_spawn_rate = 1
        self.max_level = 100
        self.level_duration = 30  # 30 seconds
        self.elapsed_time = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        # Q to quit
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_GAME:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_screen()

        self.elapsed_time += 1 / 30  # 30 FPS
        if self.elapsed_time >= self.level_duration:
            self.elapsed_time = 0
            self.level += 1
            pyxel.play(3, 2)

            if self.level <= self.max_level:
                self.enemy_spawn_rate += 0.5
            else:
                self.scene = SCENE_GAMEOVER
                pyxel.text(43, 66, "YOU WIN", 8)

    def draw(self):
        pyxel.cls(0)
        if self.scene == 0:
            self.draw_title_scene()
        elif self.scene == 1:
            self.draw_play_scene()
        elif self.scene == 2:
            self.draw_gameover_scene()
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)
        pyxel.text(90, 4, f"LEVEL {self.level}", 7)

        if debug_mode:
            pyxel.text(40, 110, "DEBUG MODE", 8)

    @staticmethod
    def draw_title_scene():
        pyxel.text(35, 66, "Fall of the Foes", pyxel.frame_count % 16)

    def draw_play_scene(self):
        self.player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()

    @staticmethod
    def draw_gameover_scene():
        enemies.clear()
        bullets.clear()
        gunshots.clear()
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(41, 126, "IF YOU WANT TO", 10)
        pyxel.text(41, 136, "PLAY AGAIN", 10)
        pyxel.text(41, 146, "PRESS ENTER", 15)

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = 1

    def update_gameover_screen(self):
        cleanup_entities(enemies)
        cleanup_entities(bullets)
        cleanup_entities(gunshots)

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = 1
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            enemies.clear()
            bullets.clear()
            gunshots.clear()
            pyxel.playm(1, loop=True)

    def update_play_scene(self):
        self.enemy_spawn_timer += 1 / 30

        if self.enemy_spawn_timer >= (1 / self.enemy_spawn_rate):
            Enemy(enemies, pyxel.rndi(0, pyxel.width - ENEMY_WIDTH), 0)
            self.enemy_spawn_timer = 0

        for enemy in enemies:
            for bullet in bullets:
                if (
                    enemy.x + enemy.w > bullet.x
                    and bullet.x + bullet.w > enemy.x
                    and enemy.y + enemy.h > bullet.y
                    and bullet.y + bullet.h > enemy.y
                ):
                    enemy.active = False
                    bullet.active = False
                    gunshots.append(
                        Gunshot(
                            gunshots,
                            enemy.x + ENEMY_WIDTH / 2,
                            enemy.y + ENEMY_HEIGHT / 2,
                        )
                    )
                    self.score += 10
                    pyxel.play(3, 1)

        for enemy in enemies:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.active = False
                gunshots.append(
                    Gunshot(
                        gunshots,
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )
                if not debug_mode:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)

        self.player.update(bullets)

        for bullet in bullets:
            bullet.update()

        for enemy in enemies:
            enemy.update(enemies)

        for gunshot in gunshots:
            gunshot.update()

        cleanup_entities(enemies)
        cleanup_entities(bullets)
        cleanup_entities(gunshots)


def cleanup_entities(entities):
    for i in range(len(entities) - 1, -1, -1):
        if not entities[i].active:
            del entities[i]


Game()
