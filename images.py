import pygame
import os

path = os.path.join(os.getcwd(), "Images")
os.chdir(path)

BADEA_1 = pygame.image.load(os.path.join(path, "badea1.jpg"))
BADEA_2 = pygame.image.load(os.path.join(path, "badea2.png"))
BASE_1 = pygame.image.load(os.path.join(path, "base1.jpg"))   
BASE_2 = pygame.image.load(os.path.join(path, "base2.jpg"))
BECALI_1 = pygame.image.load(os.path.join(path, "becali1.jpg"))
BECALI_2 = pygame.image.load(os.path.join(path, "becali2.jpg"))
DOLANESCU_1 = pygame.image.load(os.path.join(path, "dolanescu1.jpg"))
GUTA_1 = pygame.image.load(os.path.join(path, "guta1.jpg"))
GUTA_2 = pygame.image.load(os.path.join(path, "guta2.jpg"))
ILIESCU_1 = pygame.image.load(os.path.join(path, "iliescu1.jpg"))   
JEREMY_1 = pygame.image.load(os.path.join(path, "jeremy1.png"))
PUYA_1 = pygame.image.load(os.path.join(path, "puya1.png"))
ROMEO_1 = pygame.image.load(os.path.join(path, "romeo1.jpg"))
VANDAME_1 = pygame.image.load(os.path.join(path, "vandame1.jpg"))
VANDAME_2 = pygame.image.load(os.path.join(path, "vandame2.png"))

#print (os.path.exists(path))