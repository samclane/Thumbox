# Thumbox
## A drop-in Pygame emulator for your Thumby game/app

### What is Thumbox?
Thumbox is designed to aid game devs in distributing their thumby games on Thumby, as well as on Steam. It is a drop-in emulator for your game, which allows you to test your game on your PC. 


### How do I use it?

1. Download thumbox.py
2. Place it in the same directory as your `game.py`
3. Monkey-patch your game to use Thumbox insead of Thumby, like so:

```python
# rest of imports
...
# import thumby
# Create the Emulator object
thumby = thumbox.Thumby()
graphics = thumby.graphics
button = thumby.button
# rest of monkey-patching
...
# rest of code
```

To see a full example, check out the `example.py` game in this folder.

### Contributing
We are in development and really need contributors to reach 100% completion. Feel free to reach out to me on Github or make a PR