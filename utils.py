import pygame

def get_cage_at_coordinates(group, x, y):
    for cage in group:
        if cage.rect.collidepoint(x, y):
            return cage
    return None