# What is this ?
Got bored repeating / recreating a menus system for libtcod (python version), so decided to make this reusable library.

# How to use ?
Put this lib (everything but the test.py file) in your libtcod python project, preferably under a package folder you created so you keep your project tidy.

Then, just import the menus, they are useable as is.

# Current state
Massively WIP

# TODO
* Comments / doc
* More menus than the simple one
* Generalisation
* Credits
* Proper tests
* Graphical customization (colors, frame around the menu, ...)
* Menus create their own console (possibly), then we could just call the menu's `get_console` and blit it on the main console / another console
* Migrate the input handling internally to the menu (handle_input fn)
    * Also, could create a "bind" system -> (re)bind keys to menu actions
    * Note: The binds should be shared accross all menu types

# A problem?
Just open a ticket here on github, I'll reply asap.

PS: Contributions / ideas are welcome, of course
