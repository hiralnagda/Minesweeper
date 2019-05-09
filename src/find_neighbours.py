def return_neighbours(position, rows, columns):
    neighbours = []
    x, y = position
    dx = [1, 1, 1, -1, -1, -1, 0, 0]
    dy = [0, 1, -1, 0, 1, -1, 1, -1]

    for i in range(0, len(dx)):
        row = x + dx[i]
        col = y + dy[i]

        if rows > row >= 0 and columns > col >= 0:
            neighbours.append((row, col))

    return neighbours
