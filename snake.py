class Snake:
    def __init__(self, row, col, color, head_color, id):
        self.row = row
        self.col = col
        self.color = color
        self.head_color = head_color
        self.direction = 'right'
        self.true_direction = 'right'
        self.head = 4
        self.apple_eaten = False
        self.id = id

    def update_position(self):
        if self.direction == 'up':
            self.col -= 1
        if self.direction == 'down':
            self.col += 1
        if self.direction == 'left':
            self.row -= 1
        if self.direction == 'right':
            self.row += 1
        self.true_direction = self.direction
    
    def set_position(self, row, col):
        self.row = row
        self.col = col


