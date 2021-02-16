import pygame
import sys
import random

class InMem():
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.num_flags = 0
        self.tiles = [[0 for x in range(cols)] for y in range(rows)]
        self.AItiles = [["NV" for x in range(cols)]  for y in range(rows)]
        self.mines = []
        self.screen_width = 20*self.cols + self.cols + 1
        self.screen_height = 20*self.rows + self.rows + 41
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))   
        self.caption = pygame.display.set_caption("Minesweeper") 
        self.logo = pygame.image.load("logo.png")
        self.running = True
        self.win = False
        self.lose = False

    def set_mines(self):       
        """sets mines on random positions"""
        self.mines = []
        i = 0
        while i < self.num_mines:
            x = random.randint(0,self.cols-1)
            y = random.randint(0,self.rows-1)
            if (y,x) not in self.mines:
                self.mines.append((y,x))
                i += 1
        for i in range(len(self.mines)):
            self.tiles[self.mines[i][0]][self.mines[i][1]] = "M"
    
    def ingrid(self,i,j):
        """checks whether given possition is in grid(exists)"""
        if i<0 or j<0 or j>=self.cols or i>=self.rows:
            return False
        return True

    def get_around(self,i,j):
        """returns number of mines surrounding given position"""
        around = 0
        for (a,b) in [(0,1), (0,-1), (1,-1), (1,0), (1,1), (-1,1), (-1,0), (-1,-1)]:
            if self.ingrid(a+i, b+j):
                if self.tiles[a+i][b+j] == "M":
                    around+=1
        return around

    def get_surrounding_mines(self):
        """counts surrounding miles for each tile"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.tiles[i][j] != "M":
                    self.tiles[i][j] = self.get_around(i,j)
        # for row in self.tiles:
            # print(row)

    def draw_colored_tile (self, x, y, color):
        """draws tile of given color on given position"""
        tile = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(self.screen, color, tile)

    def draw_flag(self,x,y):
        """draws tile with flag on given position"""
        self.draw_colored_tile(x,y,(0,0,0))
        pygame.draw.line(self.screen, (205,0,0), (x+5,y+2), (x+5,y+17), 2)
        pygame.draw.polygon(self.screen, (255,255,0), ((x+6,y+2), (x+6, y+12), (x+12,y+7)),1)
        pygame.display.update()
        
    def draw_mine(self,x,y):
        """draws tile with mine on given position"""
        tile = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(self.screen, (250,0,0), tile)
        pygame.draw.circle(self.screen, (0,0,0), (x+10,y+10), 5)
    
    def draw_tile_withnum(self,x,y,num):
        """draws tile with given number and corresponding color"""
        self.draw_colored_tile(x,y,(0,0,0))
        font = pygame.font.SysFont("ebrim.ttf",26)
        if num == 1: clr = (0, 255, 255)        # light-blue
        elif num == 2: clr = (51,255,51)        # light-green
        elif num == 3: clr = (255,51,153)       # pink
        elif num == 4: clr = (153,51,255)       # purple
        elif num == 5: clr = (255,255,0)        # yellow
        elif num == 6: clr = (255,153,0)        # orange
        elif num == 7: clr = (0,153,0)          # dark-green
        else: clr = (255,255,255)               # white
        nmbr = font.render(str(num), True, clr)
        self.screen.blit(nmbr, (x+5,y+2))            
    
    def draw_firstline(self): # počet mín a vlajočiek(označených pozícií)
        """draws bar with number of mines, number of flags and hint tile"""
        first_line = "MINES: " + str(self.num_mines) + "    FLAGS: " + str(self.num_flags) + "   "
        font = pygame.font.SysFont("ebrima.ttf", 16)
        line = font.render(first_line, True, (0,0,0), (255,255,255))
        self.screen.blit(line, (5,18))                                          # vypíše počet mín a aktuálne vyznačených vlajočiek
        give = font.render("GIVE", True, (0,0,0), (255,235,0))
        hint = font.render("HINT", True, (0,0,0), (255,235,0))
        self.screen.blit(give, (self.screen_width-35, 10))
        self.screen.blit(hint, (self.screen_width-35, 21))                      # vypíšet "tlačítko" GIVE HINT
        pygame.display.update()
   
    def initialize(self):
        """shows start screen of game"""
        self.running = True
        self.lose = False
        self.win = False
        self.num_flags = 0
        self.tiles = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.AItiles = [["NV" for x in range(self.cols)] for y in range(self.rows)]
        self.set_mines()
        x = 1
        y = 41
        self.screen.fill(pygame.Color(255,255,255))
        for i in range(self.rows):
            for j in range(self.cols):
                self.draw_colored_tile(x,y,(0,0,0))
                x+=21
            y+=21
            x=1
        self.get_surrounding_mines()
        self.draw_firstline()
        
    def chceck_win(self):
        """checks if the situation is winning"""
        correct_flags = 0
        for (a,b) in self.mines:
            if self.tiles[a][b] == "F":
                correct_flags += 1
        if correct_flags == self.num_mines and correct_flags == self.num_flags:
            self.win = True
            self.running = False

    def search(self,i,j):
        """action on leftclick on a tile"""
        x = j*21 +1
        y = i*21 +41
        if not self.ingrid(i,j):                                #if the tile is outside of the grid, returns
            return
        if self.tiles[i][j] == "V":                             #if the tile is already vivsible, returns
            return
        if self.tiles[i][j] == "M":                             #if the clicked tile is a mine, shows all mines and goes into a lose state       
            self.draw_mine(x,y)
            for i in range(self.rows):
                for j in range(self.cols):
                    if (i,j) in self.mines:
                        self.draw_mine(j*21 +1, i*21 +41)
            self.lose = True
            self.running = False
            return
        if self.tiles[i][j] == 0:                                                               #if the tile is a zero, draws grey tile,
            self.draw_colored_tile(x,y,(96,96,96))                                              #sets the tile to visible, recursively calls the search function
            self.AItiles[i][j] = self.tiles[i][j]                                               #on all of its neighbours
            self.tiles[i][j] = "V"                                                              #and passes on the information aboout the tile to AI
            for (a,b) in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
                self.search(a+i, b+j)
        if type(self.tiles[i][j]) == int and self.tiles[i][j] > 0 and self.tiles[i][j] < 9:     #if the tile is a number between 0 and 9,
            self.draw_tile_withnum(x,y,self.tiles[i][j])                                        #draws a numberd tile with a corresponding number
            self.AItiles[i][j] = self.tiles[i][j]                                               #and sets the tie to visible
            self.tiles[i][j] = "V"                                                              #and passes on the information aboout the tile to AI
            return
    
    def right_button(self,i,j):
        """action on rightclick on a tile"""
        x = j*21 +1
        y = i*21 +41
        if self.tiles[i][j] == "F":                              #unflag
            self.draw_colored_tile(x,y,(0,0,0))       
            self.AItiles[i][j] = "NV"
            self.num_flags -= 1
            if (i,j) in self.mines:
                self.tiles[i][j] = "M"          
            else:                                              
                self.tiles[i][j] = self.get_around(i,j)
            self.draw_firstline()
        else:                                   #place flag
            if self.AItiles[i][j] != "NV":            #can't place flag on a visible tile
                pass
            else:
                self.draw_flag(x,y)               
                self.tiles[i][j] = "F"
                self.AItiles[i][j] = "F"
                self.num_flags += 1
                self.draw_firstline()

    def is_safe_to_click(self,i,j):
        """chcecks whether a tile is safe to click on""" 
        safety = False
        for (a,b) in [(0,1), (0,-1), (1,-1), (1,0), (1,1), (-1,1), (-1,0), (-1,-1)]:
            if self.ingrid(i+a,j+b):
                if self.AItiles[i+a][j+b] != "NV":
                    flags = 0
                    for (aa,bb) in [(0,1), (0,-1), (1,-1), (1,0), (1,1), (-1,1), (-1,0), (-1,-1)]:
                        if self.ingrid(i+a+aa, j+b+bb):
                            if self.AItiles[i+a+aa][j+b+bb] ==  "F":
                                flags += 1
                    if self.AItiles[i+a][j+b] == flags:
                        safety = True
        return safety

    def give_hint(self):
        """returns list of possible safe clicks"""
        out = []
        i=0
        while i < self.rows:
            j=0
            while j < self.cols:
                if self.AItiles[i][j] == "NV":
                    if self.is_safe_to_click(i,j):
                        out.append((i,j))
                j+=1
            i+=1
        return out

    def write_hint(self):
        """writes no hint on bar"""
        font = pygame.font.SysFont("ebrima.ttf", 16)
        line = font.render("No hints", True, (0,0,0), (255,255,255))
        self.screen.blit(line, (self.screen_width-45, 30))
    
    def delete_hint(self):
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(self.screen_width-45, 30, 45, 11))

    def mousePress(self,event):
        """actions when a button on mouse is pressed"""
        (a,b) = pygame.mouse.get_pos()
        if a < 0 or a >self.screen_width or b < 41 or b > self.screen_height:
            # clicking on the hint button (with right or left button)
            if a > self.screen_width-35 and a < self.screen_width-10 and b > 10 and b < 32:
                tip = self.give_hint()
                if len(tip)==0:
                    self.write_hint()
                else:
                    self.draw_colored_tile(tip[0][1]*21 +1, tip[0][0]*21+41, (255,235,0))            
        else:
            i = (b -41)//21
            j = a //21
            # RMB
            if event.button == 3:
                self.right_button(i,j)
            # LMB
            elif event.button == 1:
                self.search(i,j)
        pygame.display.update()
        # print("----------")
        # for row in self.tiles:
        #     print(row) 
    
    def lost(self):
        "draws game over on bar"
        font = pygame.font.SysFont("ebrima.ttf", 44)
        game_over = font.render("GAME OVER   ", True, (200,0,0), (255,255,255))
        self.screen.blit(game_over, (5,5))
        pygame.display.update() 
    
    def won(self):
        """draws you won on bar"""
        font = pygame.font.SysFont("ebrima.ttf", 44)
        youwon = font.render("YOU WON   ", True, (0,200,0), (255,255,255))
        self.screen.blit(youwon, (5,5))
        pygame.display.update() 
    
    def set_level(self,r,c,m):
        """sets level parameters and initializes"""
        self.rows = r
        self.cols = c
        self.num_mines = m
        self.screen_width = 20*self.cols + self.cols + 1
        self.screen_height = 20*self.rows + self.rows + 41
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.initialize()
        
    def run_game(self):
        """game loop"""
        pygame.init()
        pygame.display.set_icon(self.logo)
        self.initialize()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                if event.type == pygame.MOUSEBUTTONDOWN and self.running:
                    self.mousePress(event)
                    self.chceck_win()
                self.delete_hint()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.lose = False
                        self.initialize()
                    if event.key == pygame.key.key_code("e") and not self.running:
                        self.set_level(8,10,10)
                    if event.key == pygame.key.key_code("m") and not self.running:
                        self.set_level(14,18,40)
                    if event.key == pygame.key.key_code("h") and not self.running:
                        self.set_level(20,24,99)
            if self.win: self.won()
            if self.lose: self.lost()
            
        pygame.quit()
