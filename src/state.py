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
