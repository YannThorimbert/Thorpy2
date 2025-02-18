"""We show here how to set up TkDialog gor file or folder browsing."""
#tags: TkDialog, file, files, filenames, events handling, folder, directory

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen) #bind screen to gui elements and set theme

d1 = tp.TkDialog("Choose a folder :", "folder")
d2 = tp.TkDialog("Choose a filename :", "filename",
                 filetypes=[("Python files", ".py")], #sequence like [("Excel files", ".xlsx .xls"), ...]
                 initial_dir="./") #initial location of the dialog
d3 = tp.TkDialog("Choose multiple filenames :", "filenames")
d4 = tp.TkDialog("Choose save path :", "save")
group = tp.TitleBox("TkDialog example :", [d1,d2,d3,d4])
group.center_on(screen)

# d3.action() #Uncomment this is you want to directly launch the dialog, without having the user to click on it.

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
    # print(my_dialog.get_value())
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.


#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch()
pygame.quit()
