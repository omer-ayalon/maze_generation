import random
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

current_pos = [0, 0]
visited_num = 0
visited_stack = []

grid_shape = [30, 30]

grid_visited = [[0 for _ in range(grid_shape[1])] for _ in range(grid_shape[0])]
grid_edges = [[[1, 1] for _ in range(grid_shape[1])] for _ in range(grid_shape[0])]

done = False


def draw():
    for j in range(grid_shape[1]):
        for i in range(grid_shape[0]):
            if grid_visited[i][j]:
                pygame.draw.rect(screen, (255, 255, 255), [j * width / grid_shape[1],
                                                           i * height / grid_shape[0],
                                                           width / grid_shape[1] + 1,
                                                           height / grid_shape[0] + 1])

            if grid_edges[i][j][0]:
                pygame.draw.line(screen, (0, 0, 0), [width / grid_shape[1] * j, height / grid_shape[0] * i],
                                 [width / grid_shape[1] * (j + 1), height / grid_shape[0] * i])
            if grid_edges[i][j][1]:
                pygame.draw.line(screen, (0, 0, 0), [width / grid_shape[1] * j, height / grid_shape[0] * i],
                                 [width / grid_shape[1] * j, height / grid_shape[0] * (i + 1)])

            if not done:
                pygame.draw.rect(screen, (0, 255, 0), [current_pos[1] * width / grid_shape[1],
                                                       current_pos[0] * height / grid_shape[0],
                                                       width / grid_shape[1] + 1,
                                                       height / grid_shape[0] + 1])


def get_neighbors(pos):
    arr = []
    if pos[0] > 0:
        if not grid_visited[pos[0] - 1][pos[1]]:  # Check Up
            arr.append([pos[0] - 1, pos[1]])
    if pos[1] < grid_shape[1] - 1:
        if not grid_visited[pos[0]][pos[1] + 1]:  # Check Right
            arr.append([pos[0], pos[1] + 1])
    if pos[0] < grid_shape[0] - 1:
        if not grid_visited[pos[0] + 1][pos[1]]:  # Check Down
            arr.append([pos[0] + 1, pos[1]])
    if pos[1] > 0:
        if not grid_visited[pos[0]][pos[1] - 1]:  # Check Left
            arr.append([pos[0], pos[1] - 1])

    return arr


while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    visited_stack.append(current_pos)
    grid_visited[current_pos[0]][current_pos[1]] = 1

    neighbors = get_neighbors(current_pos)

    if len(neighbors) > 0:
        rand = random.choice(neighbors)
        dy, dx = (rand[0] - current_pos[0]), (rand[1] - current_pos[1])

        if dy == 1:
            grid_edges[current_pos[0] + 1][current_pos[1]][0] = 0
        if dy == -1:
            grid_edges[current_pos[0]][current_pos[1]][0] = 0
        if dx == 1:
            grid_edges[current_pos[0]][current_pos[1] + 1][1] = 0
        if dx == -1:
            grid_edges[current_pos[0]][current_pos[1]][1] = 0

        current_pos = rand
        visited_num += 1

    else:
        if visited_num == grid_shape[0] * grid_shape[1] - 1:
            done = True
            # print('Done')
            # draw()
        else:
            while len(neighbors) == 0:
                current_pos = visited_stack.pop()
                neighbors = get_neighbors(current_pos)

    draw()

    pygame.display.flip()
    fpsClock.tick(0)
