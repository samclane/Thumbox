import os
import sys
import time
import json
import numpy as np
from typing import Literal

import pygame

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

pygame.init()

WIDTH = 72
HEIGHT = 40
SCALE = 10


class Time:
    def tick_ms(self):
        return int(time.time() * 1000)


class Micropython:
    def viper(self, func):
        return func


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
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == self.button:
                            return True
                return False

    def inputPressed(self):
        for event in pygame.event.get():
            pass
        keys = pygame.key.get_pressed()
        for key in self.button.buttom_map:
            if keys[key]:
                return True
        return False

    def dpadPressed(self):
        for event in pygame.event.get():
            pass
        keys = pygame.key.get_pressed()
        return (
            keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
        )

    def dpadJustPressed(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                ]:
                    return True
        return False

    def actionPressed(self):
        return self.buttonA.pressed() or self.buttonB.pressed()

    def actionJustPressed(self):
        return self.buttonA.justPressed() or self.buttonB.justPressed()

    class Sprite:
        def __init__(
            self, width, height, bitmapData, x=0, y=0, key=-1, mirrorX=0, mirrorY=0
        ):
            self.width = width
            self.height = height
            self.bitmapData = bitmapData
            self.x = x
            self.y = y
            self.key = key
            self.mirrorX = mirrorX
            self.mirrorY = mirrorY
            self._frame = 0

        def getFrame(self):
            return self._frame

        def setFrame(self, frame):
            self._frame = frame

    class ThumbyGraphics:
        def __init__(self):
            self.display = self.Display()

        class Display:
            def __init__(self):
                self.width = WIDTH
                self.height = HEIGHT

                self._fps = 0  # non-limiting
                self._surface = pygame.Surface((self.width, self.height))
                self._screen = pygame.display.set_mode(
                    (self.width * SCALE, self.height * SCALE)
                )
                self._brightness = 255
                self.setFont("font5x7.bin", 5, 7, 1)

            @property
            def _white(self):
                return (self._brightness, self._brightness, self._brightness, 255)

            @property
            def _black(self):
                return (0, 0, 0, 255)

            def drawText(self, stringToPrint, x, y, color):
                screenWidth, screenHeight = self._surface.get_size()
                maxChar = self.textCharCount

                for char in stringToPrint:
                    charBitmap = ord(char) - 0x20
                    spriteSurface = pygame.Surface(
                        (self.textWidth, self.textHeight), pygame.SRCALPHA, 32
                    )
                    if 0 <= charBitmap <= maxChar:
                        if (
                            0 <= x + self.textWidth <= screenWidth
                            and 0 <= y + self.textHeight <= screenHeight
                        ):
                            sprite = np.zeros(
                                (self.textHeight, self.textWidth), dtype=bool
                            )
                            self.textBitmapFile.seek(charBitmap * self.textWidth)
                            self.textBitmap = self.textBitmapFile.read(self.textWidth)
                            for i in range(self.textHeight):
                                for j in range(self.textWidth):
                                    sprite[i, j] = (
                                        self.textBitmap[(i >> 3) * self.textWidth + j]
                                        & (1 << (i & 0x07))
                                    ) != 0

                            for i in range(self.textHeight):
                                for j in range(self.textWidth):
                                    if sprite[i, j]:
                                        if color == 0:
                                            spriteSurface.set_at((j, i), self._black)
                                        else:
                                            spriteSurface.set_at((j, i), self._white)

                    self._surface.blit(spriteSurface, (x, y))
                    x += self.textWidth + self.textSpaceWidth

            def setFont(self, fontFilePath, width, height, space):
                self.textBitmapSource = fontFilePath
                self.textBitmapFile = open(self.textBitmapSource, "rb")
                self.textWidth = width
                self.textHeight = height
                self.textSpaceWidth = space
                self.textBitmap = bytearray(self.textWidth)
                self.textCharCount = os.stat(self.textBitmapSource)[6] // self.textWidth

            def update(self):
                upscaled_surface = pygame.transform.scale(
                    self._surface, (self.width * 10, self.height * 10)
                )
                self._screen.blit(upscaled_surface, (0, 0))
                pygame.display.flip()
                if self._fps != 0:
                    pygame.time.wait(1000 // self._fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            def setFPS(self, FPS: int = 0) -> None:
                self._fps = FPS

            def fill(self, color: Literal[0, 1]):
                color = self._white if color == 1 else self._black
                self._surface.fill(color)

            def brightness(self, brightness):
                self._brightness = (brightness / 127) * 255

            def setPixel(self, x: int, y: int, color: Literal[0, 1]):
                if color == 1:
                    self._surface.set_at((x, y), self._white)
                elif color == 0:
                    self._surface.set_at((x, y), self._black)

            def getPixel(self, x, y):
                self._surface.get_at((x, y))

            def drawLine(self, x1, y1, x2, y2, color):
                color = self._white if color == 1 else self._black
                pygame.draw.line(self._surface, color, (x1, y1), (x2, y2))

            def drawFilledRectangle(self, x, y, w, h, color):
                color = self._white if color == 1 else self._black
                pygame.draw.rect(self._surface, color, (x, y, w, h))

            def drawRectangle(self, x, y, w, h, color):
                color = self._white if color == 1 else self._black
                pygame.draw.rect(self._surface, color, (x, y, w, h), 1)

            def blit(self, bitmapData, x, y, width, height, key, mirrorX, mirrorY):
                sprite = Thumby.Sprite(
                    width, height, bitmapData, x, y, key, mirrorX, mirrorY
                )
                self.drawSprite(sprite)

            def blitWithMask(
                self,
                bitmapData,
                x,
                y,
                width,
                height,
                key,
                mirrorX,
                mirrorY,
                maskBitmapData,
            ):
                sprite = Thumby.Sprite(
                    width, height, bitmapData, x, y, key, mirrorX, mirrorY
                )
                maskSprite = Thumby.Sprite(
                    width, height, maskBitmapData, x, y, key, mirrorX, mirrorY
                )
                self.drawSpriteWithMask(sprite, maskSprite)

            def drawSprite(self, sprite):
                surface = pygame.Surface(
                    (sprite.width, sprite.height), pygame.SRCALPHA, 32
                )
                bits_per_byte = 8
                for i in range((sprite.width * (sprite.height + 7) // 8)):
                    byte = sprite.bitmapData[i] if len(sprite.bitmapData) > i else 0
                    for j in range(bits_per_byte):
                        x = i % sprite.width
                        y = 8 * (i // sprite.width) + j

                        # Get the color value from the bytearray (white or black)
                        bit = (byte >> j) & 1
                        color = self._white if bit else self._black
                        if sprite.key == -1:
                            # Set the pixel color on the surface
                            surface.set_at((x, y), color)
                        elif sprite.key != bit:
                            surface.set_at((x, y), color)

                self._surface.blit(
                    surface, (sprite.x, sprite.y), (0, 0, sprite.width, sprite.height)
                )

            def drawSpriteWithMask(self, sprite, maskSprite):
                surface = pygame.Surface(
                    (sprite.width, sprite.height), pygame.SRCALPHA, 32
                )
                mask_surface = pygame.Surface(
                    (sprite.width, sprite.height), pygame.SRCALPHA, 32
                )
                bits_per_byte = 8
                for i in range((sprite.width * (sprite.height + 7) // 8)):
                    byte = sprite.bitmapData[i] if len(sprite.bitmapData) > i else 0
                    mask_byte = (
                        maskSprite.bitmapData[i]
                        if len(maskSprite.bitmapData) > i
                        else 0
                    )

                    for j in range(bits_per_byte):
                        x = i % sprite.width
                        y = 8 * (i // sprite.width) + j

                        # Get the color value from the bytearray (white or black)
                        bit = (byte >> j) & 1
                        mask_bit = (mask_byte >> j) & 1
                        color = self._white if bit else self._black
                        mask_color = self._white if mask_bit else self._black

                        if sprite.key == -1 and maskSprite.key == -1:
                            surface.set_at((x, y), color)
                            mask_surface.set_at((x, y), mask_color)
                        elif sprite.key != bit and maskSprite.key != mask_bit:
                            surface.set_at((x, y), color)
                            mask_surface.set_at((x, y), mask_color)

                surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self._surface.blit(
                    surface, (sprite.x, sprite.y), (0, 0, sprite.width, sprite.height)
                )

    class ThumbyAudio:
        def __init__(self):
            self._freq = 0

        def play(self, freq, duration):
            self._freq = freq
            sample_rate = 44100  # sampling rate in Hz
            samples_mono = (
                np.sin(
                    2 * np.pi * np.arange(sample_rate * duration) * freq / sample_rate
                )
            ).astype(np.float32)
            samples_stereo = np.ascontiguousarray(
                np.vstack((samples_mono, samples_mono)).T
            )
            pygame.mixer.init(frequency=sample_rate, size=-16, channels=2)
            sound = pygame.sndarray.make_sound(samples_stereo)
            sound.play()

        def playBlocking(self, freq, duration):
            self.play(freq, duration)
            while pygame.mixer.get_busy():
                pygame.time.wait(100)

        def stop(self):
            pygame.mixer.music.stop()

        def setEnabled(self, setting):
            if setting:
                pygame.mixer.unpause()
            else:
                pygame.mixer.pause()

        def set(self, freq):
            self._freq = freq

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
