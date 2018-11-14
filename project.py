import pygame, sys, time, math, base64
import numpy as np
import pandas as pd
import googlemaps
import datetime
import openpyxl
from pygame.locals import *

from function import *
from input_box3 import *
from direction import *
from spellchecker import *


pygame.init()

# color
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
BLUE1   = (130, 180, 250)
ORANGE  = (240, 150,  50)
L_GRAY  = (230, 230, 230)
YELLOW  = (255, 255,   0)

# input boxes
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

map = pygame.image.load('ntumap(3).png')
ratio_scale = 1.3
initial_scale = 3309/900 # original width/scree width
food_list = [
    "B & D",
    "Chinese",
    "Fast food",
    "Indian",
    "Japanese",
    "Mala",
    "Mixed Rice",
    "Vegetarian",
    "Western",
    "Others"
]

def main():
    FPS = 60
    global screen, clock, mouse, shiftDown, width, height, space,\
            backspace, max_rating, mouseClicked, mouseClickedUp, scroll_bar_top, scroll_bar_active, dif_bar
    # all stage materials
    width = 900
    height = 636
    stage = 1
    mouse = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('NTU Food')


    # materials in stage 2
    # option part
    selected_box = [False]*len(food_list)
    box_of_choices = []
    num_of_choices = 0
    locked = False
    minBox = TextBox()
    maxBox = TextBox()
    dishBox = TextBox()
    pricerange = [0, 100]
    # rating
    max_rating, current_rating = 5, 0

    # stage 3
    rating_active = False
    price_active = False
    distance_active = False
    official_result = []

    # stage 4: map
    left_image = 0
    top_image = 0
    user_location = "(0,0)"
    current_scale = 0
    place = ""
    hall_place = ""

    # stage 5: display food stalls in canteen
    chosen_canteen = ""
    chosen_stall = ""

    # stage 6: display dishes in stall
    chosen_dish = ""
    chosen_price = 0
    page = 1

    # stage 7:
    gate7 = ""
    direction_error = 0

    # stage 9: log in
    username = TextInput()
    password = TextInput1()
    check9 = 0

    # stage 10: Update
    canteen_fix = TextInput()
    stall_fix = TextInput()
    dish_fix = TextInput()
    canteen_fix_text = ""
    stall_fix_text = ""
    dish_fix_text = ""

    # stage 11, 12, 13: Add, Edit, Remove
    foodtype_fix = TextInput()
    price_fix = TextInput()
    rating_fix = TextInput()
    allowed11 = 0
    allowed12 = 0

    # stage 16: map instruction
    walk_active = 0
    car_active = 0
    bus_active = 0
    direction_list1 = []
    scroll_bar_width = 20
    scroll_bar_height = 80
    scroll_bar_top = height//2.7
    scroll_bar_color_active = (160, 160, 160)
    scroll_bar_color_clicked = (105, 105, 105)
    scroll_bar_region_color = (231, 231, 231)
    scroll_bar_active = False
    gate75 = ""
    # start of loop
    while True:
        mouseClicked = False
        mouseClickedUp = False
        mouseMove = False
        shiftDown = False
        backspace = False
        space = False
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:       scroll_bar_top = max(height//2.7, scroll_bar_top - 30)
                elif event.button == 5:     scroll_bar_top = min(height - scroll_bar_height, scroll_bar_top + 30)
                elif event.button == 1:     mouseClicked = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:       mouseClickedUp = True
            elif event.type == pygame.MOUSEMOTION:
                mouseMove = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
            if event.type == pygame.KEYDOWN:
                if minBox.active and not minBox.locked: minBox.add_chr(pygame.key.name(event.key))
                if maxBox.active and not maxBox.locked: maxBox.add_chr(pygame.key.name(event.key))
                if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
                if event.key == K_SPACE:
                    space = True
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                    if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
                if event.key == pygame.K_BACKSPACE:
                    backspace = True

        # stage 1
        if stage == 1:
            screen.fill((0,167,157))
            cover = pygame.transform.scale(pygame.image.load("cover.jpg"), (900, 636))
            display_image(cover, 0, 0, width, height)
            drawTextCenter("Comic Sans MS", "NTU Food", YELLOW, None, 35, width//2, height//2, True)
            box2 = pygame.Rect(0, 0, 250, 50)
            box2.center = (width//2, height//1.4)
            pygame.draw.rect(screen, (150, 150, 255), box2)
            pygame.draw.rect(screen, BLACK, box2, 2)
            drawTextCenter("Gadugi", "GET START", (255,255,200), None, 35, width//2, height//1.4, True)
            if box2.collidepoint(mouse):
                pygame.draw.rect(screen, (105, 105, 200), box2)
                drawTextCenter("Gadugi", "GET START", (255, 255, 200), None, 37, width//2, height//1.4, True)
                pygame.draw.rect(screen, BLACK, box2, 2)
                if mouseClickedUp:
                    stage = 2
            box3 = pygame.Rect(0, 0, 250, 50)
            box3.center = (width//2, height//1.2)
            pygame.draw.rect(screen, (150, 150, 250), box3)
            pygame.draw.rect(screen, BLACK, box3, 2)
            drawTextCenter("Gadugi", "UPDATE", (255, 255, 200), None, 35, width//2, height//1.2, True)
            if box3.collidepoint(mouse):
                pygame.draw.rect(screen, (105, 105, 250), box3)
                pygame.draw.rect(screen, BLACK, box3, 2)
                drawTextCenter("Gadugi", "UPDATE", (255, 255, 200), None, 37, width//2, height//1.2, True)
                if mouseClicked:
                    stage = 9

        #stage 2
        if stage == 2:
            screen.fill(WHITE)

            # build boxes of options
            for i in range(len(food_list)):
                box_color = WHITE
                box_border = BLACK
                back_box = get_place(i) # postion of box i
                if selected_box[i]:
                    box_color = (255, 162, 100)
                    box_border = (200, 120, 0)
                    if mouseClicked and back_box.collidepoint(mouse):
                        selected_box[i] = not selected_box[i]
                        box_of_choices.remove(i)
                        num_of_choices -= 1
                else:
                    if back_box.collidepoint(mouse):
                        box_color = (153, 217, 234)
                        box_border = (0, 0, 180)
                        if num_of_choices < 3:
                            if mouseClicked:
                                selected_box[i] = not selected_box[i]
                                box_of_choices.append(i)
                                num_of_choices += 1
                        else:
                            drawTextTopLeft("Ebrima", "Maximum number of food reached!", 18, RED, None, width//20, height//5.9)
                drawOptions(i, box_color, box_border)

            # Your current choice:
            drawTextTopLeft("Corbel", "Your type of food: ", 30, BLACK, None, width//20, height//20)

            # box of selected choices
            name_of_choices = [food_list[i] for i in box_of_choices] # get in the input of the search function
            choices =  "   " + ", ".join(name_of_choices)
            font_choice2 = pygame.font.SysFont("Maiandra GD", 25)
            text_choice = font_choice2.render(choices, True, BLACK)
            # box_text_choice = text_choice.get_rect()
            box_of_choices_display = pygame.Rect(width//20, height//10, max(width//1.11, 360), height//15)
            pygame.draw.rect(screen, ORANGE, box_of_choices_display, 3)
            screen.blit(text_choice, box_of_choices_display)

            # budget
            drawTextTopLeft("Corbel", "Your budget:", 30, BLACK, None, width//20, height//1.7)

            # Minimum price
            drawTextTopLeft("Corbel", "Min ($)", 25, BLACK, None, width//15, height//1.53)
            minBox.rect = pygame.Rect(width//6, height//1.55, width//9, minBox.image.get_height())
            minBox.active = get_active(minBox.rect, minBox.active)
            if len(minBox.text) == 6:
                minBox.locked = True
                drawTextTopLeft("Corbel", "Too many characters!", 20, RED, None, width//3.5, height//1.53)
            else: minBox.locked = False
            if minBox.active:
                minBox.color = BLUE
                if backspace and len(minBox.text) > 1: minBox.text = minBox.text[:-1]
            else: minBox.color = BLUE1
            pygame.draw.rect(screen, minBox.color, minBox.rect, 2)
            screen.blit(minBox.image,  minBox.rect)

            # Maximum price
            drawTextTopLeft("Gadugi", "Max ($)", 25, BLACK, None, width//15, height//1.39)
            maxBox.rect = pygame.Rect(width//6, height//1.4, width//9, maxBox.image.get_height())
            maxBox.active = get_active(maxBox.rect, maxBox.active)
            if len(maxBox.text) == 6:
                maxBox.locked = True
                drawTextTopLeft("Gadugi", "Too many characters!", 20, RED, None, width//3.5, height//1.39)
            else: maxBox.locked = False
            if maxBox.active:
                maxBox.color = BLUE
                if backspace and len(maxBox.text) > 1: maxBox.text = maxBox.text[:-1]
            else: maxBox.color = BLUE1
            pygame.draw.rect(screen, maxBox.color, maxBox.rect, 2)
            screen.blit(maxBox.image,  maxBox.rect)

            # rating
            drawTextTopLeft("Gadugi", "Rating: " + str(current_rating), 30, BLACK, None, width//2, height//1.7)
            list_of_star = drawRating(max_rating)
            for j in range(current_rating):
                screen.blit(list_of_star[-2], list_of_star[j])
            for i in range(len(list_of_star[:-2])):
                if list_of_star[i].collidepoint(mouse):
                    for j in range(1+i):
                        screen.blit(list_of_star[-1], list_of_star[j])
                    if mouseClicked:
                        current_rating = i+1
            # let they type their dish
            drawTextTopLeft("Gadugi", "Your dish:", 30, BLACK, None, width//20, height//2.1)
            dishBox.rect = pygame.Rect(width//5, height//2.1, width/1.34, dishBox.image.get_height())
            dishBox.active = get_active(dishBox.rect, dishBox.active)
            if dishBox.active:
                if backspace and len(dishBox.text) > 1: dishBox.text = dishBox.text[:-1]
                if space: dishBox.text += " "
                dishBox.color = BLUE
            else: dishBox.color = BLUE1
            pygame.draw.rect(screen, dishBox.color, dishBox.rect, 2)
            screen.blit(dishBox.image,  dishBox.rect)
            # submit button
            submit = drawTextCenter("Gadugi", "SUBMIT", BLACK, WHITE, 35, width//2, height//1.2, False)
            submit_box = drawBorderCenter(submit[2] + 10, submit[3] + 6, submit.center[0], submit.center[1], BLACK, 3)
            if submit_box.collidepoint(mouse):
                pygame.draw.rect(screen, (100, 100, 255), submit_box)
                pygame.draw.rect(screen, BLACK, submit_box, 3)
                drawTextCenter("Gadugi", "SUBMIT", WHITE, None, 35, width//2, height//1.2, False)
                if mouseClickedUp:
                    stage = 3

        # stage 3: return results to user
        # get input from stage 2: box_of_choices, minBox.text, maxBox.text, dishBox.text, current_rating
        if stage < 3:
            official_result = []
        if stage == 3:
            screen.fill(WHITE)
            result = []
            # FOOD
            list_of_choices = [food_list[i] for i in box_of_choices]
            name_of_choices = ", ".join(list_of_choices)
            drawTextTopLeft("Calibri", "Food: " + process_input(name_of_choices), 25, BLACK, None, width//50, height//30)
            # RATING
            drawTextTopLeft("Calibri", "Rating: " + str(current_rating), 25, BLACK, None, width//2, 3*height//30)
            # DISH
            drawTextTopLeft("Calibri", "Dish: " + process_input(str(dishBox.text)), 25, BLACK, None, width//50, 5*height//30)
            # LOCATION
            locate = drawTextTopLeft("Calibri", "Location: ", 25, BLACK, None, width//2, 5*height//30)
            # SORT BY
            main_sort = drawTextTopLeft("Calibri", "Sort by: ", 25, BLACK, None, width//2, height//30)
            rating_sort = drawTextTopLeft("Calibri", "Rating", 25, BLACK, None, main_sort.right + 5, height//30)
            dash1 = drawTextTopLeft("Calibri", "/", 25, BLACK, None, rating_sort.right + 5, height//30)
            price_sort = drawTextTopLeft("Calibri", "Price", 25, BLACK, None, dash1.right + 5, height//30)
            dash2 = drawTextTopLeft("Calibri", "/", 25, BLACK, None, price_sort.right + 5, height//30)
            distance_sort = drawTextTopLeft("Calibri", "Distance", 25, BLACK, None, dash2.right + 5, height//30)
            choice_border = drawBorderCenter(distance_sort.right - rating_sort.left, 25,
                                            (distance_sort.right + rating_sort.left)//2, (dash1.top + dash1.bottom)//2, WHITE, 1)
            if choice_border.collidepoint(mouse):
                rating_active = get_active(rating_sort, rating_active)
                price_active = get_active(price_sort, price_active)
                distance_active = get_active(distance_sort, distance_active)

            if rating_active: drawTextTopLeft("Calibri", "Rating", 25, BLACK, BLUE1, main_sort.right + 5, height//30)
            if price_active: drawTextTopLeft("Calibri", "Price", 25, BLACK, BLUE1, dash1.right + 5, height//30)
            if distance_active:
                drawTextTopLeft("Calibri", "Distance", 25, BLACK, BLUE1, dash2.right + 5, height//30)
                if place == "":
                    drawTextTopLeft("Calibri", "You haven't choose your location", 25, RED, None, locate.right + 5, 5*height//30)
            if place != "": drawTextTopLeft("Calibri", place, 25, BLACK, None, locate.right + 5, 5*height//30)

            if box_of_choices == [] and minBox.text == " " and maxBox.text == " " and dishBox.text == " ":
                drawTextTopLeft("Calibri", "Price: " + displayValidPrice([None, None]), 25, BLACK, None, width//50, 3*height//30)
                drawNotFound()
            else:
                # PRICE
                price_range = validPrice(minBox.text, maxBox.text)
                drawTextTopLeft("Calibri", "Price: " + displayValidPrice(price_range), 25, BLACK, None, width//50, 3*height//30)
                if price_range == [None, None]:
                    drawNotFound()
                else:
                    result = searchfood(list_of_choices, price_range, current_rating, dishBox.text[1:], df)
                    if result.shape[0] == 0:
                        drawNotFound()
                        if dishBox.text != " ":
                            spellChecker = SpellChecker()
                            recommend = spellChecker.correction(dishBox.text[1:])
                            drawTextTopLeft("Corbel", "Did you mean: ", 30, BLACK, None,width//2 - 200, height//1.2)
                            font4 = pygame.font.SysFont("Calibri", 30, bold = True, italic = True)
                            text4 = font4.render(recommend, True, BLACK)
                            rect4 = text4.get_rect()
                            rect4.x, rect4.y = width//2, height//1.2
                            screen.blit(text4, rect4)
                            if rect4.collidepoint(mouse):
                                text4_active = font4.render(recommend, True, BLUE)
                                screen.blit(text4_active, rect4)
                                if mouseClicked:
                                    dishBox.text = " " + recommend
                                    stage = 3


                    else:
                        if rating_active:
                            result = sort_by_rating(result)
                        if price_active:
                            result = sort_by_price(result)
                        if distance_active and place != "":
                            result = sort_by_location(process_place(place), result, infocan)
                        result = display10(result)
                        canteen_list = result.index.unique()
                        image_list = [infocan.loc[canteen]["Image"] for canteen in canteen_list]
                        chosen_canteen2 = drawCanteenBoxes(canteen_list, image_list, result, distance_active and place != "")

                        if chosen_canteen2 != "": chosen_canteen = chosen_canteen2
                        official_result = result

            drawTextTopLeft("Calibri", "Your canteen: " + chosen_canteen, 25, BLACK, None, width//50, 7*height//30)
            # map button
            map_icon = pygame.transform.scale(pygame.image.load("location.jpg"), (55, 55))
            map_box = map_icon.get_rect()
            map_box.topleft = (width - 55, 26)
            screen.blit(map_icon, map_box)
            if map_box.collidepoint(mouse) and mouseClicked: stage = 4
            stage = backNext(stage, 2, 5, chosen_canteen)

        # stage 4: map
        if stage == 4:
            list_of_boxes, list_of_names = generateMap()
            buttonZone = drawBorderCenter(height//15, height//1.42 - height//1.6 + height//15, width//1.065, (height//1.6 + height//1.42)/2, RED, 1)
            moveZone = drawBorderCenter(3*height/15, 3*height/15, width//1.065, height//1.12, RED, 1)
            confirmZone = drawBorderCenter(600, 46, 300, height - 14, RED, 1)
            screen.fill(WHITE)
            ratio = initial_scale * (ratio_scale ** current_scale)
            map_copy = pygame.transform.scale(map, (int(3309/ratio), int(2339/ratio)))
            left_image, top_image, image_width, image_height = display_image(map_copy, top_image, left_image, width, height)
            processed_mouse = processMouse(top_image, left_image, image_width, image_height, mouse)
            zoomIn = zoomButton(width//1.065, height//1.6, True)
            zoomOut = zoomButton(width//1.065, height//1.42, False)
            if (zoomIn or pressed[pygame.K_LEFTBRACKET]) and current_scale > -10:
                current_scale -= 1
                left_image, top_image, image_width, image_height = zoom(1, top_image, left_image, image_width, image_height)
                time.sleep(0.1)
            if (zoomOut or pressed[pygame.K_RIGHTBRACKET]) and current_scale < 0 :
                current_scale += 1
                left_image, top_image, image_width, image_height = zoom(-1, top_image, left_image, image_width, image_height)
                time.sleep(0.1)
            up, down, left, right = moveButtons()
            if pressed[pygame.K_UP] and (top_image <= 0) or up.collidepoint(mouse) and mouseClicked:
                top_image += 30
                #time.sleep(0.02)
            if pressed[pygame.K_DOWN] and (top_image + image_height >= height) or down.collidepoint(mouse) and mouseClicked:
                top_image -= 30
                time.sleep(0.02)
            if pressed[pygame.K_LEFT] and (left_image <= 0) or left.collidepoint(mouse) and mouseClicked:
                left_image += 30
                time.sleep(0.02)
            if pressed[pygame.K_RIGHT] and (left_image + image_width >= width) or right.collidepoint(mouse) and mouseClicked:
                left_image -= 30
                time.sleep(0.02)

            if mouseClicked:
                if not buttonZone.collidepoint(mouse) and not moveZone.collidepoint(mouse) and not confirmZone.collidepoint(mouse):
                    user_location = str(processed_mouse)
                hall_place = ""
                hall_place = checkMap(list_of_boxes, list_of_names, hall_place, processed_mouse)
            else:
                checkMap(list_of_boxes, list_of_names, hall_place, processed_mouse)

            # return to stage 3 to sort by distance
            proceed = drawTextCenter("Gadugi", "Proceed ?", BLACK, WHITE, 25, 52, height - 14, False)
            if proceed.collidepoint(mouse):
                drawTextCenter("Gadugi", "Proceed ?", WHITE, (0, 100, 100), 25, 52, height - 14, False)
                if mouseClicked:
                    place = user_location
                    stage = 3
            left_location = proceed.right
            text = " Your location: " + user_location + " " + hall_place
            drawTextTopLeft("Gadugi", text, 25, BLACK, WHITE, left_location, height - 30)

        # Show direction instructions


        # stage 5: stalls in canteen
        if stage < 5:
            chosen_stall = ""
        if stage == 5:
            gate5 = ""
            screen.fill(WHITE)
            drawTextTopLeft("Calibri", "Your canteen: " + chosen_canteen, 25, BLACK, None, width//50, height//30)
            drawTextTopLeft("Calibri", "Capacity: " + str(int(infocan.loc[chosen_canteen, "Capacity"])), 25, BLACK, None, width//2, height//30)
            drawTextTopLeft("Calibri", "Telephone: " + infocan.loc[chosen_canteen, "Telephone"], 25, BLACK, None, width//2, 3*height//30)
            drawTextTopLeft("Calibri", "Operating hours: " + infocan.loc[chosen_canteen, "Operating hours"], 25, BLACK, None, width//50, 3*height//30)
            drawTextTopLeft("Calibri", "Address: " + infocan.loc[chosen_canteen, "Address"], 25, BLACK, None, width//50, 5*height//30)
            list_of_stalls1 = official_result.loc[chosen_canteen, "Stall"]
            list_of_stalls = [list_of_stalls1] if type(list_of_stalls1) == str else list_of_stalls1.unique()
            chosen_stall1 = drawStallBoxes(list_of_stalls)
            if chosen_stall1 != "":
                chosen_stall = chosen_stall1

            drawTextTopLeft("Calibri", "Your stall: " + chosen_stall, 25, BLACK, None, width//50, 7*height//30)
            stage = backNext(stage, 3,6, chosen_stall)

        # stage 6: dishes in stall
        if stage < 6:
            chosen_dish = ""
            chosen_price = 0
            page = 1
        if stage == 6:
            screen.fill(WHITE)
            data1 = official_result.loc[chosen_canteen]
            dishes = []
            prices = []
            min_price = max_price = avg_price = 0
            if len(data1.shape) == 1:
                dishes = [data1[2]]
                prices = [data1[3]]
                min_price = max_price = avg_price = data1[3]
            else:
                data2 = data1[data1["Stall"] == chosen_stall]
                dishes = data2["Menu Item"]
                prices = data2["Price"]
                min_price, max_price, avg_price = prices.min(), prices.max(), prices.mean()
            drawTextTopLeft("Calibri", "Your canteen: " + chosen_canteen, 25, BLACK, None, width//50, 2*height//30)
            drawTextTopLeft("Calibri", "Your stall: " + chosen_stall, 25, BLACK, None, width//2, 2*height//30)
            drawTextTopLeft("Calibri", "Minimum price: " + str(min_price), 25, BLACK, None, width//50, 4*height//30)
            drawTextTopLeft("Calibri", "Maximum price: " + str(max_price), 25, BLACK, None, width//3 + width//50, 4*height//30)
            drawTextTopLeft("Calibri", "Average price: " + str(round(avg_price,1)), 25, BLACK, None, width//1.5 + width//50, 4*height//30)
            # menu
            box_width = max(600, width//1.25)
            price_width = max(width//10, 60)
            dish_width = box_width - price_width
            box_height = 2*(height//30)
            x_dish = width//2 - price_width//2
            x_price = x_dish + box_width//2
            drawDishBox("Menu Item", "Price ($)", x_dish, x_price, dish_width, price_width, box_height, 7*(height//30), (150, 150, 255), True)

            list_of_dishes = list(dishes)
            list_of_prices = list(prices)
            total = len(list_of_dishes)
            num_of_boxes = 10
            total_page = math.ceil(total / num_of_boxes)
            page = switchPage(page)
            if page > total_page:
                page = page - total_page
            if page == 0: page = total_page
            menu1 = list_of_dishes[(page-1)*num_of_boxes : page*num_of_boxes]
            price1 = list_of_prices[(page-1)*num_of_boxes : page*num_of_boxes]
            list_of_display_dishes = []
            for i in range(len(menu1)):
                dish_price = drawDishBox(menu1[i], str(price1[i]), x_dish, x_price,
                                            dish_width, price_width, box_height, (9+2*i)*(height//30), WHITE, False)
                list_of_display_dishes.append(dish_price)

            for dish_price in list_of_display_dishes:
                if dish_price[2] != "":
                    chosen_dish = dish_price[2]
                    chosen_price = dish_price[3]
            drawTextCenter("Comic Sans MS", str(page) + "/" + str(total_page), BLACK, None, 20, width//2, 29*(height//30), False)
            drawTextTopLeft("Calibri", "Your dish: " + chosen_dish, 25, BLACK, None, width//50, 0)
            stage = backNext(stage, 5, 7, chosen_dish)

        # stage 7: display all results
        if stage != 7:
            gate7 = ""
            direction_error = 0
        if stage == 7:
            screen.fill(WHITE)
            left1 = width//8
            left2 = width//3
            top = 5
            drawTextTopLeft("Calibri", "Your canteen: ", 25, BLACK, None, left1, top*height//30)
            drawTextTopLeft("Calibri", chosen_canteen, 25, BLACK, None, left2, top*height//30)
            drawTextTopLeft("Calibri", "Your stall: ", 25, BLACK, None, left1, (top+2)*height//30)
            drawTextTopLeft("Calibri", chosen_stall, 25, BLACK, None, left2, (top+2)*height//30)
            drawTextTopLeft("Calibri", "Your dish: ", 25, BLACK, None, left1, (top+4)*height//30)
            drawTextTopLeft("Calibri", chosen_dish, 25, BLACK, None, left2, (top+4)*height//30)
            drawTextTopLeft("Calibri", "Price: ", 25, BLACK, None, left1, (top+6)*height//30)
            drawTextTopLeft("Calibri", "$" + str(chosen_price), 25, BLACK, None, left2, (top+6)*height//30)
            drawTextTopLeft("Calibri", "Address: ", 25, BLACK, None, left1, (top+8)*height//30)
            drawTextTopLeft("Calibri", infocan.loc[chosen_canteen, "Address"], 25, BLACK, None, left2, (top+8)*height//30)
            drawTextTopLeft("Calibri", "Capacity: ", 25, BLACK, None, left1, (top+10)*height//30)
            drawTextTopLeft("Calibri", str(int(infocan.loc[chosen_canteen, "Capacity"])), 25, BLACK, None, left2, (top+10)*height//30)
            drawTextTopLeft("Calibri", "Telephone: ", 25, BLACK, None, left1, (top+12)*height//30)
            drawTextTopLeft("Calibri", infocan.loc[chosen_canteen, "Telephone"], 25, BLACK, None, left2, (top+12)*height//30)
            drawTextTopLeft("Calibri", "Operating hours: ", 25, BLACK, None, left1, (top+14)*height//30)
            drawTextTopLeft("Calibri", infocan.loc[chosen_canteen, "Operating hours"], 25, BLACK, None, left2, (top+14)*height//30)
            current_time = datetime.datetime.now().time()
            checkTime(current_time, chosen_canteen)

            # direction instruction
            # show direction
            font4 = pygame.font.SysFont("Corbel", 30)
            text_srf = font4.render("Show direction", True, BLACK)
            text_box = text_srf.get_rect()
            text_box.center = (width//3, 23*height//30)
            a = pygame.Rect(0, 0, 250, 40)
            a.center = (width//3, 23*height//30)
            pygame.draw.rect(screen, BLUE1, a)
            if a.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, a)
                if mouseClicked:
                    if place == "":
                        direction_error = True
                    else: stage = 7.5
            pygame.draw.rect(screen, BLACK, a, 2)
            screen.blit(text_srf, text_box)
            if direction_error:
                drawTextTopLeft("Calibri", "We haven't got your location", 25, RED, None, left1, 25*height//30)
            # go to map:
            text_srf1 = font4.render("Go to map", True, BLACK)
            text_box1 = text_srf1.get_rect()
            text_box1.center = (width//1.5, 23*height//30)
            b = pygame.Rect(0, 0, 250, 40)
            b.center = (width//1.5, 23*height//30)
            pygame.draw.rect(screen, BLUE1, b)
            if b.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, b)
                if mouseClicked:
                    stage = 4
            pygame.draw.rect(screen, BLACK, b, 2)
            screen.blit(text_srf1, text_box1)


            box11 = pygame.Rect(width - 110, 0, 110, 2)
            pygame.draw.rect(screen, WHITE, box11, 2)
            if mouseClicked and not box11.collidepoint(mouse): gate7 = "a"
            stage = backNext(stage, 6, 8, gate7)

        if stage < 7.5:
            gate45= ""
            direction_list1 = []
        if stage == 7.5:
            screen.fill(WHITE)
            box11 = pygame.Rect(width - 110, 0, 110, 20)
            # create buttons: walking, bus, transit(walking + bus)
            # user clicks 1 of them to set their travelling mode

            drawTextCenter("Calibri", "BACK", BLACK, None, 25, width - 50, 20, True)

            size = (100, 100)
            y_image = height//8
            # walk
            walk_image = pygame.transform.scale(pygame.image.load("walk.png"), size)
            walk_image_rect = walk_image.get_rect()
            walk_circle = pygame.Rect(0, 0, 150, 150)
            walk_image_rect.center = walk_circle.center = (width//4, y_image)
            if walk_active != 2:
                if walk_circle.collidepoint(mouse): walk_active = 1
                else: walk_active = 0
            if mouseClickedUp:
                if walk_image_rect.collidepoint(mouse): walk_active = 2
                else:
                    if scroll_bar_active == False and not box11.collidepoint(mouse): walk_active = 0


            # car
            car_image = pygame.transform.scale(pygame.image.load("car.png"), size)
            car_image_rect = car_image.get_rect()
            car_circle = pygame.Rect(0, 0, 150, 150)
            car_image_rect.center = car_circle.center = (width//2, y_image)

            if car_active != 2:
                if car_circle.collidepoint(mouse): car_active = 1
                else: car_active = 0
            if mouseClickedUp:
                if car_image_rect.collidepoint(mouse): car_active = 2
                else:
                    if scroll_bar_active == False and not box11.collidepoint(mouse): car_active = 0

            # bus (transit)
            bus_image = pygame.transform.scale(pygame.image.load("bus.png"), size)
            bus_image_rect = bus_image.get_rect()
            bus_circle = pygame.Rect(0, 0, 150, 150)
            bus_image_rect.center = bus_circle.center = (width//(4/3), y_image)
            if bus_active != 2:
                if bus_circle.collidepoint(mouse): bus_active = 1
                else: bus_active = 0
            if mouseClickedUp:
                if bus_image_rect.collidepoint(mouse): bus_active = 2
                else:
                    if scroll_bar_active == False and not box11.collidepoint(mouse): bus_active = 0

            chosen = walk_active == 2 or car_active == 2 or bus_active == 2
            if chosen:
                gate75 = "a"
                if place == "":
                    drawTextCenter("Calibri", "You haven't chose your location!", BLUE, None, 30, width//2, height//3.1, False)
                else:
                    x, y = process_place(place)
                    lat_lng = pixeltolatlng(x, y) # return tuple
                    address1 = lat_lng
                    address2 = chosen_canteen + "Nanyang Technological University"
                    y_dif = 40
                    y_top = height//2.7
                    steps = []

                    if walk_active == 2:
                        directions_result = get_directions(address1, address2, "walking")
                        steps = get_steps_not_transit(directions_result)

                    elif car_active == 2:
                        directions_result = get_directions(address1, address2, "driving")
                        steps = get_steps_not_transit(directions_result)
                    elif bus_active == 2:
                        directions_result = get_directions(address1, address2, "transit")
                        steps = get_steps_transit(directions_result)
                    elif walk_active != 2 and car_active != 2 and bus_active != 2:
                        direction_list = []
                    direction_list1 = directionList(steps, width//6, width - width//6)
                    print(direction_list1)
                    num = len(direction_list1)
                    end = max(height, 60 + num * y_dif)
                    top = height//2.7
                    if end > height:
                        scroll_bar_left = width//1.2 + 60
                        scroll_bar = pygame.Rect(scroll_bar_left, scroll_bar_top, scroll_bar_width, scroll_bar_height)
                        scroll_bar_region = pygame.Rect(scroll_bar_left, height//2.7, scroll_bar_width, height)
                        scroll_bar_color = (200, 200, 200)
                        end_view_point = end - y_top
                        end_scroll_bar = (height - y_top) - scroll_bar_height
                        ratio = (scroll_bar.y - y_top) / end_scroll_bar
                        top = end_view_point * ratio + y_top
                        pygame.draw.rect(screen, scroll_bar_region_color, scroll_bar_region)
                        if scroll_bar.collidepoint(mouse):
                            scroll_bar_color = scroll_bar_color_active
                            if mouseClicked:
                                scroll_bar_active = True
                                dif = mouse[1] - scroll_bar_top
                        if mouseClickedUp:
                            scroll_bar_active = False
                        if mouseMove and scroll_bar_active:
                            scroll_bar_top = max(y_top, min(mouse[1] - dif, height - scroll_bar_height))
                        if scroll_bar_active:
                            scroll_bar_color = scroll_bar_color_clicked

                        scroll_bar = pygame.Rect(scroll_bar_left, scroll_bar_top, scroll_bar_width, scroll_bar_height)
                        pygame.draw.rect(screen, scroll_bar_color, scroll_bar)

                    for index, text in enumerate(direction_list1):
                        font1 = pygame.font.SysFont("Calibri", 25)
                        direction1 = font1.render(text, True, BLACK, None)
                        box1 = pygame.Rect(0,0, 300, 50)
                        y_pos = 2*y_top - top + index*(y_dif) + 10
                        box1.x, box1.y = width//6, y_pos
                        screen.blit(direction1, box1)

            cover_box = pygame.Rect(0,0, width, height//2.7)
            if not chosen:
                gate75 = ""
                drawTextCenter("Calibri", "Please click one.", BLUE, None, 30, width//2, height//3.1, False)
            # draw walk icon
            pygame.draw.rect(screen, WHITE, cover_box)
            screen.blit(walk_image, walk_image_rect)
            if walk_active == 1:
                pygame.draw.ellipse(screen, BLACK, walk_circle, 3)
            elif walk_active == 2:
                pygame.draw.ellipse(screen, BLUE, walk_circle, 3)
            # draw car icon
            screen.blit(car_image, car_image_rect)
            if car_active == 1:
                pygame.draw.ellipse(screen, BLACK, car_circle, 3)
            elif car_active == 2:
                pygame.draw.ellipse(screen, BLUE, car_circle, 3)
            # draw transit icon
            screen.blit(bus_image, bus_image_rect)
            if bus_active == 1:
                pygame.draw.ellipse(screen, BLACK, bus_circle, 3)
            elif bus_active == 2:
                pygame.draw.ellipse(screen, BLUE, bus_circle, 3)

            stage = backNext(stage, 7, 8, gate75)

        # Do you want to update infomation ?
        if stage == 8:
            screen.fill(WHITE)
            box_width = 120
            box_height = 60
            font1 = pygame.font.SysFont("Comic Sans MS", 40)
            # YES
            center1 = (width//2 - 70, height//2)
            yes_box = pygame.Rect(0,0,box_width, box_height)
            yes_box.center = center1
            pygame.draw.rect(screen, (150, 200, 255), yes_box)
            if yes_box.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, yes_box)
                if mouseClicked:
                    stage = 9
            pygame.draw.rect(screen, BLACK, yes_box, 1)
            drawTextCenter("Comic Sans MS", "YES", BLACK, None, 40, width//2 - 70, height//2, False)
            # NO
            center2 = (width//2 + 70, height//2)
            no_box = pygame.Rect(0,0,box_width, box_height)
            no_box.center = center2
            pygame.draw.rect(screen, (150, 200, 255), no_box)
            if no_box.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, no_box)
                if mouseClicked:
                    stage = 1
            pygame.draw.rect(screen, BLACK, no_box, 1)
            drawTextCenter("Comic Sans MS", "NO", BLACK, None, 40, width//2 + 70, height//2, False)
            # text
            drawTextCenter("Corbel", "Do you want to update infomation?", BLACK, None, 45, width//2, height//2 - 140, False)

        # log in
        if stage != 9:
            check9 = 0
        if stage == 9:
            screen.fill(WHITE)
            font1 = pygame.font.SysFont("Calibri", 30)
            drawTextCenter("Corbel", "You must log in to update information!", RED, None, 45, width//2, height//4, False)

            # username
            box1 = drawTextTopLeft("Calibri", "Username: ", 30, BLACK, None, width//3.5, height//2.3)
            username_rect = pygame.Rect(box1.right + 20, height//2.3, 300, 30)
            pygame.draw.rect(screen, BLACK, username_rect, 2)
            username.rect = username_rect
            username.update(events)
            screen.blit(username.get_surface(), username.rect)
            # password
            drawTextTopLeft("Calibri", "Password: ", 30, BLACK, None, width//3.5, height//2)
            password_rect = pygame.Rect(box1.right + 20, height//2, 300, 30)
            pygame.draw.rect(screen, BLACK, password_rect, 2)
            password.rect = password_rect
            password.update(events)
            screen.blit(password.get_surface(), password.rect)
            # encode username and password
            real_username = username.input_string[1:]
            encoded_username = base64.b64encode(real_username.encode())
            real_password = password.input_string
            encoded_password = base64.b64encode(real_password.encode())

            admin_accounts = list(admin_data["Admin"])
            passwords = list(admin_data["Password"])
            check1 = check_account(str(encoded_username), str(encoded_password), admin_accounts, passwords)

            login_button = pygame.Rect(0, 0, 200, 50)
            login_button.center = (width//2, height//1.5)
            pygame.draw.rect(screen, (116, 153, 228), login_button)
            if login_button.collidepoint(mouse):
                pygame.draw.rect(screen, (66, 103, 178), login_button)
                if mouseClicked:
                    if check1 == 0: check9 = 2
                    else: stage = 10
            drawTextCenter("Gadugi", "LOG IN", WHITE, None, 40, width//2, height//1.5, True)
            pygame.draw.rect(screen, BLACK, login_button, 2)
            if check9 == 2:
                drawTextTopLeft("Corbel", "Invalid username or password!", 20, RED, None, width//3.5, height//1.8)

            home = pygame.Rect(width - 100, 0, 100, 40)
            pygame.draw.rect(screen, (180, 180, 180), home)
            if home.collidepoint(mouse):
                pygame.draw.rect(screen, L_GRAY, home)
                if mouseClickedUp:
                    stage = 1
            pygame.draw.rect(screen, BLACK, home, 1)
            drawTextCenter("Calibri", "HOME", BLACK, None, 25, width - 50, 20, True)

        if stage < 10:
            canteen_fix_text = ""
            stall_fix_text = ""
            dish_fix_text = ""
        if stage != 10:
            canteen_fix.active = False
            stall_fix.active = False
            dish_fix.active = False
        if stage == 10:
            screen.fill(WHITE)
            left = width//10
            top = height//5
            gap = height//10

            box1 = drawTextTopLeft("Calibri", "Canteen: ", 30, BLACK, None, left, top)
            canteen_rect = pygame.Rect(box1.right + 20, top, width//(4/3) - box1.w, 30)
            pygame.draw.rect(screen, BLACK, canteen_rect, 2)
            canteen_fix.rect = canteen_rect
            canteen_fix.update(events)
            screen.blit(canteen_fix.get_surface(), canteen_fix.rect)

            drawTextTopLeft("Calibri", "Stall: ", 30, BLACK, None, left, top + gap)
            stall_rect = pygame.Rect(box1.right + 20, top + gap, width//(4/3) - box1.w, 30)
            pygame.draw.rect(screen, BLACK, stall_rect, 2)
            stall_fix.rect = stall_rect
            stall_fix.update(events)
            screen.blit(stall_fix.get_surface(), stall_fix.rect)

            drawTextTopLeft("Calibri", "Dish: ", 30, BLACK, None, left, top + gap*2)
            dish_rect = pygame.Rect(box1.right + 20, top + gap*2, width//(4/3) - box1.w, 30)
            pygame.draw.rect(screen, BLACK, dish_rect, 2)
            dish_fix.rect = dish_rect
            dish_fix.update(events)
            screen.blit(dish_fix.get_surface(), dish_fix.rect)

            button = pygame.Rect(0,0,width//5, height//10)
            y_pos = height//1.5
            def drawButton(stage, text, x_pos, color):
                new_stage = stage
                new_button = button
                new_button.center = (x_pos, y_pos)
                pygame.draw.rect(screen, color, new_button)
                if new_button.collidepoint(mouse):
                    pygame.draw.rect(screen, ORANGE, new_button)
                    if mouseClickedUp:
                        if text == "ADD":
                            new_stage = 11
                        elif text == "EDIT":
                            new_stage = 12
                        elif text == "REMOVE":
                            new_stage = 13
                pygame.draw.rect(screen, BLACK, new_button, 2)
                drawTextCenter("Corbel", text, BLACK, None, 40, x_pos, y_pos, False)
                return new_stage

            stage_add = drawButton(stage, "ADD", width//4, (150, 255, 150))
            stage_edit = drawButton(stage, "EDIT", width//2, BLUE1)
            stage_remove = drawButton(stage, "REMOVE", width//(4/3), (255, 150, 150))
            canteen_fix_text = canteen_fix.input_string[1:]
            stall_fix_text = stall_fix.input_string[1:]
            dish_fix_text = dish_fix.input_string[1:]
            if canteen_fix_text == "" or stall_fix_text == "" or dish_fix_text == "":
                drawTextCenter("Calibri", "Please fill in all 3 boxes.", BLUE, None, 25, width//2, height//2, False)
            else:
                stage = max(stage_add, stage_edit, stage_remove)


       # ADD
        if stage != 11:
            allowed11 = 0
        if stage not in [11, 12, 13]:
            foodtype_fix.input_string = " "
            price_fix.input_string = " "
            rating_fix.input_string = " "
        if stage == 11:
            screen.fill(WHITE)
            stage = backUpdate(stage)
            info = (canteen_fix_text, stall_fix_text, dish_fix_text)
            result = search(ws, info)
            if result != []:
                drawTextCenter("Corbel", "Oops! It looks like we already have your suggestion.", BLACK, None, 30, width//2, height//6, False)
                folder1 = pygame.image.load("folder1.png")
                folder1_rect = folder1.get_rect()
                folder1_rect.center = (width//2, height//1.7)
                screen.blit(folder1, folder1_rect)
            else:
                box1 = drawTextTopLeft("Calibri", "Food Type: ", 30, BLACK, None, left, top)
                foodtype_rect = pygame.Rect(box1.right + 20, top, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, foodtype_rect, 2)
                foodtype_fix.rect = foodtype_rect
                foodtype_fix.update(events)
                screen.blit(foodtype_fix.get_surface(), foodtype_fix.rect)

                drawTextTopLeft("Calibri", "Price: ", 30, BLACK, None, left, top + gap)
                price_rect = pygame.Rect(box1.right + 20, top + gap, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, price_rect, 2)
                price_fix.rect = price_rect
                price_fix.update(events)
                screen.blit(price_fix.get_surface(), price_fix.rect)

                drawTextTopLeft("Calibri", "Rating: ", 30, BLACK, None, left, top + gap*2)
                rating_rect = pygame.Rect(box1.right + 20, top + gap*2, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, rating_rect, 2)
                rating_fix.rect = rating_rect
                rating_fix.update(events)
                screen.blit(rating_fix.get_surface(), rating_fix.rect)

                a1 = price_fix.input_string[1:].replace(".", "", 1)
                a2 = rating_fix.input_string[1:]

                check = a1.isdigit() and a2.isdigit() and int(a2) in range(0,6)

                submit = pygame.Rect(0, 0, 200, 50)
                submit.center = (width//2, height//1.5)
                pygame.draw.rect(screen, BLUE1, submit)
                if submit.collidepoint(mouse):
                    pygame.draw.rect(screen, ORANGE, submit)
                    if mouseClickedUp:
                        if check:
                            add(ws,[info[0],foodtype_fix.input_string[1:], info[1], info[2], float(price_fix.input_string[1:]), int(a2)])
                            wb.save('Canteen_db - Copy.xlsx')
                            stage = 14
                        else:
                            allowed11 = 2
                pygame.draw.rect(screen, BLACK, submit, 2)
                drawTextCenter("Corbel", "SUBMIT", BLACK, None, 40, width//2, height//1.5, True)
                if allowed11 == 2:
                    drawTextCenter("Calibri", "Please check your inputs again.", BLUE, None, 25, width//2, height//2, False)

        # EDIT
        if stage != 12:
            allowed12 = 0
        if stage == 12:
            screen.fill(WHITE)
            stage = backUpdate(stage)
            info = (canteen_fix_text, stall_fix_text, dish_fix_text)
            result = search(ws, info)
            if result == []:
                file_not_found = pygame.image.load("filenotfound.png")
                file_not_found_rect = file_not_found.get_rect()
                file_not_found_rect.center = (width//2, height//2)
                screen.blit(file_not_found, file_not_found_rect)
            else:
                box1 = drawTextTopLeft("Calibri", "Food Type: ", 30, BLACK, None, left, top)
                foodtype_rect = pygame.Rect(box1.right + 20, top, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, foodtype_rect, 2)
                foodtype_fix.rect = foodtype_rect
                foodtype_fix.update(events)
                screen.blit(foodtype_fix.get_surface(), foodtype_fix.rect)

                drawTextTopLeft("Calibri", "Price: ", 30, BLACK, None, left, top + gap)
                price_rect = pygame.Rect(box1.right + 20, top + gap, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, price_rect, 2)
                price_fix.rect = price_rect
                price_fix.update(events)
                screen.blit(price_fix.get_surface(), price_fix.rect)

                drawTextTopLeft("Calibri", "Rating: ", 30, BLACK, None, left, top + gap*2)
                rating_rect = pygame.Rect(box1.right + 20, top + gap*2, width//(4/3) - box1.w, 30)
                pygame.draw.rect(screen, BLACK, rating_rect, 2)
                rating_fix.rect = rating_rect
                rating_fix.update(events)
                screen.blit(rating_fix.get_surface(), rating_fix.rect)

                a1 = price_fix.input_string[1:].replace(".", "", 1)
                a2 = rating_fix.input_string[1:]

                check = a1.isdigit() and a2.isdigit() and int(a2) in range(0,6)

                submit = pygame.Rect(0, 0, 200, 50)
                submit.center = (width//2, height//1.5)
                pygame.draw.rect(screen, BLUE1, submit)
                if submit.collidepoint(mouse):
                    pygame.draw.rect(screen, ORANGE, submit)
                    if mouseClickedUp:
                        if check:
                            edit(ws, result[0],foodtype_fix.input_string[1:],float(price_fix.input_string[1:]), int(a2))
                            wb.save('Canteen_db - Copy.xlsx')
                            stage = 14
                        else:
                            allowed12 = 2
                pygame.draw.rect(screen, BLACK, submit, 2)
                drawTextCenter("Corbel", "SUBMIT", BLACK, None, 40, width//2, height//1.5, True)
                if allowed12 == 2:
                    drawTextCenter("Calibri", "Please check or type your inputs again.", BLUE, None, 25, width//2, height//2, False)
                    
        # REMOVE
        if stage == 13:
            screen.fill(WHITE)
            stage = backUpdate(stage)
            drawTextCenter("Calibri", "Are you sure ?", BLACK, None, 40, width//2, height//2, False)
            info = (canteen_fix_text, stall_fix_text, dish_fix_text)
            result = search(ws, info)
            submit = pygame.Rect(0, 0, 200, 50)
            submit.center = (width//2, height//1.5)
            pygame.draw.rect(screen, BLUE1, submit)
            if submit.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, submit)
                if mouseClickedUp:
                    if len(result) > 0:
                        ws.delete_rows(result[0])
                        wb.save('Canteen_db - Copy.xlsx')
                    stage = 14
            pygame.draw.rect(screen, BLACK, submit, 2)
            drawTextCenter("Corbel", "SUBMIT", BLACK, None, 40, width//2, height//1.5, True)

        # Continue ???
        if stage == 14:
            screen.fill(WHITE)
            box_width = 120
            box_height = 60
            font1 = pygame.font.SysFont("Comic Sans MS", 40)
            drawTextCenter("Corbel", "Do you want to update again?", BLACK, None, 40, width//2, height//2.5, True)
            # YES
            center1 = (width//2 - 70, height//2)
            yes_box = pygame.Rect(0,0,box_width, box_height)
            yes_box.center = center1
            pygame.draw.rect(screen, (150, 200, 255), yes_box)
            if yes_box.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, yes_box)
                if mouseClicked:
                    stage = 10
            pygame.draw.rect(screen, BLACK, yes_box, 1)
            drawTextCenter("Comic Sans MS", "YES", BLACK, None, 40, width//2 - 70, height//2, False)
            # NO
            center2 = (width//2 + 70, height//2)
            no_box = pygame.Rect(0,0,box_width, box_height)
            no_box.center = center2
            pygame.draw.rect(screen, (150, 200, 255), no_box)
            if no_box.collidepoint(mouse):
                pygame.draw.rect(screen, ORANGE, no_box)
                if mouseClicked:
                    stage = 15
            pygame.draw.rect(screen, BLACK, no_box, 1)
            drawTextCenter("Comic Sans MS", "NO", BLACK, None, 40, width//2 + 70, height//2, False)

        # Thank you
        if stage == 15:
            screen.fill((110, 205, 227))
            thankyou = pygame.image.load("thankyou.png")
            thankyou_rect = thankyou.get_rect()
            thankyou_rect.center = (width//2, height//2)
            screen.blit(thankyou, thankyou_rect)
            box = drawTextCenter("Calibri", "Home", YELLOW, None, 40, width//2, height//1.5, False)
            if box.collidepoint(mouse):
                screen.blit(thankyou, thankyou_rect)
                box = drawTextCenter("Calibri", "Home", YELLOW, None, 45, width//2, height//1.5, False)
                if mouseClickedUp:
                    stage = 1




        pygame.display.update()
        clock.tick(FPS)

def get_place(index):
    row = index//5
    col = index % 5
    minx = width//20
    miny = height//4.5
    box_width = max(100, width//6)
    box_height = max(50, height//12)
    margin = min(15, width//50)
    x_pos = minx + col*(box_width + margin)
    y_pos = miny + row*(box_height + margin)
    back_box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    return back_box

def drawBoxOption(box, color, border):
    x, y, width1, height1 = box
    radius = min(width, height)//50
    drawRoundedRectangle(border, x, y, width1, height1, radius)
    drawRoundedRectangle(color, x+2, y+2, width1-4, height1-4, radius-2)

def drawRoundedRectangle(color, x, y, width, height, radius):
    diameter = 2*radius
    pygame.draw.rect(screen, color, (x+radius, y, width - diameter, radius))
    pygame.draw.rect(screen, color, (x, y + radius, width, height - diameter))
    pygame.draw.rect(screen, color, (x+radius, y + height - radius, width - diameter, radius))
    pygame.draw.ellipse(screen, color, (x, y, diameter, diameter))                       # top-left quarter circle
    pygame.draw.ellipse(screen, color, (x + width - diameter, y, diameter, diameter))   # top-right quarter circle
    pygame.draw.ellipse(screen, color, (x, y + height - diameter, diameter, diameter))  # bot-left quarter circle
    pygame.draw.ellipse(screen, color, (x + width - diameter, y + height - diameter, diameter, diameter))

def drawOptions(index, color, border): # draw the box with its text in the middle
    name = food_list[index]
    box = get_place(index)      # find its proper place
    font1 = pygame.font.SysFont("Calibri",box.width//6)
    text = font1.render(name, True, BLACK, color)
    textbox = text.get_rect()
    textbox.center = (int(box[0] + box[2]//2), int(box[1] + box[3]//2))
    drawBoxOption(box, color, border)
    screen.blit(text, textbox)

def drawTextTopLeft(font, text, size, color, background, x_pos, y_pos):
    font1 = pygame.font.SysFont(font, size)
    text1 = font1.render(text, True, color, background)
    rect1 = text1.get_rect()
    rect1.topleft = (x_pos, y_pos)
    screen.blit(text1, (x_pos, y_pos))
    return rect1

def drawTextTopRight(font, text, size, color, background, border, x_pos, y_pos):
    font1 = pygame.font.SysFont(font, size)
    text1 = font1.render(text, True, color, background)
    rect1 = text1.get_rect()
    rect1.topright = (x_pos, y_pos)
    screen.blit(text1, rect1)
    pygame.draw.rect(screen, border, rect1, 2)
    return rect1

def backNext(stage, b, n, value):
    new_stage = stage
    next = drawTextTopRight("Arial", " NEXT ", 20, BLACK, L_GRAY, BLACK, width, 0)
    if next.collidepoint(mouse) and mouseClickedUp and value != "":
        new_stage = n
    back = drawTextTopRight("Arial", " BACK ", 20, BLACK, L_GRAY, BLACK, next.left, 0)
    if back.collidepoint(mouse) and mouseClickedUp:
        new_stage = b
    return new_stage

class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.text = " "
        self.font = pygame.font.SysFont("Calibri", 30)
        self.image = self.font.render("", True, [0, 0, 0])
        self.rect = self.image.get_rect()
        self.active = False
        self.locked = False
        self.color = BLUE1

    def add_chr(self, char):
        global shiftDown
        if self.active:
            if char in validChars and not shiftDown:
                self.text += char
            elif char in validChars and shiftDown:
                self.text += shiftChars[validChars.index(char)]
            elif char == " ":
                self.text += " "
        self.image = self.font.render(self.text, True, [0, 0, 0])

def drawRating(max_rating):
    minx = width//1.7
    margin = width//50
    star_size = width//20
    goldenstar = pygame.transform.scale(pygame.image.load("goldenstar.png"), (star_size, star_size))
    bluestar = pygame.transform.scale(pygame.image.load("bluestar.png"), (star_size, star_size))
    star = pygame.transform.scale(pygame.image.load("star.png"), (star_size, star_size))
    y_pos = height//1.5
    list_of_star = []
    for i in range(max_rating):
        x_pos = minx + i*(margin + star_size)
        screen.blit(star, (x_pos, y_pos))
        rect = pygame.Rect(x_pos, y_pos, star_size, star_size)
        list_of_star.append(rect)
    return list_of_star + [goldenstar, bluestar]

def drawTextCenter(font, text, color, background, size, x_center, y_center, bold1):
    font_text = pygame.font.SysFont(font, size, bold = bold1)
    textSrf = font_text.render(text, True, color, background)
    textbox = textSrf.get_rect()
    textbox.center = (x_center, y_center)
    screen.blit(textSrf, textbox)
    return textbox

def drawBorderCenter(rect_w, rect_h, x_center, y_center, color, border):
    rect = pygame.Rect(0, 0, rect_w, rect_h)
    rect.center = (x_center, y_center)
    pygame.draw.rect(screen, color, rect, border)
    return rect

def process_input(x):
    input1 = x
    if x == "" or x == " ":
        input1 = "Blank"
    return input1

def process_place(place):
    place1 = place.replace("(", "").replace(")", "").replace(",","")
    place2 = place1.split(" ")
    place3 = [float(a) for a in place2]
    return place3

def displayValidPrice(price_range):
    if price_range == [None, None]:
        return "No price range found"
    else:
        return "${} - ${}".format(price_range[0], price_range[1])

def validPrice(min1, max1):
    price_range = [0, 100]
    if (min1[1:].replace(".", "", 1).isdigit() or min1 == " ") and (max1[1:].replace(".", "", 1).isdigit() or max1 == " "):
        if min1 != " ": price_range[0] = float(min1[1:])
        if max1 != " ": price_range[1] = float(max1[1:])
        if price_range[0] <= price_range[1]: return price_range
    return [None, None]

def drawNotFound():
    not_found = pygame.image.load("notfound.png")
    not_found_box = not_found.get_rect()
    not_found_box.center = (width//2, height//1.8)
    screen.blit(not_found, not_found_box)

def drawCanteenBoxes(canteen_list, image_list, result, distance_active): # later will add distance
    result1 = result
    def drawCanteenBox(x_pos, y_pos, canteen_list, image_list, index, distance_active): # later will add distance
        box_width, box_height = width//6, height//3.2
        box = drawBorderCenter(box_width, box_height, x_pos, y_pos, BLACK, 2)
        # image part
        font1 = "Calibri"
        image = pygame.image.load(image_list[index])
        value = min(int(box_width//1.2), int(box_height//2)) - 8
        ratio = image.get_width() / image.get_height()
        image = pygame.transform.scale(image, (int(value*ratio), value))
        image_box = image.get_rect()
        image_box.center = (x_pos, y_pos - box_height//5)
        screen.blit(image, image_box)
        # text part
        def get_name(raw):
            name = raw
            if raw == "Northspine Foodcourt":
                name = "North spine"
            if raw == "Koufu @ Southspine":
                name =  "South spine"
            return name
        # if distance_active:
        #     pass

        drawTextCenter(font1, get_name(canteen_list[index]), (84, 100, 250), None, 25, x_pos, y_pos + box_height//5, True)
        if distance_active:
            distance1 = result1.at[canteen_list[index], "Distance"]
            distance3 = get_location(distance1)
            distance2 = str(round(distance3[0], 2)) + "km"
            drawTextCenter(font1, distance2, (250, 0, 50), None, 20, x_pos, y_pos + box_height//3, False)
        if box.collidepoint(mouse):
            pygame.draw.rect(screen, BLUE, box, 3)
        return box

    chosen_canteen1 = ""
    num_of_boxes = len(canteen_list)
    down, up, space = 0, num_of_boxes, width//5.8
    if num_of_boxes > 5:
        down = num_of_boxes//2
        up = num_of_boxes - down
    # draw top boxes
    up2, down2 = (up-1)/2, (down-1)/2
    uplist = downlist = []
    for i in range(up):
        x_pos = (i-up2)*space + width//2
        y_pos = height//2.2
        box1 = drawCanteenBox(x_pos, y_pos, canteen_list, image_list, i, distance_active)
        uplist.append(box1)
    for j in range(down):
        x_pos = (j-down2)*space + width//2
        y_pos = height//1.25
        box1 = drawCanteenBox(x_pos, y_pos, canteen_list, image_list, j+up, distance_active)
        downlist.append(box1)
    total_list = uplist + downlist
    for i in range(num_of_boxes):
        if total_list[i].collidepoint(mouse) and mouseClicked:
            chosen_canteen1 = canteen_list[i]
            break
    return chosen_canteen1

def get_active(box, active):
    new_active = active
    if mouseClicked:
        if box.collidepoint(mouse):
            new_active = not new_active
        else:
            new_active = False
    return new_active

def generateMap():
    hall1 = pygame.Rect(700, 391, 66, 52)
    hall2 = pygame.Rect(546, 291, 110, 54)
    hall3 = pygame.Rect(349, 192, 40, 20)
    hall4 = pygame.Rect(580, 444, 86, 34)
    hall5 = pygame.Rect(670, 440, 70, 30)
    hall6 = pygame.Rect(655, 291, 100, 62)
    hall7 = pygame.Rect(201, 572, 185, 45)
    hall8 = pygame.Rect(523, 161, 90, 70)
    hall9 = pygame.Rect(541, 101, 100, 50)
    hall10 = pygame.Rect(620, 44, 65, 35)
    hall11 = pygame.Rect(655, 20, 66, 25)
    hall12 = pygame.Rect(241, 180, 40, 25)
    hall13 = pygame.Rect(301, 148, 51, 27)
    hall14 = pygame.Rect(338, 109, 70, 41)
    hall15 = pygame.Rect(404, 71, 100, 45)
    hall16 = pygame.Rect(299, 225, 100, 20)
    tmrind = pygame.Rect(532, 29, 45, 30)
    pioneer = pygame.Rect(764, 369, 36, 27)
    cresent = pygame.Rect(800,368,55,25)
    grad1 = pygame.Rect(676, 11, 46, 31)
    grad2 = pygame.Rect(578,8, 68, 25)
    south = pygame.Rect(181, 452, 300, 102)
    north = pygame.Rect(139, 331, 180, 100)
    nie = pygame.Rect(47, 238, 238, 67)
    north_hill = pygame.Rect(245, 468, 74, 49)
    wave = pygame.Rect(807, 251, 71, 55)

    list_of_box = [hall1, hall2, hall3, hall4, hall5, hall6, hall7, hall8, hall9, hall10,
                    hall11, hall12, hall13, hall14, hall15, hall16, tmrind, cresent, pioneer,
                    grad1, grad2, south, north, nie, north_hill, wave]
    list_of_name = ["Hall 1", "Hall 2", "Hall 3", "Hall 4", "Hall 5", "Hall 6", "Hall 7", "Hall 8", "Hall 9",
                    "Hall 10", "Hall 11", "Hall 12", "Hall 13", "Hall 14", "Hall 15", "Hall 16", "Tamarind Hall",
                    "Pioneer Hall", "Cresent Hall", "Graduate 1", "Graduate 2", "South spine", "North spine", "NIE",
                    "North Hill", "The Wave"]
    return list_of_box, list_of_name

    list_of_box = [hall1, hall2, hall3, hall4, hall5, hall6, hall7, hall8, hall9, hall10,
                    hall11, hall12, hall13, hall14, hall15, hall16, std_hostel, cresent, pioneer,
                    grad1, grad2, south, north, nie, north_hill, wave]
    list_of_name = ["Hall 1", "Hall 2", "Hall 3", "Hall 4", "Hall 5", "Hall 6", "Hall 7", "Hall 8", "Hall 9",
                    "Hall 10", "Hall 11", "Hall 12", "Hall 13", "Hall 14", "Hall 15", "Hall 16", "Student hostel",
                    "Pioneer Hall", "Cresent Hall", "Graduate 1", "Graduate 2", "South spine", "North spine", "NIE",
                    "North Hill", "The Wave"]
    return list_of_box, list_of_name

def checkMap(list1, list2, name, processed_mouse):
    name1 = name
    for box in list1:
        if box.collidepoint(processed_mouse):
            name1 = list2[list1.index(box)]
            drawTextTopLeft("Palatino Linotype", name1, 30, BLACK, WHITE, 0, 0)
            break
    return name1

def processMouse(top_image, left_image, image_width, image_height, mouse):
    x1 = round((mouse[0] - left_image)*900/image_width, 0)
    y1 = round((mouse[1] - top_image)*636/image_height, 0)
    return x1, y1

def display_image(image, top_image, left_image, width, height):
    screen_ratio = width/height
    true_width = image.get_width()
    true_height = image.get_height()
    image_ratio = true_width/true_height
    x_pos, y_pos = 0, 0
    image_width, image_height = width, height
    if width >= true_width or height >= true_height:
        if screen_ratio >= image_ratio:
            image_width = int(image_height * image_ratio)
            image1 = pygame.transform.scale(image, (image_width, image_height))
            x_pos = (width - height*image_ratio)//2
            screen.blit(image1, (x_pos, y_pos))
        else:
            image_height = int(image_width / image_ratio)
            image1 = pygame.transform.scale(image, (image_width, image_height))
            y_pos = (height - width/image_ratio)//2
            screen.blit(image1, (x_pos, y_pos))
    else:
        screen.blit(image, (left_image, top_image))
        image_width = true_width
        image_height = true_height
        x_pos = left_image
        y_pos = top_image

    return x_pos, y_pos, image_width, image_height

def zoom(zoom_num, top_image, left_image, image_width, image_height):
    x_center = width//2 - left_image
    y_center = height//2 - top_image
    ratio = ratio_scale if zoom_num == 1 else 1/ratio_scale
    new_x_center = x_center * ratio
    new_y_center = y_center * ratio
    image_width *= ratio
    image_height *= ratio
    new_left_image = width//2 - new_x_center
    new_top_image = height//2 - new_y_center
    return new_left_image, new_top_image, image_width, image_height

def zoomButton(x_center, y_center, bool):
    zoombox = pygame.Rect(0, 0, height//15, height//15)
    zoombox.center = (x_center, y_center)
    color = (130, 170, 250)
    if zoombox.collidepoint(mouse): color = (255, 220, 105)
    pygame.draw.ellipse(screen, color, zoombox)
    pygame.draw.line(screen, BLACK, (x_center - height//40, y_center), (x_center + height//40, y_center), 2)
    if bool:
        pygame.draw.line(screen, BLACK, (x_center, y_center - height//40), (x_center, y_center + height//40), 2)
    return zoombox.collidepoint(mouse) and mouseClicked

def moveButtons():
    color = (100, 240, 150)
    x_cen, y_cen, size = width//1.065, height//1.12, height//15
    dif1, dif2 = size, height//60
    # up
    up = pygame.Rect(0,0, size, size)
    up.center = (x_cen, y_cen - dif1)
    pygame.draw.ellipse(screen, color, up)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif2, y_cen - dif1), (x_cen, y_cen - dif1 - dif2), (x_cen + dif2, y_cen - dif1)), 4)
    pygame.draw.line(screen, BLACK, (x_cen, y_cen - dif1 - dif2), (x_cen, y_cen - dif1 + dif2), 3)
    # down
    down = pygame.Rect(0,0, size, size)
    down.center = (x_cen, y_cen + dif1)
    if down.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), down)
    pygame.draw.ellipse(screen, color, down)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif2, y_cen + dif1), (x_cen, y_cen + dif1 + dif2), (x_cen + dif2, y_cen + dif1)), 4)
    pygame.draw.line(screen, BLACK, (x_cen, y_cen + dif1 - dif2), (x_cen, y_cen + dif1 + dif2), 3)
    # left
    left = pygame.Rect(0,0, size, size)
    left.center = (x_cen - dif1, y_cen)
    if left.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), left)
    pygame.draw.ellipse(screen, color, left)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif1, y_cen - dif2), (x_cen - dif1 - dif2, y_cen), (x_cen - dif1, y_cen + dif2)), 4)
    pygame.draw.line(screen, BLACK, (x_cen - dif1 - dif2, y_cen), (x_cen - dif1 + dif2, y_cen), 3)
    # right
    right = pygame.Rect(0,0, size, size)
    right.center = (x_cen + dif1, y_cen)
    if right.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), right)
    pygame.draw.ellipse(screen, color, right)
    pygame.draw.lines(screen, BLACK, False, ((x_cen + dif1, y_cen - dif2), (x_cen + dif1 + dif2,y_cen), (x_cen + dif1, y_cen + dif2)), 4)
    pygame.draw.line(screen, BLACK, (x_cen + dif1 - dif2, y_cen), (x_cen + dif1 + dif2, y_cen), 3)
    return up, down, left, right

def drawStallBoxes(list_of_stalls):
    left_pos = width//(4/1.2) - width//70
    right_pos = width//(4/2.8) + width//70
    box_width = width//2.5
    num_of_stalls = len(list_of_stalls)
    gap_between_center = min(height//10, height//num_of_stalls)
    list_of_boxes = []
    chosen_stall = ""
    def drawStallBox(stall, x_pos, y_pos):
        stall_box = pygame.Rect(0,0, box_width, 35)
        stall_box.center = (x_pos, y_pos)
        if stall_box.collidepoint(mouse):
            pygame.draw.rect(screen, ORANGE, stall_box)
        text_box = drawTextCenter("Calibri", stall, BLACK, None, 25, x_pos, y_pos, False)
        pygame.draw.rect(screen, BLACK, stall_box, 1)
        return stall_box

    right = num_of_stalls//2
    left = num_of_stalls - right
    right_list = left_list = []
    for i in range(left):
        y_pos = height//3 + (2*i+1)*height//30
        box = drawStallBox(list_of_stalls[i], left_pos, y_pos)
        left_list.append(box)
    for j in range(right):
        y_pos = height//3 + (2*j+1)*height//30
        box = drawStallBox(list_of_stalls[j + left], right_pos, y_pos)
        right_list.append(box)
    list_of_boxes = left_list + right_list

    for i in range(num_of_stalls):
        if list_of_boxes[i].collidepoint(mouse) and mouseClicked:
            chosen_stall = list_of_stalls[i]
            break
    return chosen_stall

def drawDishBoxes(list_of_dishes, list_of_prices, count):
    box_width = width//1.25
    price_width = width//20
    dish_width = box_width - price_width
    x_dish = width//2 - price_width//2
    x_price = x_dish + box_width//2
    y_pos = 11*width//30
    pass

def drawDishBox(dish, price, x_dish, x_price, dish_width, price_width, box_height, y_pos, background, bold1):
    new_price = new_dish = ""
    menu_box = pygame.Rect(0,0, dish_width, box_height)
    menu_box.center = (x_dish, y_pos)
    price_box = pygame.Rect(0,0, price_width, box_height)
    price_box.center = (x_price, y_pos)
    pygame.draw.rect(screen, background, menu_box)
    pygame.draw.rect(screen, background, price_box)
    if (menu_box.collidepoint(mouse) or price_box.collidepoint(mouse)) and dish != "Menu Item" and price != "Price ($)":
        pygame.draw.rect(screen, (255, 255, 200), menu_box)
        pygame.draw.rect(screen, (255, 255, 200), price_box)
        if mouseClickedUp:
            new_dish = dish
            new_price = price
    pygame.draw.rect(screen, BLACK, menu_box,1)
    pygame.draw.rect(screen, BLACK, price_box,1)
    drawTextCenter("Calibri", dish, BLACK, None, 25, x_dish, y_pos, bold1)
    drawTextCenter("Calibri", price, BLACK, None, 25, x_price, y_pos, bold1)
    return [menu_box, price_box, new_dish, new_price]

def switchPage(page):
    new_page = page
    size = width//30
    space = width//20
    dif = size//3
    y_pos = 29*(height//30)
    # box back
    color_b = BLUE1
    box_b = pygame.Rect(0,0,size, size)
    box_b.center = (width//2 - space, y_pos)
    if box_b.collidepoint(mouse):
        color_b = ORANGE
        if mouseClickedUp: new_page -= 1
    pygame.draw.rect(screen, color_b, box_b)
    pygame.draw.rect(screen, BLACK, box_b, 2)
    pygame.draw.lines(screen, BLACK, True, ((width//2 - space + dif, y_pos - dif), (width//2 - space - dif, y_pos), (width//2 - space + dif, y_pos + dif)), 2)
    # box_next
    color_n = BLUE1
    box_n = pygame.Rect(0, 0, size, size)
    box_n.center = (width//2 + space, y_pos)
    if box_n.collidepoint(mouse):
        color_n = ORANGE
        if mouseClickedUp: new_page += 1
    pygame.draw.rect(screen, color_n, box_n)
    pygame.draw.rect(screen, BLACK, box_n, 2)
    pygame.draw.lines(screen, BLACK, True, ((width//2 + space - dif, y_pos - dif), (width//2 + space + dif, y_pos), (width//2 + space - dif, y_pos + dif)), 2)
    return new_page

def check_account(username, password, usernames, passwords):
    try:
        return usernames.index(username) == passwords.index(password)
    except ValueError:
        return False
    return False

def backUpdate(stage):
    new_stage = stage
    back = pygame.Rect(width - 100, 0, 100, 40)
    pygame.draw.rect(screen, (180, 180, 180), back)
    if back.collidepoint(mouse):
        pygame.draw.rect(screen, L_GRAY, back)
        if mouseClickedUp:
            new_stage = 10
    pygame.draw.rect(screen, BLACK, back, 1)
    drawTextCenter("Calibri", "BACK", BLACK, None, 25, width - 50, 20, True)
    return new_stage

def checkTime(current_time, chosen_canteen):
    open = int(infocan.loc[chosen_canteen, "Open"])
    closed = int(infocan.loc[chosen_canteen, "Closed"])
    hour = current_time.hour
    minute = current_time.minute
    time = hour * 60 + minute
    top = 21*(height//30)
    left = width//8
    if time >= closed * 60:
        drawTextTopLeft("Calibri", "You should come back tommorow. It's already {}:{}".format(hour, minute), 25, BLUE, None, left, top)
    elif time >= (closed - 1) * 60:
        drawTextTopLeft("Calibri", "You still have {} minute(s) left to get some food.".format(60 - minute), 25, BLUE, None, left, top)
    elif 13*60 + 30 >= time > 12*60:
        drawTextTopLeft("Calibri", "Be quick! There will be many people in the queue.", 25, BLUE, None, left, top)
    elif open * 60 > time:
        drawTextTopLeft("Calibri", "Wow! You woke up so early! Have some exercises first.", 25, BLUE, None, left, top)
    else:
        drawTextTopLeft("Calibri", "Let's go!!! It's just {}:{:02d}.".format(hour, minute), 25, BLUE, None, left, top)

def lineDown(left, right, text, font1, size):
    def getWidth(text1):
        font2 = pygame.font.SysFont(font1, size)
        text2 = font2.render(text1, True, BLACK)
        rect2 = text2.get_rect()
        return rect2.width

    range = right - left
    char_width = getWidth("m")
    limit1 = range//char_width
    limit = limit1
    new_text = text
    result = []
    if getWidth(new_text) > range:
        while getWidth(new_text) > range:
            cut_text = new_text[:limit1]
            new_text = new_text[limit1:]
            while getWidth(cut_text) < range and limit < len(text):
                cut_text += new_text[0]
                new_text = new_text[1:]
            result.append(cut_text)
        result += [new_text]
        return result
    else: return [text]

def directionList(steps, left, right):
    list1 = []
    for step in steps:
        direction_list = lineDown(left, right, step["direction"], "Calibri", 25)
        list1 += direction_list + [step["distance"]] + [""]
    return list1




if __name__ == '__main__':
    main()
