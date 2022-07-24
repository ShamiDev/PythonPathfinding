import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "O", "#", "#", "#", "#"],
    ["#", "#", " ", "#", " ", "#", " ", "#", "#"],
    ["#", "#", " ", "#", " ", " ", " ", "#", "#"],
    ["#", " ", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", "B", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", "#", "#", " ", " ", "#", "#"],
    ["#", "#", " ", " ", "#", " ", "#", "#", "#"],
    ["#", "#", " ", " ", "#", " ", " ", " ", "#"],
    ["#", " ", " ", "#", "#", " ", "#", "#", "#"],
    ["#", "#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", "#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "A", "#", "#"],
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr, start, end):
    start_pos = find_start(maze, start)
    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        curr_pos, path = q.get()
        row, col = curr_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            r, c = neighbour
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)


def find_neighbours(maze, row, col):
    neighbours = []

    if row > 0:
        neighbours.append((row - 1, col))  # checks up
    if row + 1 < len(maze):
        neighbours.append((row + 1, col))  # checks down
    if col > 0:
        neighbours.append((row, col - 1))  # checks left
    if col + 1 < len(maze[0]):
        neighbours.append((row, col + 1))  # checks right
    if row > 0 and col > 0:
        neighbours.append((row - 1, col - 1))  # checks up left
    if row > 0 and (col + 1 < len(maze[0])):
        neighbours.append((row - 1, col + 1))  # checks up right
    if (row + 1 < len(maze)) and col > 0:
        neighbours.append((row + 1, col - 1))  # checks down left
    if (row + 1 < len(maze)) and (col + 1 < len(maze[0])):
        neighbours.append((row + 1, col + 1))  # checks down right

    return neighbours


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr, "O", "A")
    find_path(maze, stdscr, "A", "B")
    stdscr.getch()


wrapper(main)

# print(find_start(maze, "O"))
