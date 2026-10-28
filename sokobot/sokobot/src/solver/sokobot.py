import time


class SokoBot:

    Directions = { # Directions serves as a directory, and each direction (up, down, left, right) is connected to how the plane (r, c) changes and moves.
    'u': (-1, 0), # UP; (row - 1)
    'd': (1, 0), # DOWN; (row + 1)
    'l': (0, -1), # LEFT; (column - 1)
    'r': (0, 1), # RIGHT; (column + 1)
    } 

    @staticmethod
    def attributesOfLevel(width, height, mapData, itemsData): # function that reads the entire map, after reading it will return its attributes (e.g. bricks, targets, cats, and crates.)
    
        # set() will hold the rows and columns (row, column) of the attributes for the entire map.
        bricks = set() 
        targets = set() 
        crates = set() 

        # set to none, cat/player is not found yet, will become one and will also read (row, column)
        cat = None 

        # Nested loop to go through every row and column number.
        for r in range(height): 
            for c in range(width): 

                # @block used to know the attribute within the current cell, stores into 'block' after reading from mapData.
                block = mapData[r][c] 

                # checks if block is a wall ('#'), if block is a target ('.'), adds their corresponding attribute and sets it to the position.
                if block == '#': bricks.add((r, c)) 
                elif block == '.': targets.add((r, c))
                
                # @item reads itemsData and storing the attributes into the 'item' variable.
                item = itemsData[r][c] 

                # checks if item is a cat ('@'), if block is a crate ('$'), adds their corresponding attribute and sets it to the position.
                if item == '@': cat = (r, c) 
                elif item == '$': crates.add((r, c)) 

        # return the values obtained and sends them to their respected positions.
        # @frozenset() variable can't be changed once it's made
        return bricks, targets, cat, frozenset(crates)

    @staticmethod
    def nextLegalMoves(cat, crates, bricks, width, height) :

        # @xibcera, @mjbee, add board boundary checks for both nextCell and vacant.
        nextMoves = [] # We are defining an empty list to get the possible next moves we find.

        # for loop will go through every considerable list of moves.
        for move, (dr, dc) in SokoBot.Directions.items():   
            
            # Check if the next cell is within the bounds of the board
            nextCell = (cat[0] + dr, cat[1] + dc)
            if nextCell[0] < 0 or nextCell[0] >= height or nextCell[1] < 0 or nextCell[1] >= width:
                continue

            # line adds difference/change of the cat/player's current position
            nextCell = (cat[0] + dr, cat[1] + dc) # This line now adds the difference/change of the cat's position to be able to get the cell next to it. Checks the positions of the cat
            # Example: let's say the cat is at cell (1, 2) and it wants to move a cell up. What the line above does is it adds the change of position to (1, 2).
            
            if nextCell in bricks: # If statement that checks if the next cell is a brick wall
                
                continue # if  wall, then skip cell and go to the next cell.

            # if statement to check if there is a crate in the next cell
            if nextCell in crates: 
                vacant = (nextCell[0] + dr, nextCell[1] + dc) 

                # @vacant, this is to check if there is a vancant cell behind the crate
                # if there is a crate or a brick, then the crate can't be pushed or moved anymore and we skip it
                if vacant in bricks or vacant in crates: 
                    continue 

                # initialize "newCrates", the board has to describe the result  after pushing a specific crate
                newCrates = (crates - {nextCell}) | {vacant}

                nextMoves.append((move, nextCell, newCrates)) # Now, it saves all of the variables, like: the letter, the cat's new position, and the changes as to where the crates are.
            
            # else statement, if not a brick, crate, it is an empty cell or a target
            else: 
                nextMoves.append((move, nextCell, crates)) # Just save the walk with nothing changing

        return nextMoves # After 4 directions are done, returns and send back the entire list

    # @goalAchieved simply checks if all crates are sitting on their respective targets, and the goal is achieved.
    # Requirements: frozenset crates, targets; Function checks if all crates are in their respective targets; if so, goal is achieved.
    @staticmethod
    def goalAchieved(crates, targets):

        # @issubset() function does is check if all of the crate's positions are one of the targets. returns true or false
        return crates.issubset(targets) 
    

    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        Directions = self.Directions

        bricks, targets, cat, crates = self.attributesOfLevel(width, height, mapData, itemsData)

        if cat is None or self.goalAchieved(crates, targets): 
            return ""

        inside = lambda p: 0 <= p[0] < height and 0 <= p[1] < width

        dist = {t: 0 for t in targets}

        q = list(targets)
        i = 0
        while i < len(q):
            cell = q[i]
            i += 1
            for dr, dc in Directions.values():
                prev = (cell[0] - dr, cell[1] - dc)
                stand = (prev[0] - dr, prev[1] - dc)
                if(inside(prev) and inside(stand)) and prev not in bricks and stand not in bricks and prev not in dist:
                    dist[prev] = dist[cell] + 1
                    q.append(prev)

        def heuristic(cs):
            return sum(dist[c] for c in cs)

        def expand(start, cs):
            parent = {start: None}
            pushes = []
            beg = [start]
            j = 0
            while j < len(beg):
                pu = beg[j]
                j += 1
                for move, nxt, newCrates, in self.nextLegalMoves(pu, cs, bricks, width, height):
                    if newCrates == cs:
                        if nxt not in parent:
                            parent[nxt] = (pu, move)
                            beg.append(nxt)
                    else:
                        pushes.append((pu, move, nxt, newCrates))         
            return parent, pushes

        def movePath(parent, target):
            out = []
            while parent[target] is not None:
                target, mov = parent[target]
                out.append(mov)
            return ''.join(reversed(out))

        nodes = [(None, "")]
        closed = set()
        listOfEntries = {}
        listOfEntries.setdefault(heuristic(crates), []).append((0,0, cat, crates))
        f_min = heuristic(crates)
        pending = True

        while pending:
            # make sure solution is executed before deadline
            start_time = time.time()
            deadline = start_time + 13.0 

            if time.time() >= deadline:
                return ""
            
            while f_min not in listOfEntries or not listOfEntries[f_min]:
                listOfEntries.pop(f_min, None)
                f_min += 1

            
            go, nodeid, pl, cs = listOfEntries[f_min].pop(0)
            pending -= 1

            parent, pushes = expand(pl, cs)
            key = (cs, min(parent))
            if key in closed:
                continue
            closed.add(key)

            if self.goalAchieved(cs, targets):
                out = []
                while nodes[nodeid][0] is not None:
                    nodeid = nodes[nodeid][0]
                    out.append(nodes[nodeid][1])
                return ''.join(reversed(out))

            for stand, move, newCat, newCrates in pushes:
                dr, dc, = Directions[move]
                dest = (newCat[0] + dr, newCat[1] + dc)
                if dest not in dist:
                    continue
                nodes.append((nodeid, movePath(parent, stand) + move))
                nf = go + 1 + heuristic(newCrates)
                listOfEntries.setdefault(nf, []).append((nf, len(nodes) - 1, newCat, newCrates))
                pending += 1
                if nf < f_min:
                    f_min = nf
        return ""