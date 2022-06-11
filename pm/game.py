import pygame
from .constants import BACKGROUND, BLACK, BG_X, BG_Y, FACTOR, WHITE, PACMAN_LIFE, RED
from .balls import SmallBall, BigBall
from .pacman import Pacman
from .intersection import Intersection
from .ghosts import Blinky, Inky, Pinky, Clyde, GhostCaption
from math import sqrt
from .fruit import Fruit, FruitCaption
from queue import PriorityQueue

class Game():
    BALLS_THRESHOLD = 70 # number of small balls needed to collect due to fruit to pop up
    
    def __init__(self, win):
        self.win = win
        self.high_score = 0
        self.restart()

    def restart(self, next_level=False):
        self.pacman = None
        self.intersections = []
        self.small_balls = []
        self.big_balls = []
        self.ghosts = []
        self.frames = 0
        self.fruit = None
        self.fruit_caption = None
        self.ghost_caption = None
        self.eaten_balls = 0
        self.ghost_score = 200 # basic of bonus points for eating the blue ghost
        if not next_level:
            self.gameover = False
            self.pause = False
            self.level = 1
            self.score = 0
            self.lives = 3
        self.home_center = None # needed for path finding algorithm
        self.above_home = None # needed for path finding algorithm
        self.create_sprites(self.level)

    def render(self):
        # the background
        self.win.fill(BLACK)
        self.win.blit(BACKGROUND, (BG_X, BG_Y))
        
        # small balls
        for obj in self.small_balls:
            obj.draw(self.win)

        # big balls
        for obj in self.big_balls:
            if obj.IMG:
                obj.draw(self.win)

        # the Pacman
        if self.pacman:
            self.pacman.draw(self.win)

        # the fruit
        if self.fruit:
            self.fruit.draw(self.win)

        # ghosts
        for obj in self.ghosts:
            obj.draw(self.win)

        # the fruit caption
        if self.fruit_caption:
            self.fruit_caption.draw(self.win)
        
        # the ghost caption
        if self.ghost_caption:
            self.ghost_caption.draw(self.win)

        # an upper bar
        font = pygame.font.SysFont('comicsans', 20)
        caption = font.render(f'LVL: {self.level}\
                    SCORE: {self.score}\
                    HIGH SCORE: {self.high_score}', 1, WHITE)
        self.win.blit(caption, (int(BG_X + 10), int(BG_Y - caption.get_height() / 2 - 13)))

        # a bottom bar
        font = pygame.font.SysFont('comicsans', 15)
        caption = font.render('LIVES: ', 1, WHITE)
        self.win.blit(caption, (int(BG_X + 10), int(BG_Y + BACKGROUND.get_height() + caption.get_height() / 2 - 11)))
        DX = PACMAN_LIFE.get_width() + 5
        x = caption.get_width() + 15
        temp = self.lives - 1
        while temp > 0:
            self.win.blit(PACMAN_LIFE, (int(BG_X + x), int(BG_Y + BACKGROUND.get_height() + PACMAN_LIFE.get_height() / 2)))
            x += DX
            temp -= 1

        # a game over caption
        if self.gameover:
            font = pygame.font.SysFont('comicsans', 35)
            caption = font.render('GAME OVER', 1, RED)
            self.win.blit(caption, (int(BG_X + BACKGROUND.get_width() / 2 - caption.get_width() / 2), int(BG_Y + 140 * FACTOR - caption.get_height() / 2)))
            font = pygame.font.SysFont('comicsans', 25)
            caption = font.render('(PRESS ENTER TO RESTART)', 1, RED)
            self.win.blit(caption, (int(BG_X + BACKGROUND.get_width() / 2 - caption.get_width() / 2), int(BG_Y + 160 * FACTOR - caption.get_height() / 2)))

        # a pause caption
        if self.pause:
            font = pygame.font.SysFont('comicsans', 35)
            caption = font.render('PAUSED', 1, RED)
            self.win.blit(caption, (int(BG_X + BACKGROUND.get_width() / 2 - caption.get_width() / 2), int(BG_Y + 140 * FACTOR - caption.get_height() / 2)))
            font = pygame.font.SysFont('comicsans', 25)
            caption = font.render('(PRESS ENTER TO UNPAUSE)', 1, RED)
            self.win.blit(caption, (int(BG_X + BACKGROUND.get_width() / 2 - caption.get_width() / 2), int(BG_Y + 160 * FACTOR - caption.get_height() / 2)))

        pygame.display.update()

    def update(self):
        # frame number update
        self.frames += 1

        # high score update
        if self.score > self.high_score:
            self.high_score = self.score

        # next level condition
        if not self.small_balls and not self.big_balls:
            self.level += 1
            self.restart(next_level=True)

        # the popping up of a fruit
        if not self.fruit:
            if self.eaten_balls >= self.BALLS_THRESHOLD:
                self.fruit = Fruit(112, 140, self.level)

        # the disappearance of a fruit
        if self.fruit:
            self.fruit.frames += 1
            if self.fruit.frames >= self.fruit.HIDE_THRESHOLD:
                self.fruit = None
                self.eaten_balls = 0

        # the disappearance of a fruit caption
        if self.fruit_caption:
            self.fruit_caption.frames += 1
            if self.fruit_caption.frames >= self.fruit_caption.HIDE_THRESHOLD:
                self.fruit_caption = None

        # the disappearance of a ghost caption
        if self.ghost_caption:
            self.ghost_caption.frames += 1
            if self.ghost_caption.frames >= self.ghost_caption.HIDE_THRESHOLD:
                self.ghost_caption = None

        if self.pacman:
            # the decaying animation of the pacman
            if self.pacman.decaying:
                if self.pacman.decay():
                    pass # do nothing - let static objects animate until it finishes
                else:
                    self.lives -= 1
                    self.pacman = None
                    # game over condition
                    if self.lives <= 0:
                        self.gameover = True
                    else:
                        self.frames = 0
                        self.fruit = None
                        self.fruit_caption = None
                        self.ghost_caption = None
                        self.eaten_balls = 0
                        self.ghost_score = 200
                        self.create_sprites(self.level, reset_static_objects=False) # reset only dynamic objects (the Pacman and ghosts)
            else:
                # collision between the pacman and intersections
                for i in self.intersections:
                    if self.collision_detection(self.pacman, i):
                        self.pacman.last_intersection = i # setting the last visited node by Pacman

                        # searching for the predicted node to visit by Pacman
                        dir = self.pacman.current_dir
                        if dir:
                            value = i.dirs[dir]
                        else:
                            break # the dir is equal to None and the predicted intersection is found previously so break the loop
                        
                        # consider the tunnel case firstly
                        if i.y == BG_Y + 116 * FACTOR and i.x == BG_X + 52 * FACTOR and dir == 'LEFT':
                            for neighbor_node in self.intersections:
                                if neighbor_node.x == BG_X + 172 * FACTOR and neighbor_node.y == BG_Y + 116 * FACTOR:
                                    self.pacman.predicted_intersection = neighbor_node
                                    break # break the loop because the searching is over (there is always only one predicted node)
                            break # if there is a collision just pass the rest of a loop and the part of code below (optimization issue)
                        elif i.y == BG_Y + 116 * FACTOR and i.x == BG_X + 172 * FACTOR and dir == 'RIGHT':
                            for neighbor_node in self.intersections:
                                if neighbor_node.x == BG_X + 52 * FACTOR and neighbor_node.y == BG_Y + 116 * FACTOR:
                                    self.pacman.predicted_intersection = neighbor_node
                                    break # break the loop because the searching is over (there is always only one predicted node)
                            break # if there is a collision just pass the rest of a loop and the part of code below (optimization issue)

                        # consider every classic case
                        for neighbor_node in self.intersections:                            
                            distance = 0
                            if i.x == neighbor_node.x:
                                if dir == 'UP':
                                    distance = (i.y - neighbor_node.y) / 8 / FACTOR
                                elif dir == 'DOWN':
                                    distance = -1 * (i.y - neighbor_node.y) / 8 / FACTOR
                            elif i.y == neighbor_node.y:
                                if dir == 'LEFT':
                                    distance = (i.x - neighbor_node.x) / 8 / FACTOR
                                elif dir == 'RIGHT':
                                    distance = -1 * (i.x - neighbor_node.x) / 8 / FACTOR
                            if distance == value:
                                self.pacman.predicted_intersection = neighbor_node
                                break # break the loop because the searching is over (there is always only one predicted node)
                        
                        break # if there is a collision just pass the rest of a loop and the part of code below (optimization issue)
                else: 
                    # available moves between two intersections (when there is no collision)
                    if self.pacman.current_dir == 'LEFT' and self.pacman.future_dir == 'RIGHT':
                        self.pacman.change_dir()
                    elif self.pacman.current_dir == 'RIGHT' and self.pacman.future_dir == 'LEFT':
                        self.pacman.change_dir()
                    elif self.pacman.current_dir == 'UP' and self.pacman.future_dir == 'DOWN':
                        self.pacman.change_dir()
                    elif self.pacman.current_dir == 'DOWN' and self.pacman.future_dir == 'UP':
                        self.pacman.change_dir()

                self.pacman.move() # move according to the current_dir
                self.pacman.change_image() # an animation

                # collision between the pacman and small balls
                for sb in self.small_balls:
                    if self.collision_detection(self.pacman, sb):
                        self.small_balls.remove(sb)
                        self.score += 10
                        self.eaten_balls += 1

                # collision between the pacman and big balls
                for bb in self.big_balls:
                    if self.collision_detection(self.pacman, bb):
                        self.big_balls.remove(bb)
                        self.score += 50
                        self.ghost_score = 200
                        for g in self.ghosts:
                            if g.state == 'NORMAL' or g.state == 'FULL_BLUE' or g.state == 'HALF_BLUE':
                                if g.state == 'NORMAL' and not g.stay_at_home:
                                    for i in self.intersections:
                                        if self.collision_detection(g, i):
                                            break
                                    else:
                                        g.change_dir_to_opposite() # change dir only when ghost is between intersections
                                
                                g.change_state('FULL_BLUE')

                # collision between the pacman and ghosts
                for g in self.ghosts:
                    if self.collision_detection(self.pacman, g):
                        if g.state == 'NORMAL':
                            self.ghosts = []
                            self.pacman.decaying = True
                            self.pacman.stop()
                        elif g.state == 'FULL_BLUE' or g.state == 'HALF_BLUE':
                            g.change_state('EYES')
                            self.score += self.ghost_score
                            self.ghost_caption = GhostCaption((g.x - BG_X) // FACTOR, \
                                (g.y - BG_Y) // FACTOR, self.ghost_score)
                            self.ghost_score *= 2
                        break

                # collision between the pacman and the fruit
                if self.fruit:
                    if self.collision_detection(self.pacman, self.fruit):
                        self.fruit_caption = FruitCaption(112, 140, self.level)
                        self.score += self.fruit_caption.VALUE
                        self.fruit = None
                        self.eaten_balls = 0

                # the tunnel for the Pacman
                if self.pacman.x + self.pacman.IMG.get_width() // 2 < BG_X:
                    self.pacman.x = BG_X + BACKGROUND.get_width() + self.pacman.IMG.get_width() // 2
                elif self.pacman.x - self.pacman.IMG.get_width() // 2 > BG_X + BACKGROUND.get_width():
                    self.pacman.x = BG_X - self.pacman.IMG.get_width() // 2

        # an animation of a static object - a big ball
        for bb in self.big_balls:
            bb.change_image()

        for g in self.ghosts:
            # the tunnel for the ghosts (it has to be before collision detection with intersections due to STEP changing)
            if g.x + g.IMG.get_width() // 2 < BG_X:
                g.x = BG_X + BACKGROUND.get_width() + g.IMG.get_width() // 2
            elif g.x - g.IMG.get_width() // 2 > BG_X + BACKGROUND.get_width():
                g.x = BG_X - g.IMG.get_width() // 2
            if g.state != 'EYES': # do not change the ghost's step if the ghost's state is EYES (keep STEP_FASTER value)
                if g.y == BG_Y + 116 * FACTOR and (g.x < BG_X + 52 * FACTOR or g.x > BG_X + 172 * FACTOR):
                    g.STEP = g.STEP_SLOWER
                else:
                    g.STEP = g.STEP_NORMAL

            if g.stay_at_home:
                # stay at home collision and go out conditions
                if g.y - g.IMG.get_height() // 2 < BG_Y + 103 * FACTOR:
                    g.y = BG_Y + 103 * FACTOR + g.IMG.get_height() // 2
                    g.set_future_dir('DOWN')
                    g.change_dir()
                    if self.frames > g.GO_OUT_THRESHOLD:
                        g.stay_at_home = False
                elif g.y + g.IMG.get_height() // 2 > BG_Y + 128 * FACTOR:
                    g.y = BG_Y + 128 * FACTOR - g.IMG.get_height() // 2
                    g.set_future_dir('UP')
                    g.change_dir()
                    if self.frames > g.GO_OUT_THRESHOLD:
                        g.stay_at_home = False

            # the first stage of the recovery of a ghost (changing state from FULL BLUE to HALF BLUE)
            if g.state == 'FULL_BLUE':
                g.frames += 1
                if g.frames >= g.HALF_BLUE_THRESHOLD:
                    g.change_state('HALF_BLUE')

            # the second stage of the recovery of a ghost (changing state from HALF BLUE to NORMAL)
            if g.state == 'HALF_BLUE':
                g.frames += 1
                if g.frames >= g.NORMAL_THRESHOLD:
                    g.change_state('NORMAL')

            # set random mode for Inky ghost from the list of 3 possible modes
            if g.SUBTYPE == 'INKY':
                g.frames_to_change_mode += 1
                if g.frames_to_change_mode >= g.CHANGE_MODE_THRESHOLD:
                    g.change_mode()

            g.move() # move according to the current_dir (it has to be before collision detection with intersections due to STEP changing)
            g.change_image() # an animation

            # collision between ghosts and intersections
            for i in self.intersections:
                if self.collision_detection(g, i):
                    if g.eaten: # needed for call the A* algorithm only once
                        g.eaten = False
                        g.return_home_path = self.a_star_algorithm(start_node=i, end_node=self.above_home) # assign the path to the current ghost
                        self.collision_detection(g, i) # it is needed to start the path from the proper node (start node, not the node next to the start node)
                        break
                    if g.state == 'NORMAL':
                        if g.SUBTYPE == 'BLINKY' or g.SUBTYPE == 'CLYDE':
                            g.follow_pacman_path = self.a_star_algorithm(start_node=i, end_node=self.pacman.last_intersection)
                            self.collision_detection(g, i)
                            break
                        elif g.SUBTYPE == 'PINKY':
                            g.follow_pacman_path = self.a_star_algorithm(start_node=i, end_node=self.pacman.predicted_intersection)
                            self.collision_detection(g, i)
                            break
                        elif g.SUBTYPE == 'INKY':
                            if g.mode == 'being_like_blinky' or g.mode == 'being_like_clyde':
                                g.follow_pacman_path = self.a_star_algorithm(start_node=i, end_node=self.pacman.last_intersection)
                            elif g.mode == 'being_like_pinky':
                                g.follow_pacman_path = self.a_star_algorithm(start_node=i, end_node=self.pacman.predicted_intersection)
                            self.collision_detection(g, i)
                            break
                    elif g.state == 'FULL_BLUE' or g.state == 'HALF_BLUE':
                        g.follow_pacman_path = self.a_star_algorithm(start_node=i, end_node=self.pacman.last_intersection)
                        self.collision_detection(g, i)
                        break
                    break

    def collision_detection(self, obj1, obj2): # obj1 is a dynamic object, obj2 is considered as a static object even though it is a dynamic object
        if (obj1.TYPE == 'PACMAN' or obj1.TYPE == 'GHOST') and obj2.TYPE == 'INTERSECTION':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < FACTOR * obj1.STEP - 0.1: # the radius of a collision - it should be lesser than STEP * FACTOR but not lesser than a half of STEP * FACTOR of a dynamic object to work properly
                obj1.x = obj2.x # alignment to the center of obj2
                obj1.y = obj2.y # alignment to the center of obj2
                if obj1.TYPE == 'GHOST':
                    if obj1.stay_at_home:
                        return False
                    if obj1.state == 'NORMAL':
                        if obj1.SUBTYPE == 'BLINKY':
                            obj1.take_dir_to_follow_pacman(self.pacman.x, self.pacman.y)
                        elif obj1.SUBTYPE == 'PINKY':
                            obj1.take_dir_to_follow_pacman(self.pacman.x, self.pacman.y)
                        elif obj1.SUBTYPE == 'INKY':
                            if obj1.mode == 'being_like_blinky' or obj1.mode == 'being_like_pinky':
                                obj1.take_dir_to_follow_pacman(self.pacman.x, self.pacman.y)
                            elif obj1.mode == 'being_like_clyde':
                                # checking if Inky has to switch to fleeing mode (normally it follows the Pacman)
                                if sqrt((obj1.x - self.pacman.x)**2 + (obj1.y - self.pacman.y)**2) <= obj1.FLEEING_RANGE * FACTOR:
                                    possible_dirs = obj2.dirs.keys()
                                    if len(possible_dirs) > 1: # protection from staying in the infinite loop
                                        obj1.take_dir_to_flee_from_pacman(possible_dirs)
                                        return True
                                    else:
                                        obj1.generate_random_dir() # generate random dir while the ghost change dir to appropriate one
                                else:
                                    obj1.take_dir_to_follow_pacman(self.pacman.x, self.pacman.y)
                        elif obj1.SUBTYPE == 'CLYDE':
                            # checking if Clyde has to switch to fleeing mode (normally it follows the Pacman)
                            if sqrt((obj1.x - self.pacman.x)**2 + (obj1.y - self.pacman.y)**2) <= obj1.FLEEING_RANGE * FACTOR:
                                possible_dirs = obj2.dirs.keys()
                                if len(possible_dirs) > 1: # protection from staying in the infinite loop
                                    obj1.take_dir_to_flee_from_pacman(possible_dirs)
                                    return True
                                else:
                                    obj1.generate_random_dir() # generate random dir while the ghost change dir to appropriate one
                            else:
                                obj1.take_dir_to_follow_pacman(self.pacman.x, self.pacman.y)
                    elif obj1.state == 'FULL_BLUE' or obj1.state == 'HALF_BLUE':
                        possible_dirs = obj2.dirs.keys()
                        if len(possible_dirs) > 1: # protection from staying in the infinite loop
                            obj1.take_dir_to_flee_from_pacman(possible_dirs)
                            return True
                        else:
                            obj1.generate_random_dir() # generate random dir while the ghost change dir to appropriate one
                    elif obj1.state == 'EYES' and not obj1.eaten:
                        obj1.take_dir_to_go_home() # use the path from path finding algorithm to back home
                        # the last step to return home
                        if obj2 is self.above_home:
                            obj1.change_dir()
                            return True
                        # back to NORMAL state
                        if obj2 is self.home_center:
                            obj1.change_state('NORMAL')
                            obj1.set_future_dir('UP')
                        
                if obj1.future_dir in obj2.dirs:
                    # if there is a possibility to change dir then do it firstly
                    obj1.change_dir() # assign future_dir to current_dir
                elif obj1.current_dir in obj2.dirs:
                    pass # if there is a possibility to keep going then do not change anything
                else:
                    obj1.stop() # assign None value to current_dir if there is no possibility to move forward or wherever you wish
                return True
                
        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'SMALL_BALL':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG.get_width() // 2:
                return True

        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'BIG_BALL':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG_WIDTH // 2:
                return True

        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'GHOST':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG.get_width() // 2:
                return True
            
        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'FRUIT':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG.get_width() // 2:
                return True

        return False

    # heuristic part of A* algorithm
    # def h(self, n1, n2):
    #     result = abs(n1.x - n2.x) + abs(n1.y - n2.y)
    #     result /= FACTOR
    #     result /= 8
    #     return result

    # build a path from the end node to the start node using the dictionary came_from (stepping node by node)
    def create_path(self, came_from, current):
        path = []
        while current in came_from:
            current, dir = came_from[current]
            path.append(dir)
        return path # returns the path starting from the last dir !!! (reversed path - the ghost popping items from the end so for him is the first move)

    # A* path finding algorithm
    def a_star_algorithm(self, start_node, end_node):
        count = 0
        open_set = PriorityQueue() # it sorts items out in ascending order by the first element (if the first elements have the same value it sorts by the second element, so thats why var count is needed)
        came_from = {} # thanks to this dict we can reconstruct the shortest path that algorithm traverses through for us
        g_score = {node: float("inf") for node in self.intersections} # G score is an obligatory and basic component of this algorithm
        g_score[start_node] = 0
        f_score = {node: float("inf") for node in self.intersections} # F score = G score + H score
        f_score[start_node] = 0#self.h(start_node, end_node) # H score is not obligatory component but it helps with reaching faster the end node (less items in open set to sort)
        open_set.put((f_score[start_node], count, start_node))
        open_set_hash = {start_node} # there is no possisility to check if the priority queue has the specific item so we need to save this info in the set

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_node = open_set.get()[2] # always returns the node with the minimum F score
            open_set_hash.remove(current_node)

            # goal reaching
            if current_node is end_node:
                path = self.create_path(came_from, current_node)
                return path

            # create a temporary part of the graph
            neighbor_nodes = set()
            for node in self.intersections:
                for dir, value in current_node.dirs.items():
                    distance = 0
                    if current_node.x == node.x:
                        if dir == 'UP':
                            distance = (current_node.y - node.y) / 8 / FACTOR
                        elif dir == 'DOWN':
                            distance = -1 * (current_node.y - node.y) / 8 / FACTOR
                    elif current_node.y == node.y:
                        if dir == 'LEFT':
                            distance = (current_node.x - node.x) / 8 / FACTOR
                        elif dir == 'RIGHT':
                            distance = -1 * (current_node.x - node.x) / 8 / FACTOR
                    if distance == value:
                        neighbor_nodes.add((node, dir, value))

            for node, dir, value in neighbor_nodes:
                temp_g_score = g_score[current_node] + value # extend the neighbor node's G score by the edge's weight (distance) between current node and neighbor node

                if temp_g_score < g_score[node]: # thanks to that line, the algorithm does not go the same path back
                    # update the dictionaries
                    came_from[node] = (current_node, dir)
                    g_score[node] = temp_g_score
                    f_score[node] = temp_g_score #+ self.h(node, end_node)
                    if node not in open_set_hash:
                        count += 1
                        open_set.put((f_score[node], count, node)) # add to the open set all the new neighbor nodes which are not in there yet
                        open_set_hash.add(node)

    def create_sprites(self, lvl, reset_static_objects=True):
        # dynamic objects
        if lvl == 1:
            ghost_step = 1.0 # ghost step never should be greater or equal to the pacman's step which is always 2
            go_out_threshold = 270 # basic number of frames to go out (Blinky always has 0)
            half_blue_threshold = 300 # number of frames during ghost's recovery process
        elif lvl == 2:
            ghost_step = 1.2
            go_out_threshold = 240
            half_blue_threshold = 200
        elif lvl == 3:
            ghost_step = 1.4
            go_out_threshold = 210
            half_blue_threshold = 150
        elif lvl == 4:
            ghost_step = 1.6
            go_out_threshold = 180
            half_blue_threshold = 100
        elif lvl == 5:
            ghost_step = 1.7
            go_out_threshold = 150
            half_blue_threshold = 80
        elif lvl == 6:
            ghost_step = 1.8
            go_out_threshold = 120
            half_blue_threshold = 50
        elif lvl == 7:
            ghost_step = 1.9
            go_out_threshold = 100
            half_blue_threshold = 30
        else:
            ghost_step = 2.0
            go_out_threshold = 90
            half_blue_threshold = 0

        ghost_step = 2/3 * ghost_step # global scale
        go_out_threshold = 1 * go_out_threshold # global scale
        half_blue_threshold = 1 * half_blue_threshold # global scale
        self.pacman = Pacman(112, 188, 2)
        self.ghosts.append(Blinky(112, 92, ghost_step, 0, half_blue_threshold))
        self.ghosts.append(Inky(96, 116, ghost_step, 2 * go_out_threshold, half_blue_threshold))
        self.ghosts.append(Pinky(112, 116, ghost_step, go_out_threshold, half_blue_threshold))
        self.ghosts.append(Clyde(128, 116, ghost_step, 3 * go_out_threshold, half_blue_threshold))

        # static objects
        if reset_static_objects:
            # out of the coordinate system (home and other points)
            self.above_home = Intersection(112, 92, LEFT=1.5, RIGHT=1.5) # above home
            self.intersections.append(self.above_home)
            self.intersections.append(Intersection(96, 116, RIGHT=2)) # home's left side
            self.home_center = Intersection(112, 116, UP=3) # home's centre
            self.intersections.append(self.home_center)
            self.intersections.append(Intersection(128, 116, LEFT=2)) # home's right side

            # 2D coordinate system - height: 31 (rows), width: 28 (cols) with the external border
            for row in range(1, 30): # from 1 to 29
                for col in range(28): # from 0 to 27
                    if row == 1:
                        if col not in (0, 13, 14, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, RIGHT=5, DOWN=4))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=5, RIGHT=6, DOWN=4))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=6, DOWN=4))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, RIGHT=6, DOWN=4))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=6, RIGHT=5, DOWN=4))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=5, DOWN=4))
                    elif row == 2:
                        if col in (1, 6, 12, 15, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 3:
                        if col in (6, 12, 15, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        elif col in (1, 26):
                            self.big_balls.append(BigBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 4:
                        if col in (1, 6, 12, 15, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 5:
                        if col not in (0, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=4, RIGHT=5, DOWN=3))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=4, LEFT=5, RIGHT=3, DOWN=3))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, RIGHT=3, DOWN=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, UP=4, RIGHT=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, UP=4, RIGHT=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, RIGHT=3, DOWN=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=4, LEFT=3, RIGHT=5, DOWN=3))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=4, LEFT=5, DOWN=3))
                    elif row == 6:
                        if col in (1, 6, 9, 18, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 7:
                        if col in (1, 6, 9, 18, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 8:
                        if col not in (0, 7, 8, 13, 14, 19, 20, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=5))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=5, DOWN=6))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, DOWN=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, RIGHT=3, DOWN=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=5, DOWN=6))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=5))
                    elif row == 9:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 10:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 11:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, RIGHT=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, RIGHT=1.5))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=1.5, RIGHT=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, LEFT=3))
                    elif row == 12:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 13:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 14:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=6, LEFT=12, RIGHT=3, DOWN=6))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, DOWN=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=3, DOWN=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=6, LEFT=3, RIGHT=12, DOWN=6))
                    elif row == 15:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 16:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 17:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=9, DOWN=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=9, DOWN=3))
                    elif row == 18:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 19:
                        if col in (6, 21):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 20:
                        if col not in (0, 13, 14, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, RIGHT=5))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=6, LEFT=5, RIGHT=3, DOWN=3))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, RIGHT=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, DOWN=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, RIGHT=3, DOWN=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, RIGHT=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=6, RIGHT=5, LEFT=3, DOWN=3))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, LEFT=5))
                    elif row == 21:
                        if col in (1, 6, 12, 15, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 22:
                        if col in (1, 6, 12, 15, 21, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 23:
                        if col in (2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 24, 25):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        elif col in (1, 26):
                            self.big_balls.append(BigBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=2))
                        elif col == 3:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=2, DOWN=3))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=3, DOWN=3))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, LEFT=3, RIGHT=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, UP=3, RIGHT=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, UP=3, RIGHT=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, LEFT=3, RIGHT=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, DOWN=3))
                        elif col == 24:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, RIGHT=2))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=2))
                    elif row == 24:
                        if col in (3, 6, 9, 18, 21, 24):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 25:
                        if col in (3, 6, 9, 18, 21, 24):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 26:
                        if col not in (0, 7, 8, 13, 14, 19, 20, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, RIGHT=2))
                        elif col == 3:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=2, RIGHT=3))
                        elif col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=3))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, LEFT=3, DOWN=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, RIGHT=3))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=3))
                        elif col == 24:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, RIGHT=2))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, DOWN=3, LEFT=2))
                    elif row == 27:
                        if col in (1, 12, 15, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 28:
                        if col in (1, 12, 15, 26):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif row == 29:
                        if col not in (0, 27):
                            self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                        if col == 1: 
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, RIGHT=11))
                        elif col == 12:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=11, RIGHT=3))
                        elif col == 15:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=3, RIGHT=11))
                        elif col == 26:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, UP=3, LEFT=11))
