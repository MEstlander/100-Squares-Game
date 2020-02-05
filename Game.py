import pygame
import time
pygame.font.init()


class Grid:
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win
        self.value = 1
        self.last = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self):
        val = self.value
        (row, col) = self.selected
        if self.cubes[row][col].value == 0:
            if valid(self.model, self.last, (row,col)):
                self.value += 1
                self.last = (row, col)
                self.cubes[row][col].set(val)
                self.update_model()
                return True
            else:
                self.cubes[row][col].set(0)
                self.update_model()
                return False

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 10
        for i in range(self.rows+1):
            thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        if self.value == 1:
            return
        last_found = False
        val = 0
        row, col = self.last
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == self.value - 2:
                    last_found = True
                    self.last = (i, j)
                if val != 0 and last_found:
                    break
        self.value -= 1
        if self.value == 1:
            self.last = None
        self.cubes[row][col].set(0)
        self.update_model()


    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 10
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 100:
                    return True
        l0, l1 = self.last
        valid_left = False
        valid_pos = [[l0, l1+3], [l0, l1-3], [l0-3, l1], [l0+3, l1], [l0+2, l1+2], [l0+2, l1-2],[l0-2, l1-2], [l0-2, l1+2]]
        for i in valid_pos:
            if not (i[0] < 0 or i[0] > 9 or i[1] < 0 or i[1] > 9):
                if self.cubes[i[0]][i[1]].value == 0:
                    valid_left = True
                    break
        if valid_left:
            return False
        else:
            return True


class Cube:
    rows = 10
    cols = 10

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 10
        x = self.col * gap
        y = self.row * gap

        if not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 1)

    def set(self, val):
        self.value = val

def valid(bo, last, pos):
    # Check row
    if last == None:
        return True
    if bo[pos[0]][pos[1]] != 0:
        return False
    if (pos[0] == last[0] and ((pos[1] == last[1] + 3) or pos[1] == last[1] - 3)):
        return True
    if (pos[1] == last[1] and ((pos[0] == last[0] - 3) or pos[0] == last[0] + 3)):
        return True
    if (pos[0] == last[0] + 2 and pos[1] == last[1] + 2) or (pos[0] == last[0] + 2 and pos[1] == last[1] - 2):
        return True
    if (pos[0] == last[0] - 2 and pos[1] == last[1] - 2) or (pos[0] == last[0] - 2 and pos[1] == last[1] + 2):
        return True
    return False

def redraw_window(win, board, time):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("100 Squares game")
    board = Grid(10, 10, 540, 540, win)
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    board.clear()

                if event.key == pygame.K_RETURN:
                    if board.is_finished():
                        print("Game over")
                        run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    board.place()

        redraw_window(win, board, play_time)
        pygame.display.update()


main()
pygame.quit()