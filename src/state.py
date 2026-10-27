def attributesOfLevel(width, height, mapData, itemsData): 
    # attributesOfLevel is a function that reads the entire map, then it will return its attributes like bricks, targets, cats, and crates.
    bricks = set() # this is an empty set, however it will hold the rows and columns (row, column) of the walls surrounding the map.
    targets = set() # same goes for targets; an empty set.
    crates = set() # same goes for crates; an empty set.
    cat = None # the reason as to why this is set to none, is because the cat/player is supposedly not found yet, however, it will become one and will also read (row, column)

    for r in range(height): # This will go through every single row number. For example, 0, 1, 2, up to height - 1
        for c in range(width): # This will also go though every single column number inside the specific row
    # Think of this like a nested for loop, this will run a program that will scan through the entire map counting each block.
    # For example if height was 10, 'r' will run 10 times, but if 'c' was 5, it will run 5 times inside that 1 'r' run. 
            block = mapData[r][c] # This is used to know what on a specific cell, whether its a brick, a target, or even blank, it reads from the mapData and stores it to 'block'
            if block == '#': bricks.add((r, c)) # all this logic says is if that specific block is '#' then it's a the wall, and we add it to our bricks variable to remember its position
            elif block == '.': targets.add((r, c)) # same goes here, if the block is '.', then it's the target, and we add it to our targets variable to remember its position
            item = itemsData[r][c] # Same logic as mapData, but instead we are reading itemsData and storing the crate, player, and a blank block into the item variable
            if item == '@': cat = (r, c) # if item has the '@' symbol, it means that the cat is there
            elif item == '$': crates.add((r, c)) # Same logic as the bricks and the targets, if the item is '$', then it's a crate
    return bricks, targets, cat, frozenset(crates)
    # So basicaly, return the values gotten and sends them to their respected variables.
    # We make crates a "frozenset()" which only means that the variable can't be changed once it's made, that's why we call it frozenset, it's set frozen/locked
    # The reasons as to why the crates are frozenset is so that the search logic will be able to store its value    

Directions = { # Directions serves as a directory, and each direction (up, down, left, right) is connected to how the rows and columns (r, c) change and move.
    'u': (-1, 0), # row moving upwards = (row - 1) and the columns is 0, because the value won't change, you're not going left or right here
    'd': (1, 0), # same logic applies, row moving downwards = (row + 1)
    'l': (0, -1), # column moving to the left = (column - 1), row value doesn't change
    'r': (0, 1), # column moving to the right = (column + 1), row value doesn't change
    } # One quick note, notice how the row subtracts when moving upwards (up = row - 1), this is because rows will count downwards from the top, that's why subtracting it actually goes upwards


# This function is used to get every single possible move that the player/cat can make, and what the board looks like after making a certain move.
# Now, because we need to get every single poosible move, we'll need the Cat, crates, and bricks function.
# Need 'cat' variable to know where the player is in the board (row, column).
# Need 'crates' frozenset variable to know what changes and where the crates are in the board.
# Need 'bricks' variable to know where the postion of the walls are.
def nextLegalMoves(cat, crates, bricks) : 
    nextMoves = [] # We are defining an empty list to get the possible next moves we find.
    for move, (dr, dc) in Directions.items():   
    # What this means: This for loop will go through the list of every move pairs (pairs: u = (-1, 0), d = (1, 0), etc...)  
    # ".items" is what turns the dictionary into pairs
        nextCell = (cat[0] + dr, cat[1] + dc) # This line now adds the difference/change of the cat's position to be able to get the cell next to it. Note that the cat doesn't move, it just checks the positions of the cat
        # Example: let's say the cat is at cell (1, 2) and it wants to move a cell up. What the line above does is it adds the change of position to (1, 2).
        # So, (2, 3) moving up will look like: ((2+(-1), 3 + 0)) = (1, 3). (1, 3) is the cell if the cat would move up from (2, 3)
        if nextCell in bricks: # If statement that checks if the next cell is a brick wall
            continue # if it is a wall, then skip this cell and go to the next cell in the loop.
        if nextCell in crates: # Another if statement to check if there is a crate in the next cell
            vacant = (nextCell[0] + dr, nextCell[1] + dc) 
            # Now, we initialize this vairable called "vacant", and this is to check if there is a vancant cell behind the crate (in the same direction, one more step)
            if vacant in bricks or vacant in crates: # This is an if statement to check if there is a brick or a crate behind it
                continue 
                # Similar to the logic on checking if the next cell is the brick wall, 
                # if there is a crate or a brick, then the crate can't be pushed or moved anymore and we skip it
            newCrates = (crates - {nextCell}) | {vacant}
            # What does this code mean? 
            # We need to initialize "newCrates", because when we push a crate, the board has to describe the result on what it looks like, after we push that specific crate
            # Technically without this logic, if the cat tries to push a crate, the program will not detect that it pushed the crate.
            # Instead, the cat will just step into the crate's cell without the crate itself moving
            nextMoves.append((move, nextCell, newCrates)) # Now, it saves all of the variables, like: the letter, the cat's new position, and the changes as to where the crates are.
        else: # else if it's not a brick, crate, then it's an empty cell or a target
            nextMoves.append((move, nextCell, crates)) # Just save the walk with nothing changing

    return nextMoves # After all of the 4 directions are done, return and send back the entire list

# Lastly, this last remaining function simply checks if all crates are sitting on their respective targets, and the goal is achieved. Hence the function name goalAchieved
# All this function needs is the frozenset of where the crates are and where the targets are.
# In short, Needs: frozenset crates, targets; Function checks if all crates are in their respective targets; if so, goal is achieved.
def goalAchieved(crates, targets):
    return crates.issubset(targets) 
    # This returns a true or false value, 
    # basically what the .issubset() function does is check if all of the crate's positions are one of the targets
    # Example: if the crates are in {(1, 4), (3, 1), (3, 2), (3, 4)} and the targets = {(1, 4), (3, 1), (3, 2), (3, 4)}, then the goal is achieved!
    # However, if just one of the crates doesn't match a target, then the game is not yet over. 
