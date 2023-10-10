import perlin_noise
import vector
import particle
import pygame
from random import randint
from numpy import zeros
from math import pi


NUM_PARTICLES = 1000
VEL_MAGNITUDE = 4

VECTORS_X = 64
VECTORS_Y = 64
TOTAL_TIME = 128
OCTATES = 4

EVAPORATE_RATE = 0.99
PARTICLE_COLOUR = 150
FIELD_SPEED = 12

SCREEN_X = 800
SCREEN_Y = 800


pygame.init()
pygame.display.set_caption("Flow fields")

window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
screen_array = zeros((SCREEN_X, SCREEN_Y))


def create_vectors(time, noise_array):
    vectors = []

    scale_x = SCREEN_X // VECTORS_X
    scale_y = SCREEN_Y // VECTORS_Y
    
    for x in range(VECTORS_X):
        for y in range(VECTORS_Y):
            noise = noise_array[time][x][y]
            angle = (noise + 0.7) / 1.4 * pi * 2

            vectors.append(vector.Vector(0.5, (x * scale_x, y * scale_y), angle))

    return vectors


def precompute_vectors():
    vectors = []

    noise_array = perlin_noise.generate_fractal_noise_3d((TOTAL_TIME, VECTORS_X, VECTORS_Y), (8, 4, 4), OCTATES)

    for i in range(TOTAL_TIME):
        current = create_vectors(i, noise_array)
        vectors.append(current)

    return vectors


def create_particles(num):
    particles = []

    for _ in range(num):
        x = randint(0, SCREEN_X)
        y = randint(0, SCREEN_Y)

        particles.append(particle.Particle((x, y), SCREEN_X, SCREEN_Y, VEL_MAGNITUDE))

    return particles


def draw(particles):
    global screen_array

    for i in particles:
        x, y = i.pos()

        if x > SCREEN_X - 1:
            x = SCREEN_X - 1
        if y > SCREEN_Y - 1:
            y = SCREEN_Y - 1

        screen_array[x][y] = PARTICLE_COLOUR

    screen_array *= EVAPORATE_RATE

    pygame.surfarray.blit_array(window, screen_array)
    pygame.display.update()


def update_particles(particles, vectors):
    for i in particles:
        i.vectors = vectors
        i.main()


def main():
    vector_sets = precompute_vectors()
    particles = create_particles(NUM_PARTICLES)

    inx = 0
    vector_inx = 0
    while True:
        vectors = vector_sets[vector_inx % len(vector_sets)]

        if inx % FIELD_SPEED == 0:
            vector_inx += 1

        inx += 1

        update_particles(particles, vectors)
        draw(particles)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()


main()