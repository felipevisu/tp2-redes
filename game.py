import pygame
import random
import time

LIGHT_GRAY = (200, 200, 200)

IMG_CARS = []

for i in range(0,8):
    IMG_CARS.insert(i , pygame.image.load('imagens/carro'+str(i+1)+ 'L' + '.png'))
    IMG_CARS.insert(i+8 , pygame.image.load('imagens/carro'+str(i+1)+ 'R' + '.png'))

IMG_GALINHA = [
    pygame.image.load('imagens/galinha1.png'),
    pygame.image.load('imagens/galinha2.png')
]

class Street():
    def __init__(self, x, y, orientation, speed, space):
        self.x = x
        self.y = y
        self.orientation = orientation # Sentido do tráfego
        self.speed = speed # Velocidade do tráfego
        self.space = space # Distância entre os carros
        self.cars = []

    def draw(self, screen):
        
        for car in self.cars:
            car.draw(screen)

    # Movimenta os carros correspondes a rua
    def move(self):
        for car in self.cars:
            car.move(self.orientation, self.speed)

    # Cria um novo carro para o tráfego da rua em questão
    # O carro está sugeito a orientação e velocidade configurados para a rua
    # O primeiro carro é posicionado aleatóriamente
    # Os demais carros são posicionados pela distância definina para a rua
    def new_car(self):
        color = random.randint(1, 8) 

        if len(self.cars) > 0:
            x = (self.cars[-1].x_initial + self.space)%1300
            self.space += 100
        else:
            x = random.randint(0, 1300)

        car = Car(x, self.y, color, self.orientation)
        self.cars.append(car)


class Car():
    imagem = None
    def __init__(self, x, y, cor, orientacao):
        self.x_initial = x
        self.y_initial = y
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y,(39 if cor < 5 else 80), 25)
        self.cor = cor
        self.orientacao = orientacao

    def draw(self, screen):
        screen.blit(IMG_CARS[self.cor-1+8*(1 if self.orientacao==1 else 0)],self.rect)

    # O carro recebe orientação e velocidade da rua a qual pertence
    def move(self, orientation, speed):
        if orientation == -1 and self.x < - 450:
            self.x = 1300

        if orientation == 1 and self.x > 1300:
            self.x = -450

        self.x += speed * orientation
        self.update()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Player():

    def __init__(self, x, y, color):
        self.id = None
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, 45, 30)
        self.speed = 8
        self.pontuation = 0
        self.life = 3

    def draw(self, screen):
        screen.blit(IMG_GALINHA[self.color-1],self.rect)
        self.set_life(screen)

    # Imprime a vida do jogador na tela
    def set_life(self, screen):
        pygame.font.init()
        font = pygame.font.SysFont(None, 30)
        lifes_text = "Vidas " + str(self.life)
        lifes = font.render(lifes_text, True, (0, 0, 0))
        if self.id == 0:
            x = 30
        else:
            x = 878 - lifes.get_width() - 30
        screen.blit(lifes, (x, 0))

    # Movimnenta o jogador
    def move(self, cars):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 570:
            self.y += self.speed

        # Testa a colisão com os carros
        for car in cars:
            if self.rect.colliderect(car.rect):
                self.y = 570
                self.life -= 1
                break

        if self.y < 25:
            self.y = 570
            self.pontuation += 1

        self.update()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Game():
    def __init__(self):
        self.id = None
        self.players = [None, None]
        self.streets = []
        self.winner = None

    def get_cars(self):
        cars = []

        for street in self.streets:
            for car in street.cars:
                cars.append(car)

        return cars

    def get_score(self):
        return str(self.players[0].pontuation) + " a " + str(self.players[1].pontuation)

    # Imprime na tela a pontuação dos jogadores
    def set_score(self, screen):
        pygame.font.init()
        font = pygame.font.SysFont(None, 30)
        score_text = "Sala " + str(self.id) + ' / Placar: ' + self.get_score()
        score = font.render(score_text, True, (0, 0, 0))
        screen.blit(score, (439 - score.get_width() // 2, 0))

    # O jogador 1 está esperando o jogador 2 se conectar
    def waiting(self, screen):
        screen.fill(LIGHT_GRAY)
        font = pygame.font.SysFont(None, 30)
        text = "Aguardando o segundo jogador"
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (439 - text.get_width()//2, 305 - text.get_height()//2))

    # Contagem regressiva para início do jogo
    def countdown(self, screen):
        font = pygame.font.SysFont(None, 75)
        countdown = ['3', '2', '1', 'Ready!']

        for count in countdown:
            screen.fill(LIGHT_GRAY)
            text = font.render(count, True, (0, 0, 0))
            screen.blit(text, (439 - text.get_width()//2, 305 - text.get_height()//2))
            pygame.display.update()
            time.sleep(1)

    # Jogo finalizado, algum jogador venceu
    def finalize(self, screen):
        screen.fill(LIGHT_GRAY)
        font = pygame.font.SysFont(None, 30)
        text = "O jogador " + str(self.winner + 1) + " venceu!"
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (439 - text.get_width()//2, 305 - text.get_height()//2))
        pygame.display.update()
        time.sleep(3)

    # Jogo em execução
    def render(self, screen):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('audio/ambiente.mp3')
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)

        background = pygame.image.load('imagens/background.png')
        screen.blit(background,(0,0))

        for street in self.streets:
            street.draw(screen)

        self.players[0].draw(screen)
        self.players[1].draw(screen)

        self.set_score(screen)

    def set_winner(self):
        for player in self.players:
            if player:
                if player.pontuation == 3:
                    self.winner = player.id
                if player.life == 0:
                    self.winner = (player.id-1)**2

def new_game():
    game = Game()
    game.streets = [
        Street(0, 62+6, -1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 111+6, -1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 160+6, -1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 209+6, -1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 258+6, -1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 310+6, 1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 359+6, 1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 408+6, 1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 457+6, 1, random.randint(5, 10), random.randint(100,220)),
        Street(0, 506+6, 1, random.randint(5, 10), random.randint(100,220)),
    ]

    for street in game.streets:
        street.new_car()
        street.new_car()
        street.new_car()
        street.new_car()

    return game


player_types = [
    Player(200, 570, 1),
    Player(660, 570, 2)
]
