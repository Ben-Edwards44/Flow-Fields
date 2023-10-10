class Particle:
    def __init__(self, start_pos, screen_width, screen_height, vel_magnitude):
        self.x, self.y = start_pos

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.vel_mag = vel_magnitude

        self.vectors = []

        self.vel_x = 0
        self.vel_y = 0

    def get_closest(self):
        length = int(len(self.vectors)**0.5)
        scale = length / self.screen_width

        x, y = self.pos()

        grid_x = int(x * scale)
        grid_y = int(y * scale)

        closest = None
        for i in range(-1, 2):
            for x in range(-1, 2):
                if 0 <= grid_x + i < length and 0 <= grid_y + x < length:
                    current_vector = self.vectors[(grid_x + i) * length + (grid_y + x)]
                    dist = self.find_dist(current_vector)

                    if closest == None or dist < closest:
                        closest = dist
                        closest_vect = current_vector

        return closest_vect.vector
    
    def update_vel(self):
        x, y = self.get_closest()

        self.vel_x += x
        self.vel_y += y

        magnitude = self.vel_x**2 + self.vel_y**2
        scale = self.vel_mag / magnitude

        self.vel_x *= scale
        self.vel_y *= scale

    def main(self):
        self.update_vel()

        self.x += self.vel_x
        self.y += self.vel_y

        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0

        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

    find_dist = lambda self, vector: (self.x - vector.x)**2 + (self.y - vector.y)**2
    pos = lambda self: (int(self.x), int(self.y))