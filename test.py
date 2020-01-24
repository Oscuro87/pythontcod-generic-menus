import tcod
from tcod import event
from menus.basic.listmenu import ListMenu
import config as CFG
from helpers.tools import create_console, paste_console_on


def exit_soft(*args, **kwargs):
    if 'message' in kwargs:
        print(kwargs.get('message'))
    raise SystemExit()


def printout(*args, **kwargs):
    if 'message' in kwargs:
        print(kwargs.get('message'))


if __name__ == "__main__":
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)
    tcod.sys_set_fps(30)
    root_console = tcod.console_init_root(80, 60, "Test menus lib", False)

    menu1_console = create_console(20, 8)
    menu1 = ListMenu(menu1_console)
    # , printout, 1, **{'message': 'label {} activated'})
    menu1.add_element("label 1").set_callback(printout).set_kwargs({'message': 'label 1 activated'})
    menu1.add_element("label 2", printout, 2, **{'message': 'label {} activated'})
    menu1.add_element("quit").set_cb(exit_soft).set_kwargs({'message': 'Exiting normally'})
    menu1.set_active(True)

    while True:
        menu1.draw()
        paste_console_on(menu1_console, root_console, (10, 0))
        tcod.console_flush()

        for evt in event.wait():
            if evt.type == "QUIT":
                exit_soft()
            if evt.type == "KEYDOWN":
                if evt.sym == tcod.event.K_ESCAPE:
                    exit_soft()
                if evt.sym == tcod.event.K_UP:
                    print("up") if CFG.DEBUG_MODE else ""
                    menu1.select_previous_element()
                if evt.sym == tcod.event.K_DOWN:
                    print("down") if CFG.DEBUG_MODE else ""
                    menu1.select_next_element()
                if evt.sym == tcod.event.K_KP_ENTER:
                    menu1.activate_selected_element()

        root_console.clear()
        menu1_console.clear()
