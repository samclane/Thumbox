from typing import Literal
import pygame
import time
import os
import json

pygame.init()

# Thumby emulator module

class Thumby:
    def __init__(self):
        self.hardware = self.ThumbyHardware()
        
        self.button = self.ThumbyButton()
        self.buttonA = self.button.buttonA
        self.buttonB = self.button.buttonB
        self.buttonU = self.button.buttonU
        self.buttonD = self.button.buttonD
        self.buttonL = self.button.buttonL
        self.buttonR = self.button.buttonR

        self.graphics = self.ThumbyGraphics()
        
        self.display = self.graphics.display
        # self.sprite = self.ThumbySprite()
        self.audio = self.ThumbyAudio()
        
        self.link = self.ThumbyLink()
        
        self.saveData = self.ThumbySaves()
            
    class ThumbyHardware:
        def reset(self):
            raise NotImplementedError()

    class ThumbyButton:
        def __init__(self):
            self.buttonA = self.Button(pygame.K_COMMA)
            self.buttonB = self.Button(pygame.K_PERIOD)
            self.buttonU = self.Button(pygame.K_UP)
            self.buttonD = self.Button(pygame.K_DOWN)
            self.buttonL = self.Button(pygame.K_LEFT)
            self.buttonR = self.Button(pygame.K_RIGHT)

            self.buttom_map = {
                pygame.K_COMMA: self.buttonA,
                pygame.K_PERIOD: self.buttonB,
                pygame.K_UP: self.buttonU,
                pygame.K_DOWN: self.buttonD,
                pygame.K_LEFT: self.buttonL,
                pygame.K_RIGHT: self.buttonR,
            }

        class Button:
            def __init__(self, button):
                self.button = button

            def pressed(self):
                for event in pygame.event.get():
                    pass
                keys = pygame.key.get_pressed()
                return keys[self.button]

            def justPressed(self):
                raise NotImplementedError()

    def inputPressed(self):
        for event in pygame.event.get():
            pass
        keys = pygame.key.get_pressed()
        for key in self.button.buttom_map:
            if keys[key]:
                return True
        return False

    def dpadPressed(self):
        raise NotImplementedError()

    def dpadJustPressed(self):
        raise NotImplementedError()

    def actionPressed(self):
        raise NotImplementedError()

    def actionJustPressed(self):
        raise NotImplementedError()

    class Sprite:
        def __init__(self, width, height, bitmapData, x=0, y=0, key=-1, mirrorX=0, mirrorY=0):
            self.width = width
            self.height = height
            self.bitmapData = bitmapData
            self.x = x
            self.y = y
            self.key = key
            self.mirrorX = mirrorX
            self.mirrorY = mirrorY

        def getFrame(self):
            raise NotImplementedError()

        def setFrame(self, frame):
            raise NotImplementedError()

    class ThumbyGraphics:
        def __init__(self):
            self.display = self.Display()


        class Display:
            def __init__(self):
                self.width = 72
                self.height = 40

                self._fps = 0  # non-limiting
                self._surface = pygame.Surface((self.width, self.height))
                self._screen = pygame.display.set_mode((self.width * 10, self.height * 10))
                self._font = pygame.font.SysFont("monospace", 8)

            def drawText(self, string, x, y, color):
                # pygame hack
                text = self._font.render(string, False, (255, 255, 255) if color == 1 else (0, 0, 0))
                self._surface.blit(text, (x, y))

            def setFont(self, fontFilePath, width, height, space):
                raise NotImplementedError()

            def update(self):
                upscaled_surface = pygame.transform.scale(self._surface, (self.width * 10, self.height * 10))
                self._screen.blit(upscaled_surface, (0, 0))
                pygame.display.flip()
                if self._fps != 0:
                    time.sleep(1 / self._fps)

            def setFPS(self, FPS: int = 0) -> None:
                self._fps = FPS

            def fill(self, color: Literal[0, 1]):
                color = (255, 255, 255) if color == 1 else (0, 0, 0)
                self._surface.fill(color)

            def brightness(self, brightness):
                raise NotImplementedError()

            def setPixel(self, x: int , y: int, color: Literal[0, 1]):
                if color == 1:
                    self._surface.set_at((x, y), (255, 255, 255))
                elif color == 0:
                    self._surface.set_at((x, y), (0, 0, 0))

            def getPixel(self, x, y):
                self._surface.get_at((x, y))

            def drawLine(self, x1, y1, x2, y2, color):
                color = (255, 255, 255) if color == 1 else (0, 0, 0)
                self._surface.set_at((x1, y1), color)
                self._surface.set_at((x2, y2), color)

            def drawFilledRectangle(self, x, y, w, h, color):
                color = (255, 255, 255) if color == 1 else (0, 0, 0)
                pygame.draw.rect(self._surface, color, (x, y, w, h))

            def drawRectangle(self, x, y, w, h, color):
                color = (255, 255, 255) if color == 1 else (0, 0, 0)
                pygame.draw.rect(self._surface, color, (x, y, w, h), 1)

            def blit(self, bitmapData, x, y, width, height, key, mirrorX, mirrorY):
                sprite = Thumby.Sprite(width, height, bitmapData, x, y, key, mirrorX, mirrorY)
                self.drawSprite(sprite)

            def blitWithMask(self, bitmapData, x, y, width, height, key, mirrorX, mirrorY, maskBitmapData):
                raise NotImplementedError()

            def drawSprite(self, sprite):
                surface = pygame.Surface((sprite.width, sprite.height), pygame.SRCALPHA, 32)
                bits_per_byte = 8
                for i in range((sprite.width * sprite.height) // bits_per_byte + 1):
                    byte = sprite.bitmapData[i] if len(sprite.bitmapData) > i else 0
                    for j in range(bits_per_byte):
                        idx = i * bits_per_byte + j
                        x = idx % sprite.width
                        y = idx // sprite.width

                        # Get the color value from the bytearray (white or transparent)
                        bit = (byte >> j) & 1
                        color = (255, 255, 255, 255) if bit else (0, 0, 0, 0)
                        if sprite.key == -1:
                            # Set the pixel color on the surface
                            surface.set_at((x, y), color)
                        elif sprite.key != bit:
                            surface.set_at((x, y), color)

                self._surface.blit(surface, (sprite.x, sprite.y), (0, 0, sprite.width, sprite.height))

            def drawSpriteWithMask(self, sprite, maskSprite):
                raise NotImplementedError()

    class ThumbyAudio:
        def play(self, freq, duration):
            raise NotImplementedError()

        def playBlocking(self, freq, duration):
            raise NotImplementedError()

        def stop(self):
            raise NotImplementedError()

        def setEnabled(self, setting):
            raise NotImplementedError()

        def set(self, freq):
            raise NotImplementedError()

    class ThumbyLink:
        def send(self, data):
            raise NotImplementedError()

        def receive(self):
            raise NotImplementedError()

    class ThumbySaves:
        def __init__(self):
            self.subdirectoryName = None

            self._data = {}

        def setName(self, subdirectoryName):
            os.makedirs("Saves/" + subdirectoryName, exist_ok=True)
            # creates a persistent.json file for save data to Saves/subdirectoryName/persistent.json
            with open("Saves/" + subdirectoryName + "/persistent.json", "w+") as f:
                f.write("{}")
            self.subdirectoryName = subdirectoryName

        def setItem(self, key, value):
            self._data[key] = value

        def getItem(self, key):
            return self._data[key]

        def hasItem(self, key):
            return key in self._data

        def delItem(self, key):
            del self._data[key]

        def save(self):
            with open("Saves/" + self.subdirectoryName + "/persistent.json", "w+") as f:
                f.write(json.dumps(self._data))

        def getName(self):
            return self.subdirectoryName
