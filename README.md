# Thumbox
## A drop-in Pygame emulator for your Thumby game/app

### What is Thumbox?
Thumbox is designed to aid game devs in distributing their thumby games on Thumby, as well as on Steam. It is a drop-in emulator for your game, which allows you to test your game on your PC. 


### Requirements

Major requirements are 
- Python 3
- Pygame
- numpy

### How do I use it?
1. Download `thumbox.py` and `font5x7.bin` from this repo
2. Place them in the same directory as your `game.py`
    a. If you don't have your game downloaded yet, create a `game.py` file and copy the code from the online emulator into the file.
3. Monkey-patch your game to use Thumbox insead of Thumby, like so:

```python
# imports...
import thumbox

# Create the Emulator object
thumby = thumbox.Thumby()
graphics = thumby.graphics
button = thumby.button
micropython = thumbox.Micropython()
time = thumbox.Time()
# rest of monkey-patching
...
# rest of code
```

To see a full example, check out the `example.py` game in this folder.

### Contributing
We are in development and really need contributors to reach 100% completion. Feel free to reach out to me on Github or make a PR