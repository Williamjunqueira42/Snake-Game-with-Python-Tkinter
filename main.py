#  Snake game with Python Tkinter
#  William dos Santos Junqueira

from tkinter import *
from random import randint

tiles = 20
#  necessario installar a font joystix Monospace
lb_config = {'font': 'joystix\ Monospace 10', 'bg':'#253434', 'fg': 'white'}
 
class App():
    def __init__(self, master):  #  Metodo construtor

        #  Config da janela  

        self.master = master
        self.master.state('zoomed')  #  Fazer a janela começar em tela cheia 
        self.master.resizable(0, 0)
        self.master.title('Snake Game')
        self.master['bg'] = '#253434'

        #  Frames

        self.gameFrame = Frame(self.master, width=600, height=600, highlightbackground='white', highlightthickness=1)
        self.labelFrame = Frame(self.master, bg='#253434')

        self.labelFrame.place(x=0, y=0)
        self.gameFrame.place(anchor="c", relx=.5, rely=.5)

        #  Labels
        self.points = IntVar()
        self.points.set(0)
        
        self.lb_points = Label(self.labelFrame, lb_config, text=f'Points:')
        self.lb_npoints = Label(self.labelFrame, lb_config, textvariable=self.points)

        self.lb_points.grid(row=1, column=0,padx=5, pady=20)
        self.lb_npoints.grid(row=1, column=1)


        #  Canvas

        self.canvas = Canvas(self.gameFrame, width=600, height=600, bg='#264D4D')
        self.text = self.draw_text(300, 300, 'space to start')
        self.canvas.pack()

        #  Cobra

        self.snakeX = [20, 20, 20]  #  Posição x da cobra
        self.snakeY = [20, 21, 22]  #  Posição y da cobra
        self.snakeLength = 3  #  Largura da cobra
        self.key = 'Up'

        #  maçã
        self.appleX = randint(1, 28)
        self.appleY = randint(1, 28)

        #  Vincular teclas ao tk
        self.master.bind('<space>', lambda _: self.startGame())
        self.master.bind('<KeyPress>', self.getKey)
 

    #  Começar o jogo
    def startGame(self): 
        self.master.unbind('<space>')  #  Fazer a tecla espaço parar de "fucionar"
        self.canvas.delete(self.text)
        self.gameLoop()
   

    #  Pegar tecla pressionada no computador
    def getKey(self, event):
        keys = ['Up', 'Down', 'Left', 'Right', ' ']
        for v in keys: 
            if event.keysym == v: self.key = event.keysym


    #  Movimento da cobra
    def snakeMove(self):
        for i in range(self.snakeLength-1, 0, -1):
            self.snakeX[i] = self.snakeX[i-1]
            self.snakeY[i] = self.snakeY[i-1]
        
        #  movimento das teclas
        if self.key == 'Up': self.snakeY[0] -= 1  #  cima
        elif self.key == 'Down': self.snakeY[0] += 1  #  baixo
        elif self.key == 'Left': self.snakeX[0] -= 1  #  esquerda
        elif self.key == 'Right': self.snakeX[0] += 1  #  direita

        self.eatApple()


    #  Verificar se tem e comer a maçã                  
    def eatApple(self):
        if self.snakeX[0] == self.appleX and self.snakeY[0] == self.appleY:
            self.snakeLength += 1

            x = self.snakeX[len(self.snakeX)-1] #  pega a posiçao da ultima parte da cobra
            y = self.snakeY[len(self.snakeY) - 1]
            self.snakeX.append(x+1)  #  cria uma no parte da cobra
            self.snakeY.append(y)
            self.createNewApple()
            self.points.set(self.points.get() + 1)


    #  criar uma nova maçã 
    def createNewApple(self):
        self.appleX = randint(1, 28)
        self.appleY = randint(1, 28)


    #  Mostrar um texto na tela
    def draw_text(self, x, y, text, size=25, fg='white'):
        font = (f'joystix\ Monospace {size}')
        return self.canvas.create_text(x, y, text=text, font=font, fill=fg)
   
  
    #  Verificar se o jogo acabou
    def gameOver(self):
        #  Verificar se a cobra bateu nas leterais
        if self.snakeX[0] < 0 or self.snakeX[0] > 29 or self.snakeY[0] < 0 or self.snakeY[0] > 29:
            return True

        #  Verificar se a cobra bateu em si mesma
        for i in range(1, self.snakeLength):
            if self.snakeX[0] == self.snakeX[i] and self.snakeY[0] == self.snakeY[i]:
                return True

        return False  #  se o jogo não acabou retorna falso
   

    #  Loop do jogo
    def gameLoop(self):
        self.canvas.after(100, self.gameLoop)  #  Repete o metodo apos 200 milisegundos
        self.canvas.delete('all')  #  Apaga todos os elementos no canvas

        if self.gameOver() == False:
            self.snakeMove()

            #  Cabeça da Cobra
            self.canvas.create_rectangle(self.snakeX[0]*tiles, self.snakeY[0]*tiles, self.snakeX[0]*tiles+tiles, self.snakeY[0]*tiles+tiles, fill='white')

            #  Corpo da cobra
            for i in range(1, self.snakeLength):
                self.canvas.create_rectangle(self.snakeX[i]*tiles, self.snakeY[i]*tiles, self.snakeX[i]*tiles+tiles, self.snakeY[i]*tiles+tiles, fill='white')
        
            # maçã
            self.canvas.create_rectangle(self.appleX*tiles, self.appleY*tiles, self.appleX*tiles+tiles, self.appleY*tiles+tiles, fill='red')


        else:  #  fim do jogo
            self.draw_text(300, 300, 'GameOver!', 40)
            self.draw_text(300, 340,  f'Your Points:{self.points.get()}', 10)
            self.draw_text(300, 380,  f'Press r to restart', 10)
            self.master.bind('<r>', lambda _: self.replayGame())


    def replayGame(self):
        self.__init__(self.master)


if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()
    