from minesweeper import Minesweeper

rows = int(input("Enter the number of rows: "))
columns = int(input("Enter the number of columns: "))
prob = 0.1
mines = int(prob * rows * columns)
Minesweeper(rows, columns, mines, False).run()
Minesweeper(rows, columns, mines, True).run()
