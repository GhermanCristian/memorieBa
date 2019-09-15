import pygame
import os

path = os.path.join(os.getcwd(), "Images")
ALL_IMAGES = {}

for file in os.listdir(path):
    imageName = file[:-5].upper() + "_" + file[-5]
    if "ICON" in imageName:
        continue
    ALL_IMAGES[imageName] = pygame.image.load(os.path.join(path, file))

SERGHEI_ICON1 = pygame.image.load(os.path.join(path, "SERGHEI_ICON1.jpg"))