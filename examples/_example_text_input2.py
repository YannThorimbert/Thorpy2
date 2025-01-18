"""
We show here how to declare a text input field.

In order to show how the text input value can be retrived, we also display a text according to the input value.

Just comment out the numerous customization parameters to try different options.
"""
#tags:  text input, TextInput, type text, text insertion, events handling, text inserter

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200,780))
tp.init(screen, tp.themes.theme_human)

text = tp.Text("My name is Bob")
text_input = tp.TextInput("", placeholder="Bob") #create an empty text field
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
# text_input.click_outside_cancel = False #if True and user clicks outside, same as cancelling.
# def dummy_validation():
#    print("Setting the value of the first button to demonstrate how it works.")
#    list_of_elements[0].set_text(text_input.get_value())
text_input.on_validation = lambda:text.set_text("My name is "+text_input.get_value())


list_of_elements = [text_input, text]
box = tp.Box(list_of_elements)
box.center_on(screen)

def at_refresh():
    tp.get_screen().fill((255,255,255))
    # text.set_text("My name is "+text_input.get_value())

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
loop = box.get_updater()
loop.launch(at_refresh)
pygame.quit()

