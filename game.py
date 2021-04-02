import pygame, sys

def update():
    left_arrow = pygame.key.get_pressed()[pygame.K_RIGHT]
    right_arrow = pygame.key.get_pressed()[pygame.K_LEFT]
    up_arrow = pygame.key.get_pressed()[pygame.K_UP]
    return left_arrow, right_arrow, up_arrow

def main():

    pygame.init()
    screen_size = width, height = 626, 357
    screen = pygame.display.set_mode(screen_size)
    backround = pygame.image.load("space-game-background-with-landscape-planet_107791-1700.png")
    spaceship = pygame.image.load("spaceship.png")
    ufo = pygame.image.load("ufo.png")
    explosion = pygame.image.load("explosion.png")
    bullet = pygame.image.load("bullet.png")
    pygame.display.set_icon(spaceship)
    pygame.display.set_caption("Hello spaceship")
    explosionrect = explosion.get_rect()
    spaceshiprect = spaceship.get_rect()
    uforect = ufo.get_rect()
    bulletrect = bullet.get_rect()
    runing = True
    spaceshiprect = spaceshiprect.move(281,293)
    
    
    
    
    speed_bullet = [0,-5]
    number_ufo = 1
    number_ufo_spawn = 0
    number_bullet_spawn = 0
    number_bullets = 0
    time = 0
    time_passed = 0
    time_passed_ufos = 0
    bullets = {}
    ufos = {0 : [uforect.move(1,30), [3,0], 0, 0]}
    bullets_outside = []
    ufos_hit = []
    bullets_topop = []
    ufos_topop = []
    stop = 0
    ufo_bullets_spawn = 0
    ufo_bullets = {}
    ufo_bullets_topop = []
    ufo_number_bullets = 0
    while runing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        time = pygame.time.get_ticks()
        bulletrect = bullet.get_rect()
        explosionrect = explosion.get_rect()

        if time > (time_passed_ufos + 2000):
            time_passed_ufos = time
            number_ufo_spawn += 1
        
        for i in range(number_ufo_spawn):
            number_ufo_spawn -= 1
            number_ufo += 1
            ufos[number_ufo] = [uforect.move(1,30), [3,0], 0, 0]

        for key in ufos:
            if ufos[key][0].left < 0 or ufos[key][0].right > width:
                ufos[key][1][0] = -ufos[key][1][0]
            ufos[key][0] = ufos[key][0].move(ufos[key][1])

        left_arrow, right_arrow, up_arrow = update()

        if spaceshiprect.right < width: 
            if left_arrow:
                spaceshiprect = spaceshiprect.move(4,0)
        if spaceshiprect.left > 0:
            if right_arrow:
                spaceshiprect = spaceshiprect.move(-4,0)

        if up_arrow and (time  > (time_passed + 500)):
            number_bullet_spawn += 1 
            time_passed = time

        screen.blit(backround, (0,0))
        screen.blit(spaceship, spaceshiprect)
       
        for key in bullets:
            bullets[key] = bullets[key].move(speed_bullet)
        
        for i in range(number_bullet_spawn):
            number_bullets += 1
            bulletrect =  bulletrect.move((spaceshiprect[0] + 16),260)
            bullets[number_bullets] = bulletrect
            number_bullet_spawn -= 1
        
        for key in bullets:
            if bullets[key][1] < -32:
                bullets_outside.append(key)
        
        for i in bullets_outside:
            del bullets[i]
            
        bullets_outside = []
        
        for i in ufos_hit:
            del ufos[i]
            
        ufos_hit = []

        for i in ufos:
            if (ufos[i][2] + 1000) < time:
                ufos[i][2] = time
                ufos[i][3] = 1

        for i in ufos:
            if ufos[i][3] == 1:
                ufo_number_bullets += 1
                bulletrect = bulletrect.move((ufos[i][0][0] + 16),84)
                ufo_bullets[ufo_number_bullets] = bulletrect
                ufos[i][3] = 0
        
        for key in ufo_bullets:
            ufo_bullets[key] = ufo_bullets[key].move(0,4)
        
        for key in ufo_bullets:
            if ufo_bullets[key][0] > 358:
                bullets_topop.append(key)
        
        for i in bullets_topop:
            del ufo_bullets[i]

        bullets_topop = []

        for key in ufo_bullets:
            screen.blit(pygame.transform.rotate(bullet, 180), ufo_bullets[key])

        for key in bullets:
            screen.blit(bullet, bullets[key])

        for key in ufos:
            screen.blit(ufo, ufos[key][0])

        for key in ufos:
            for keys in bullets:
                if pygame.Rect.colliderect(ufos[key][0], bullets[keys]):
                    if stop == 0:
                            bullets_outside.append(keys)
                            stop += 1       
                    ufos_hit.append(key) 
                    screen.blit(explosion, explosionrect.move((bullets[keys][0]-16),30))           
        
        for keys in ufo_bullets:
            if pygame.Rect.colliderect(spaceshiprect, ufo_bullets[keys]):
                screen.blit(explosion, explosionrect.move((ufo_bullets[keys][0]-16),293))
                runing = False

        stop = 0
        pygame.time.Clock().tick(50)
        pygame.display.flip()

    
main()
