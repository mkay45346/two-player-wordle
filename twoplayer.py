import pygame, sys
from pygame import Vector2
from wordfreq import top_n_list
all_words=top_n_list('en', 40000)
import random
import json

five_letter_words=[w for w in all_words if len(w)==5 and w.isalpha()]
wordset=set(five_letter_words)
pygame.init()
cell_number_h = 5
cell_number_v = 2
cell_size = 250
screen_width = cell_number_h * cell_size
screen_height = cell_number_v * cell_size+250
screen = pygame.display.set_mode((cell_number_h * cell_size, cell_number_v * cell_size+250))
pygame.display.set_caption("two player") 
typing_sound=pygame.mixer.Sound("C:\\Users\\manjeet\\Desktop\\coding\\wordle\\dilligafanditmeans-kick-drum-263837.mp3")
font_popup = pygame.font.Font(None, 60)
clock = pygame.time.Clock()
dark_gray="#212120"
fps = 60
state="main_menu"
word_player1 = []
word_player2 = []
player_names=[]
result1 = [0] * 5
used1 = [False] * 5
result2 = [0] * 5
used2 = [False] * 5
target_word=random.choice(five_letter_words)
target=list(target_word)
guess=1
reset=False
evaluated1=False
evaluated2=False
won=False
game_reset=False
count=0
shift_allow=False

target_letters=[]
tell_player=["PLAYER ONE","PLAYER TWO"]
winning_player=["Player 1 wins!","Player 2 wins!"]
losing_player=["Player 1 loses.","Player 2 loses."]
popups=["get the show on the road","strong start, good stuff", "i believe in you.", "you can do this.", "...you sure? all right.""that guess seems... interesting.","so close but so far.", "i wouldnt have done that if i were you.","you can do better than that.","jesus christ bruh guess the word.","are you even trying.","i aint even got a reaction for this bruh what the hell.","you all suck", "this is difficult to watch.","i doubted anyone would ever come this far.","you like jazz?","give a monkey a typewriter and infinite time.","skibidi",f"the answer is {target}"]
font = pygame.font.SysFont(None, 100)
class Letter:
    def __init__(self):
        pass
    def draw(self):
        for i in range(5):
            for j in range(2):
                letter_rect = pygame.Rect(i * cell_size + 5,(j) * cell_size + 255,cell_size - 10,cell_size - 10) 
                pygame.draw.rect(screen, 'gray', letter_rect, 3)
        if evaluated1:
            for col,res in enumerate(result1):
                if res == 0:
                    color=dark_gray
                elif res == 1:
                    color='green'
                else:
                    color='yellow'
                letter_rect = pygame.Rect(col * cell_size + 5,(cell_number_v-1) * cell_size + 5,cell_size - 10,cell_size - 10)
                pygame.draw.rect(screen,color, letter_rect)
        if evaluated2:
            for col,res in enumerate(result2):
                if res == 0:
                    color=dark_gray
                elif res == 1:
                    color='green'
                else:
                    color='yellow'
                letter_rect = pygame.Rect(col * cell_size + 5,(cell_number_v) * cell_size + 5,cell_size - 10,cell_size - 10)
                pygame.draw.rect(screen,color, letter_rect)
        for col, ch in enumerate(word_player1):
            rect = pygame.Rect(col * cell_size + 5,(cell_number_v-1) * cell_size + 5,cell_size - 10,cell_size - 10)
            text_surface = font.render(ch.upper(), True, "white")
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        for col, ch in enumerate(word_player2):
            rect = pygame.Rect(col * cell_size + 5,(cell_number_v) * cell_size + 5,cell_size - 10,cell_size - 10)
            text_surface = font.render(ch.upper(), True, "white")
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        
    def answer(self):
        if guess%2!=0:
            for i, l in enumerate(word_player1):
                if l == target[i]:
                    result1[i] = 1
                    
                    used1[i] = True
            for i, l in enumerate(word_player1):
                if result1[i] == 0:
                    for j, t in enumerate(target):
                        if not used1[j] and l == t:
                            result1[i] = 2
                            if result1[i] not in target_letters:
                                target_letters.append(l)
                            used1[j] = True
                            break
        else:
            for i, l in enumerate(word_player2):
                if l == target[i]:
                    result2[i] = 1
                    used2[i] = True
            for i, l in enumerate(word_player2):
                if result2[i] == 0:
                    for j, t in enumerate(target):
                        if not used2[j] and l == t:
                            result2[i] = 2
                            used2[j] = True
                            break

menu_image=pygame.transform.scale(pygame.image.load("C:\\Users\\manjeet\\Desktop\\coding\\paint\\drawing_1772023191.png"), (cell_number_h * cell_size, cell_number_v * cell_size+250))
play_button_rect = pygame.Rect(cell_number_h * cell_size//2-100, (cell_number_v * cell_size+250)//2-40, 200, 80)
win_image=pygame.transform.scale(pygame.image.load("C:\\Users\\manjeet\\Desktop\\coding\\wordle\\twoothplace.jpeg"), (cell_number_h * cell_size//2, (cell_number_v * cell_size+250)//2))
lose_image=pygame.transform.scale(pygame.image.load("C:\\Users\\manjeet\\Desktop\\coding\\wordle\\hq720.jpg"), (cell_number_h * cell_size, cell_number_v * cell_size+250))

letter=Letter()
run = True
while run:
    screen.fill("black") 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if state=="game":
            if event.type==pygame.KEYDOWN:
                if event.unicode.isalpha() and not won:
                    typing_sound.play()
                    if guess%2!=0:
                        if len(word_player1)<5:
                            word_player1+=event.unicode
                    else:
                        if len(word_player2)<5:
                            word_player2+=event.unicode
                if event.key==pygame.K_BACKSPACE:
                    if guess%2!=0:
                        word_player1=word_player1[:-1] 
                    else: 
                        word_player2=word_player2[:-1] 
                if event.key==pygame.K_RETURN:
                    if not shift_allow:
                        if len(word_player1)==5 and guess%2!=0:
                            guess_word1="".join(word_player1)
                            if guess_word1 in wordset:
                                evaluated1=True
                                letter.answer()
                                if guess_word1==target_word:

                                    state="win_screen"
                                guess+=1
                            else:
                                count+=1
                                if count==4:
                                    state="lose_screen"
                                
                        elif len(word_player2)==5 and guess%2==0: 
                            guess_word2="".join(word_player2)
                            if guess_word2 in wordset:
                                letter.answer()
                                evaluated2=True
                                count=0
                                if guess_word2==target_word:
                                    state="win_screen"
                                guess+=1
                                shift_allow=True
                            else:
                                count+=1
                                if count==4:
                                    state="lose_screen"
                    
                if event.key==pygame.K_RSHIFT:
                    if guess%2!=0 and len(word_player2)==5:
                        reset=True
                        shift_allow=False
        
    if state=="main_menu":
        mpos=pygame.mouse.get_pos()
        mousebuttons=pygame.mouse.get_pressed()
        screen.blit(menu_image, (0,0))
        pygame.draw.rect(screen, 'white', play_button_rect)
        screen.blit(font.render("PLAY", True, "black"), (play_button_rect.x + 10, play_button_rect.y + 10))
        if mousebuttons[0] and play_button_rect.collidepoint(mpos):
            state="game"
            game_reset=True

        players_rect=pygame.Rect(screen_width//2-275, screen_height//2+50, 550, 80)
        name_text=font.render("PLAYER NAMES", True, "black")
        pygame.draw.rect(screen, 'white', players_rect)
        screen.blit(name_text, (players_rect.x + 10, players_rect.y + 10))
        if mousebuttons[0] and players_rect.collidepoint(mpos):
            state="player_names"

        setting_rect=pygame.Rect(screen_width//2-200, screen_height//2+140, 400, 80)
        setting_text=font.render("SETTINGS", True, "black")
        pygame.draw.rect(screen, 'white', setting_rect)
        screen.blit(setting_text, (setting_rect.x + 25, setting_rect.y + 10))

    if state=="player_names":
        mpos=pygame.mouse.get_pos()
        mousebuttons=pygame.mouse.get_pressed()
        save_one_rect=pygame.Rect(25, 25, 250, 80)
        pygame.draw.rect(screen, 'white', save_one_rect)
        screen.blit(font.render("SAVE ONE", True, "black"), (save_one_rect.x + 10, save_one_rect.y + 10))
        if mousebuttons[0] and save_one_rect.collidepoint(mpos):
            player_names[0]=input("Enter Player 1's name: ")
        save_two_rect=pygame.Rect(25, 125, 250, 80)
        pygame.draw.rect(screen, 'white', save_two_rect)
        screen.blit(font.render("SAVE PLAYER 2 NAME", True, "black"), (save_two_rect.x + 10, save_two_rect.y + 10))
        if mousebuttons[0] and save_two_rect.collidepoint(mpos):
            player_names[1]=input("Enter Player 2's name: ")

    if state=="lose_screen":

        screen.blit(lose_image,(0,0))
        if guess%2!=0:
            lose_text = font.render(winning_player[1] + " " + losing_player[0], True, (255,0,0))
        elif guess%2==0:
            lose_text=font.render(winning_player[0] + " " + losing_player[1], True, (255,0,0))
        screen.blit(lose_text, (100,200))
        target_text=font.render(f"the word was {target_word}", True, "red")
        screen.blit(target_text, (100,300))

        mpos=pygame.mouse.get_pos()
        mousebuttons=pygame.mouse.get_pressed()
        playagain_button_rect=pygame.Rect(screen_width//2-300,screen_height-100,300,50)
        pygame.draw.rect(screen, 'white', playagain_button_rect)
        screen.blit(font_popup.render("HELL YEAH", True, "red"), (playagain_button_rect.x + 10, playagain_button_rect.y + 10))
        if mousebuttons[0] and playagain_button_rect.collidepoint(mpos):
            game_reset=True
            state="main_menu"
            reset=True
        dontplayagain_button_rect=pygame.Rect(screen_width//2,screen_height-100,300,50)
        pygame.draw.rect(screen, 'white', dontplayagain_button_rect) 
        screen.blit(font_popup.render("HELL NAH", True, "red"), (dontplayagain_button_rect.x + 10, dontplayagain_button_rect.y + 10))
        if mousebuttons[0] and dontplayagain_button_rect.collidepoint(mpos):
            pygame.quit()
            sys.exit()

    if state=="win_screen":
        mpos=pygame.mouse.get_pos()
        mousebuttons=pygame.mouse.get_pressed()
        if guess%2!=0:
            win_text = font.render(winning_player[1], True, (0,250,0))
        else:
            win_text = font.render(winning_player[0], True, (0,250,0))
        screen.blit(win_text, (100,100))
        target_text=font.render(f"the word was {target_word}", True, "white")
        screen.blit(target_text, (100,200))
        playagain_button=font.render("PLAY AGAIN?", True, "white")
        screen.blit(playagain_button, (100,400))
        guess_text=font.render(f"guesses taken: {guess-1}", True, "white")
        screen.blit(guess_text, (100,300))
        playagain_button_rect=pygame.Rect(100,500,300,50)
        pygame.draw.rect(screen, 'white', playagain_button_rect)
        screen.blit(font_popup.render("HELL YEAH", True, "red"), (playagain_button_rect.x + 10, playagain_button_rect.y + 10))
        if mousebuttons[0] and playagain_button_rect.collidepoint(mpos):
            game_reset=True
            state="main_menu"
            reset=True
        dontplayagain_button_rect=pygame.Rect(400,500,300,50)
        pygame.draw.rect(screen, 'white', dontplayagain_button_rect) 
        screen.blit(font_popup.render("HELL NAH", True, "red"), (dontplayagain_button_rect.x + 10, dontplayagain_button_rect.y + 10))
        if mousebuttons[0] and dontplayagain_button_rect.collidepoint(mpos):
            pygame.quit()
            sys.exit()
        
        screen.blit(win_image,(700,300))
        
    if state=="game":
        if game_reset:
            guess=1
            target_word=random.choice(five_letter_words)
            target=list(target_word)
            game_reset=False
            count=0
            shift_allow=False
        if reset:
            word_player1=[]
            word_player2=[]
            result1=[0]*5
            used1=[False]*5
            result2=[0]*5
            used2=[False]*5
            evaluated1=False
            evaluated2=False
            reset=False
            count=0
        if guess<len(popups):
            question_text = font_popup.render(popups[guess-1], True, (200,160,10))
        else:
            question_text = font_popup.render("fuck you", True, (200,160,10))
        screen.blit(question_text, (0,0))
        if guess%2!=0:
            turn_text = font.render(tell_player[0], True, (250,200,0))
        
        else:        
            turn_text = font.render(tell_player[1], True, (250,200,0))
        screen.blit(turn_text, (0,60))
        letter.draw()
        if count>0:
            count_text=font.render(f"WRONG GUESSES: {count}", True, (255,0,0))
            screen.blit(count_text, (0,120))
    
    pygame.display.update()
