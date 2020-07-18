#submarine.py
import pygame
import os
import random
#opengameart.org

#GEOMETRY
WIDTH = 500
HEIGHT = 500
FPS = 30 #frame rate per second

#color picker
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

#Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Game Submarine')
clock = pygame.time.Clock() 


img_dir = os.path.join(os.path.dirname(__file__),"img")
snd_dir = os.path.join(os.path.dirname(__file__),"snd")

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def newmob():
	em = Enemy()
	all_sprites.add(em)
	enemy.add(em)		

def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (pct / 100) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH,BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, RED, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)	

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x +30 * i
		img_rect.y = y
		surf.blit(img, img_rect)





class Submarine(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((50,40))
		
		self.image = pygame.transform.scale(player_img,(50,60) )
		self.image.set_colorkey(BLACK)
		#self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.radius = 20
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT -10
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()

		

	def update(self):
		#unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer >1000:
			self.hidden = False
			self.rect.centerx = WIDTH/ 2
			self.rect.bottom = HEIGHT - 10
			
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8

		if keystate[pygame.K_RIGHT]:
			self.speedx = 8

		if keystate[pygame.K_SPACE]:
			self.shoot()

		self.rect.x += self.speedx

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH

		if self.rect.left < 0:
			self.rect.left = 0

		print(self.rect.centerx)

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx , self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)

	def hide(self):
		#hide the player temporarily
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2, HEIGHT + 200)	

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((30,40))
		#self.image.fill(WHITE)

		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()

		#self.image = meteor_img
		#self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width *.85 / 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,5)
		self.sprrdx = random.randrange(-3,3)
		self.rot = 0
		self.rot_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center


	def update(self):
		self.rotate()
		   #self.rect.x += self.speed.x
		self.rect.y += self.speedy

		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,5)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((10,20))
		#self.image.fill(BLUE)
		self.image = pygame.transform.scale(bullet_img,(20,20)) 
		self.image.set_colorkey(BLACK)

		self.rect =self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


#Load all game graphics
background = pygame.image.load(os.path.join(img_dir,"bg_shroom.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir,"alien.png.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 30))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(os.path.join(img_dir,"bee.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir,"alienPink_badge1.png")).convert()
meteor_images = []
meteor_list =['bat.png','ghost.png','ladyBug.png','mouse.png']


for img in meteor_list:
	meteor_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
	filename = 'sonicExplosion0{}.png'.format(i)
	img = pygame.image.load(os.path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (60,60))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32,32))
	explosion_anim['sm'].append(img_sm)

	filename = 'sonicExplosion0{}.png'.format(i)
	img = pygame.image.load(os.path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	explosion_anim['player'].append(img)


#Load all game sounds
pygame.mixer.music.load(os.path.join(snd_dir,"Fluffy style_0.mp3"))
pygame.mixer.music.set_volume(0.4)	
player_die_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'rumble1.ogg'))



#sprite is a player
all_sprites = pygame.sprite.Group()
#Add submarine
submarine = Submarine()
all_sprites.add(submarine)

enemy = pygame.sprite.Group()

bullets = pygame.sprite.Group()


for i in range(10):
	newmob()
	#em = Enemy()
	#all_sprites.add(em)
	#enemy.add(em)	

score = 0
pygame.mixer.music.play(loops=-1)

running = True
while running:
	clock.tick(FPS)

	for event in pygame.event.get():
		#check for closing
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
			   	submarine.shoot()

	all_sprites.update()


	#Check hits enemy
	
	hits = pygame.sprite.groupcollide(enemy ,bullets,True,True)
	for hit in hits:
		score += 1
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl)
		newmob()
		#em = Enemy()
		#all_sprites.add(em)
		#enemy.add(em)

#check mob hit player
	hits = pygame.sprite.spritecollide(submarine,enemy, True ,pygame.sprite.collide_circle)
	for hit in hits:
		submarine.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl)
		newmob()
		if submarine.shield <= 0:
			player_die_sound.play()
			death_explosion = Explosion(submarine.rect.center,'player')
			all_sprites.add(death_explosion)
			#submarine.kill()
			submarine.hide()
			submarine.lives -= 1
			submarine.shield =100
			

	#if the player died and the explosion has finished playing
	if submarine.lives == 0 and not death_explosion.alive():
		running = False	

	screen.fill(BLACK)
	screen.blit(background,background_rect)
	all_sprites.draw(screen)
	draw_text(screen ,str(score), 18,WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, submarine.shield)
	draw_lives(screen, WIDTH - 100, 5, submarine.lives, player_mini_img)
	pygame.display.flip()

pygame.quit()	
