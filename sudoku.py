import pygame 
import os
import copy
import time
import sys
from sudoku_solve import Sudoku

#create game
pygame.init()
win = pygame.display.set_mode((440, 550))
icon = pygame.image.load("Asserts\InGame\icon.png")
pygame.display.set_caption("Sudoku")
pygame.display.set_icon(icon)
myfont = pygame.font.SysFont('Century Gothic', 25)
myfont2 = pygame.font.SysFont('Century Gothic', 15)
myfont3 = pygame.font.SysFont('Bahnschrift', 20)

#add background music 
pygame.mixer.init()
pygame.mixer.music.load("Asserts\InGame\music.mp3")
pygame.mixer.music.play()

#SIZE
SOLVE_INDEX = (150, 480)
SOLVE_ICON_INDEX = (150, 442)
HOME_INDEX = (68, 480)
HOME_ICON_INDEX = (70, 440)

FPS = 60
MISTAKE = 0

#COLORS
WHITE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (240, 255, 255)
NEWNUMBER_COLOR = (80, 110, 140)
BLUR_COLOR = (209, 209, 209)
FUNCTION_TABLE_COLOR = (232, 232, 232)


Board = Sudoku("Beginner")
grid = Board.board
grid2 = Board.board2
solved_grid = Board.solved_board

#icon in home
SUDOKU_CHAR = pygame.transform.smoothscale(pygame.image.load('Asserts\Home\sudoku.png'), (165,48))
SHAPE = pygame.Rect(100, 160, 240, 40)
SHAPE1 = pygame.Rect(100, 220, 240, 40)
SHAPE2 = pygame.Rect(100, 280, 240, 40)
BEGINNER_CHAR = myfont3.render("Beginner", True, 'Black')
MEDIUM_CHAR = myfont3.render("Medium", True, 'Black')
HARD_CHAR = myfont3.render("Hard", True, 'Black')

#icon in game
VALUE = myfont2.render(str("solve"), True, 'Black')
HOME = myfont2.render("home", True, 'Black')
SOLVE_ICON = pygame.transform.smoothscale(pygame.image.load('Asserts\InGame\solve_icon.png'), (38,38))
SOLVE_ICON_RECT = SOLVE_ICON.get_rect(topleft=SOLVE_ICON_INDEX)
HOME_ICON = pygame.transform.smoothscale(pygame.image.load('Asserts\InGame\Home.png'), (40,40))
HOME_ICON_RECT = HOME_ICON.get_rect(topleft=HOME_ICON_INDEX)

#Home
def draw_home(win):
    pygame.draw.rect(win, 'Grey', SHAPE, border_radius=20)
    pygame.draw.rect(win, 'Grey', SHAPE1, border_radius=20)
    pygame.draw.rect(win, 'Grey', SHAPE2, border_radius=20)
    win.blit(SUDOKU_CHAR, (137, 100))
    win.blit(BEGINNER_CHAR, (185,170))
    win.blit(MEDIUM_CHAR, (185, 230))
    win.blit(HARD_CHAR, (195, 290))
    
#InGame here
#Add new number and check valid
def insert(win, position):
    global MISTAKE
    i,j = position[1] // 40, position[0] // 40
    x_index, y_index= j * 40 + 2, i * 40 + 2
    if position[0] >= 40 and position[0] < 400 and position[1] >= 40 and position[1] < 400:
        if grid[i - 1][j - 1] == 0 and grid2[i - 1][j - 1] == 0:
            pygame.draw.rect(win, BLUR_COLOR, (x_index, y_index, 38, 38))
            pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid[i - 1][j - 1] != 0):
                    pygame.draw.rect(win, WHITE_COLOR, (x_index, y_index, 38, 38))
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    pygame.draw.rect(win, WHITE_COLOR, (x_index, y_index, 38, 38))
                    if Board.is_legal_move(i - 1, j - 1, event.key - 48):
                        grid2[i - 1][j - 1] = event.key - 48
                        value = myfont.render(str(event.key-48), True, NEWNUMBER_COLOR)
                        win.blit(value, (j * 40 + 14, i * 40 + 4))
                    else:
                        MISTAKE += 1
                        pygame.display.update()
                        return 
                return 
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.draw.rect(win, WHITE_COLOR, (x_index, y_index, 38, 38))
                return

#Create a Sudoku pluzze with unique solution
def draw_sudoku(win, level_char):
    global MISTAKE
    pygame.draw.rect(win, (255, 255, 255), (40, 40, 360, 360))
    pygame.draw.rect(win, 'Black', (40, 40, 362, 362), 2, 5)   
    for i in range(1, 9):
        k = 1
        if i % 3 == 0:
            k = 2
        pygame.draw.line(win, 'Black', (40 + 40 * i, 40), (40 + 40 * i, 400), k)
        pygame.draw.line(win, 'Black', (40, 40 * i + 40), (400, 40 * i + 40), k)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                value = myfont.render(str(grid[i][j]), True, 'Black')
                win.blit(value, ((j + 1) * 40 + 14, (i + 1) * 40 + 4))
            elif grid2[i][j] != 0:
                value = myfont.render(str(grid2[i][j]), True, NEWNUMBER_COLOR)
                win.blit(value, ((j + 1) * 40 + 14, (i + 1) * 40 + 4))
    #myfont2 = pygame.font.SysFont('Century Gothic', 15)
    level = myfont2.render(level_char, True, 'Black' )
    MISTAKE_CHAR = myfont2.render(f"mistake: {MISTAKE}/3", True, 'Black')
    win.blit(level, (40, 20))
    win.blit(MISTAKE_CHAR, (310, 20))

#Create function table 
def draw_table(win):
    pygame.draw.rect(win, WHITE_COLOR, (40, 420, 180, 100),border_radius=10)
    #myfont = pygame.font.SysFont('Century Gothic', 15) 
    win.blit(VALUE, SOLVE_INDEX)
    win.blit(HOME, HOME_INDEX)
    win.blit(SOLVE_ICON, SOLVE_ICON_RECT)
    win.blit(HOME_ICON, HOME_ICON_RECT)

#Function button
def function(win, pos): 
    for i in range(9):
        for j in range(9):
            if grid[i][j] != solved_grid[i][j]:
                time.sleep(0.05)
                value = myfont.render(str(solved_grid[i][j]), True, NEWNUMBER_COLOR)
                win.blit(value, ((j + 1) * 40 + 14, (i + 1) * 40 + 4))
                if  grid2[i][j] != solved_grid[i][j]:
                    grid2[i][j] = solved_grid[i][j]
                pygame.display.update()

def renew_table(level_char):
    global MISTAKE,Board, grid, grid2, solved_grid
    Board = Sudoku(level_char)
    grid = Board.board
    grid2 = Board.board2
    solved_grid = Board.solved_board
    MISTAKE = 0

def main():
    global MISTAKE
    clock = pygame.time.Clock()
    running = True
    running2 = False
    level_char = "Beginner"
    while running:
        clock.tick(FPS)
        win.fill(WHITE_COLOR)
        draw_home(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pos_rect = pygame.Rect(pos[0], pos[1], 1, 1)
                    if pos_rect.colliderect(SHAPE):
                        level_char = "Beginner"
                        running2 = True
                        renew_table(level_char)
                        break
                    elif pos_rect.colliderect(SHAPE1):
                        level_char = "Medium"
                        running2 = True
                        renew_table(level_char)
                        break
                    elif pos_rect.colliderect(SHAPE2):
                        level_char = "Hard"
                        running2 = True
                        renew_table(level_char)
                        break                    
            pygame.display.update()
        while running2: 
            # The fresh rate is 60hz
            clock.tick(FPS)

            #DRAW GAME
            win.fill(BACKGROUND_COLOR)
            draw_sudoku(win, level_char)
            draw_table(win)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if pos[1] <= 400:
                            insert(win, pos)
                            if MISTAKE > 3:
                                running2 = False
                        pos_rect = pygame.Rect(pos[0], pos[1], 1, 1)
                        if pos_rect.colliderect(SOLVE_ICON_RECT):
                            function(win, pos)
                        if pos_rect.colliderect(HOME_ICON_RECT):
                            running2 = False
                    #insert(win, pos)
            pygame.display.update()
    #Home    
    pygame.quit()

if __name__ == "__main__":
    main()         
            



