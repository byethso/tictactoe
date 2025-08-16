import pygame

from utils import get_cage_at_coordinates


class Cage(pygame.sprite.Sprite):
    def __init__(self, x, y, size, images, state):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        self.images = images
        self.image = pygame.transform.scale(self.images[self.state], (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_blocked=False

    def change_state(self, state):
        self.state = state
        self.image = pygame.transform.scale(self.images[self.state], (self.size, self.size))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, size1, size2, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = pygame.transform.scale(self.images["BUTTON"], (size1, size2))
        self.rect = self.image.get_rect(topleft=(x, y))

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, size1, size2, font_size=30, text_color=(5,5,5)):
        pygame.sprite.Sprite.__init__(self)
        self.rect=pygame.Rect(x, y, size1, size2)
        self.font=pygame.font.Font(None, font_size)
        self.text_color=text_color
        self.text="Stroke X"
        self.image=pygame.Surface((size1, size2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.update_image()
    def change_text(self, text):
        self.text = text
        self.update_image()
    def update_image(self):
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.screen_width = 760
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.images = {"EMPTY": pygame.image.load("empty.PNG"),
                       "O": pygame.image.load("o.PNG"),
                       "X": pygame.image.load("x.PNG"),
                       "BUTTON": pygame.image.load("button.PNG")}
        self.configuration = [160, 100, 120, 40]
        self.all_cages = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        for row in range(3):
            for col in range(3):
                x = self.configuration[0] + col * (
                        self.configuration[2] + self.configuration[3])
                y = self.configuration[1] + row * (
                        self.configuration[2] + self.configuration[3])
                cage = Cage(x, y, self.configuration[2], self.images, "EMPTY")
                self.all_cages.add(cage)
                self.all_sprites.add(cage)
        button = Button(350, 560, 100, 30, self.images)
        self.all_sprites.add(button)
        self.buttons.add(button)

        self.textbox = TextBox(350, 65, 150, 60)
        self.textbox.change_text("Stroke X")
        self.all_sprites.add(self.textbox)

        self.selected_cage = "X"
        self.count_steps = 0
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_events(event)
            self.update()
            self.draw()
        pygame.quit()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def redraw_field(self):
        for sprite in self.all_cages:
            sprite.change_state("EMPTY")
            sprite.is_blocked = False
            self.selected_cage = "X"
            self.count_steps = 0

    def block_cage_on_field(self):
        for cage in self.all_cages:
            if cage.state == "EMPTY":
                cage.is_blocked = True

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for sprite in self.all_sprites:
                if sprite.rect.collidepoint(mouse_pos):
                    if self.all_cages.has(sprite):
                        if sprite.state == "EMPTY" and not sprite.is_blocked:
                            sprite.change_state(self.selected_cage)
                            if self.selected_cage == "X":
                                self.selected_cage = "O"
                                self.textbox.change_text("Stroke O")
                            else:
                                self.selected_cage = "X"
                                self.textbox.change_text("Stroke X")
                            self.count_steps += 1
                            self.is_win(sprite)
                    elif self.buttons.has(sprite):  # если не клетка, то кнопка, значит надо перерисовать поле. создан доп группа buttons, чтобы текст не был кликабельным
                        self.redraw_field()
                        self.textbox.change_text("Stroke X")
                        self.count_steps = 0

    def is_win(self, cage):
        self.coordinates = (cage.x, cage.y)
        # self.win_situations=[[1,2,3],[4,5,6], [7,8,9], [1,5,9], [3,5,7], [1,4,7], [2,5,8], [3,6,9]]
        self.win_situations = [[(160, 100), (320, 100), (480, 100)], [(160, 260), (320, 260), (480, 260)],
                               [(160, 420), (320, 420), (480, 420)],
                               [(160, 100), (320, 260), (480, 420)], [(480, 100), (320, 260), (160, 420)],
                               [(160, 100), (160, 260), (160, 420)], [(320, 100), (320, 260), (320, 420)],
                               [(480, 100), (480, 260), (480, 420)]]

        for i in range(len(self.win_situations)):
            if self.coordinates in self.win_situations[i]: #если в победной ситуации есть наша последняя заполненная ячейка
                temp = self.win_situations[i]
                temp.remove(self.coordinates)
                kol = 0
                for j in range(len(temp)):
                    x, y = temp[j]
                    sprite = get_cage_at_coordinates(self.all_cages, x, y)
                    if sprite.state != "EMPTY" and sprite.state != self.selected_cage:
                        kol += 1
                if kol == len(temp):
                    if self.selected_cage == "O":
                        self.textbox.change_text("Win X. Play again")
                        self.block_cage_on_field()
                    else:
                        self.textbox.change_text("Win O. Play again")
                        self.block_cage_on_field()
        if self.count_steps == 9:
            self.textbox.change_text("Draw. Play again")
            self.block_cage_on_field()


if __name__ == "__main__":
    game = Game()
    game.run()
