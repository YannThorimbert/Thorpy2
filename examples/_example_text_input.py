"""
We show here how to declare a text input field.

In order to demonstrate how it locks other elements at focus, we declare dummy
buttons along with the actual text input.

Just comment out the numerous customization parameters to try different options.
"""
#tags:  text input, TextInput, type text, text insertion, text inserter

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200,780))
tp.init(screen, tp.themes.theme_game1)

text_input = tp.TextInput("", placeholder="Type text here") #create an empty text field
## *** Customization parameters *** ############################################
# text_input.set_size((100,None)) #set the width of the text field, with auto height
# text_input.placeholder_color = (100,100,100) #font color of the placeholder
# text_input.stop_if_too_large = True #forbid user to add text if text is larger than width
# text_input.max_length = 3 #set the max number of chars
# text_input.adapt_size_if_too_large = False #Be careful if stop_if_too_large is also False...
# text_input.max_size_if_too_large = 200 #set an upper limit for width, in case it becomes larger
# text_input.adapt_parent_if_too_large = False #should parent size adapt also ?
# text_input.keys_validate.append(pygame.K_TAB) #by default, only way to validate input is K_RETURN
# text_input.set_only_numbers() #accept only numbers, including float
# text_input.set_only_integers() #accept only integers
# text_input.set_only_alpha() #accept only alphabetic chars
# text_input.accept_char = lambda x:x=="a" or x=="b"  #custom accept function
# text_input.bck_func = ... #indicate here potential bck function to execute when focus in put on text input
# def dummy_validation():
#    print("Setting the value of the first button to demonstrate how it works.")
#    list_of_elements[0].set_text(text_input.get_value())
# text_input.on_validation = dummy_validation

#create dummy buttons just to see how text input focus make them lock
list_of_elements = [tp.Button("Dummy button "+str(i)) for i in range(4)]
list_of_elements.insert(2,text_input) #add text_input to the elements
box = tp.Box(list_of_elements)
box.center_on(screen)
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
loop = box.get_updater()
##text_input.toggle_focus() #put the focus on the input at the beginning
loop.launch()
pygame.quit()

