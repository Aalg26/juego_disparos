import pygame
import os
import time
import sys
import pygame.font
pygame.init()
def game():
    
    screen_width = 1020
    screen_height = int(screen_width * 0.7)

    screen = pygame.display.set_mode((screen_width,screen_height))

    pygame.display.set_caption('Game')

    #defino framerate
    clock = pygame.time.Clock()
    FPS = 60

    #variables de juego

    GRAVITY = 0.75

    class Soldier(pygame.sprite.Sprite):
        def __init__(self,char_type,x,y,scale,speed,ammo,direction=1, flip=False):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            #define el tipo de soldado
            self.char_type = char_type
            #define la velocidad
            self.speed = speed
            self.ammo = ammo
            self.start_ammo = ammo
            self.shoot_cooldown = 0
            self.health = 400
            self.max_health = self.health
            #define la direccion
            self.direction = direction
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.flip = flip
            #guarda todas las imagenes de animacion 
            self.animation_list = []
            #define el frame actual
            self.frame_index = 0
            #define la accion
            self.action = 0
            #actualiza 
            self.update_time = pygame.time.get_ticks()

            #carga todas las imagenes
            animation_types = ['Idle','Run','Jump','Death']
            for animation in animation_types:
                temp_list = []
                #numero de imagenes en la carpeta
                num_imgs = len(os.listdir(f'img/{self.char_type}/{animation}/'))
                for i in range(num_imgs):
                    img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)
            
            #elige que imagen va a cargar dependiendo de la accion y del frame
            self.image = self.animation_list[self.action][self.frame_index]
            #posiciona la imagen
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            self.update_animation()
            self.check_alive()

            if self.shoot_cooldown >0:
                self.shoot_cooldown -=1

        #define el movimiento del jugador   
        def move(self,moving_left, moving_right):
            
            dx = 0
            dy = 0

            #movimiento
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1

            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

            #jump 
            if self.jump == True and self.in_air == False:
                self.vel_y = -20
                self.jump = False
                self.in_air = True
            #gravedad
            self.vel_y  += GRAVITY
            if self.vel_y > 10:
                self.vel_y            
            dy += self.vel_y
            #colision con el suelo 
            if self.rect.bottom + dy > 550:
                dy = 550 - self.rect.bottom
                self.in_air = False

            #actualiza la posicion de la imagen
            self.rect.x += dx
            self.rect.y += dy

        def update_animation(self):
            ANIMATION_COOLDOWN = 100
            #actualiza la imagen depediendo del frame actual
            self.image = self.animation_list[self.action][self.frame_index]
            #revisa si ha pasado suficiente tiempo desde la ultima actualizacion
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #Si la animacion ha llegado a su limite se resetea
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action ==3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo >0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + (0.6*self.rect.size[0]*self.direction),self.rect.centery, self.direction)
                bullet_group.add(bullet)
                self.ammo -=1


        def update_action(self,new_action):
            #revisa si la nueva accion es diferente a la anterior
            if new_action != self.action:
                self.action = new_action
                #actualiza la configuracion de las animaciones
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)


        def draw(self):
            screen.blit(pygame.transform.flip(self.image,self.flip, False), self.rect)




    class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y,direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction


        def update(self):
            self.rect.x += (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > screen_width:
                self.kill()
            if pygame.sprite.spritecollide(player1,bullet_group,False):
                if player1.alive:
                    player1.health -= 30
                    self.kill()
            if pygame.sprite.spritecollide(player2,bullet_group,False):
                if player2.alive:
                    player2.health -= 30
                    self.kill()


    bullet_group = pygame.sprite.Group()


    player1 = Soldier('player1',200,200,3,5, 20)
    player2 = Soldier('player2', 800, 200, 3, 5, 20,-1, True)


    #variables de accion 
    player1_moving_left = False
    player1_moving_right = False
    shoot1 = False

    player2_moving_left,player2_moving_right = False, False
    shoot2 = False

    #disparos
    bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

    #colores
    BG =  pygame.image.load("img/background/BG.jpg")
    BG = pygame.transform.scale(BG, (screen_width, screen_height))
    RED = (255,0,0)

    centerx = (screen_width ) // 2
    centery = (screen_height) // 2
    players = [player1, player2]
    players_name = ['player1', 'player2']
    font = pygame.font.Font(None, 80)
    def draw_bg():
        screen.blit(BG, (0, 0))
        


    def set_health(screen, x, y, health):
        if health < 0:
            health = 0
        width = 400  # Ancho de la barra de vida
        height = 50   # Altura de la barra de vida
        borde = 2  # Grosor del borde de la barra

        # Dibujar el fondo de la barra de vida (en gris)
        pygame.draw.rect(screen, (255,0,0), (x, y, width, height))

        # Dibujar la barra de vida (en verde)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health, height))

        # Dibujar el borde de la barra
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), borde)

    def draw_counter(screen, time):
        fuente = pygame.font.Font(None, 56)  # Fuente y tamaño del contador de tiempo
        texto = fuente.render(f'{time}', True, (255, 255, 255))  # Texto del contador
        screen.blit(texto, (500, 60))  # Posición del contador en la pantalla

    def get_remaining_time():
        current_time = time.time()
        time_elapsed = current_time - start_time
        remaining_time = time_to_finish - time_elapsed
        return max(remaining_time, 0) 
    def show_msg(text, x, y):
        msg = font.render(text, True, (0, 0, 0))  # Renderiza el texto en blanco
        text_rect = msg.get_rect()
        text_rect.center = (x, y)  # Configura el centro del rectángulo del texto
        screen.blit(msg, text_rect.topleft)

    start_time = time.time()
    time_to_finish = 60
    run = True
    draw_counter(screen, int(time_to_finish))
    dead_time = 0
    while run:
        #activa el limite de ticks
        clock.tick(FPS)
        #dibuja el fondo
        draw_bg()
        #define al jugador
        
        set_health(screen, 50, 50, player1.health)

        set_health(screen, 580, 50, player2.health)

        
        remaining_time = get_remaining_time()
        draw_counter(screen, int(remaining_time))



        for player in players:
            
            player.update()
            player.draw()

        
        
        #actualiza y refleja los groups
        bullet_group.update()
        bullet_group.draw(screen)

        for player in players:
            if player.alive:
            
                if player.in_air:
                    player.update_action(2) #salto
                
                if player.char_type == 'player1':
                    if shoot1:
                        player.shoot()

                    if player1_moving_left or player1_moving_right:
                        player.update_action(1)#corre
                    else:
                        player.update_action(0)#quieto
                    player.move(player1_moving_left,player1_moving_right)
                else:
                    if shoot2:
                        player.shoot()
                    if player2_moving_left or player2_moving_right:
                        player.update_action(1)#corre
                    else:
                        player.update_action(0)#quieto
                    player.move(player2_moving_left,player2_moving_right)
        
        for event in pygame.event.get():
            #quit the game
            if event.type == pygame.QUIT:
                run = False

            #keyboard press
            if event.type == pygame.KEYDOWN and player1.alive and player2.alive:
                if event.key == pygame.K_a:
                    player1_moving_left = True

                if event.key == pygame.K_LEFT:
                    player2_moving_left = True

                if event.key == pygame.K_w:
                    player1.jump = True

                if event.key == pygame.K_UP:
                    player2.jump = True 

                if event.key == pygame.K_d:
                    player1_moving_right = True

                if event.key == pygame.K_RIGHT:
                    player2_moving_right = True

                if event.key == pygame.K_SPACE:
                    shoot1 = True
                
                if event.key == pygame.K_DOWN:
                    shoot2 = True
                
                    
                if event.key == pygame.K_ESCAPE:
                    run = False

            #keyboard released
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_a:
                    player1_moving_left = False

                if event.key == pygame.K_LEFT:
                    player2_moving_left = False

                if event.key == pygame.K_d:
                    player1_moving_right = False

                if event.key == pygame.K_RIGHT:
                    player2_moving_right = False
                
                if event.key == pygame.K_SPACE:
                    shoot1 = False

                if event.key == pygame.K_DOWN:
                    shoot2 = False

        
        if player1.health <=0 or player2.health <=0: 
            dead_time += 1
            winner = player1.char_type
            
            if player1.health > player2.health:
               text=(f'El {winner} gana ')
               show_msg(text,centerx,centery)     

            elif player1.health == player2.health:
                text=('Ambos jugadores han muerto, es un empate')
                show_msg(text,centerx,centery) 
            else:
                winner = player2.char_type
                text=(f'El {winner} gana ')
                show_msg(text,centerx,centery) 
            
            if dead_time >70:
            
                run = False
        if remaining_time == 0:
            run = False
            text=('El tiempo acabó, es un empate')
            show_msg(text,centerx,centery) 

                   
            


        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    game()