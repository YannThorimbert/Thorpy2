"""We show here how to set up TkDialog for file or folder browsing."""
#tags: TkDialog, file, files, filenames, events handling, folder, directory

#See example_filebrowser for other ways to use TkDialog.
import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen) #bind screen to gui elements and set theme

def my_launch_dialog():
    d2 = tp.TkDialog("Choose a filename :", "filename",
                 filetypes=[("Python files", ".py")], #sequence like [("Excel files", ".xlsx .xls"), ...]
                 initial_dir="./") #initial location of the dialog
    d2.launch_tk_dialog()
    print("You chose:", d2.get_value()) #this will print the chosen filename in the console

button = tp.Button("Click here to launch TK dialog")
button.center_on(screen)
button.at_unclick = my_launch_dialog


# d3.action() #Uncomment this is you want to directly launch the dialog, without having the user to click on it.

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
button.get_updater().launch()
pygame.quit()
