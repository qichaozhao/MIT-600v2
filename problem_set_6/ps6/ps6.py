# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import ps6_visualize
import pylab
import numpy as np

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height

        # initialise all tiles to zero
        # list of lists
        self.tileStatus = [[0 for n in range(height)] for m in range(width)]

        # print len(self.tileStatus)
        # print len(self.tileStatus[0])

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        ## get the tiles this corresponds to
        # print pos
        m = int(pos.getX())
        n = int(pos.getY())
        # print m
        # print n
        self.tileStatus[m][n] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        # print m
        # print n
        return self.tileStatus[m][n] == 1

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numClean = 0
        for t in self.tileStatus:
            numClean = numClean + sum(t)

        return numClean

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x_random = random.uniform(0,self.width)
        y_random = random.uniform(0,self.height)
        pos = [x_random, y_random]
        position = Position(pos)
        # print x_random
        # print y_random
        return position

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()

        if x > self.width or x < 0 \
            or y > self.height or y < 0:

            return False

        else:

            return True


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed

        # use the getRandomPosition attribute in the room
        self.position = self.room.getRandomPosition()
        # print "got random pos"
        # print self.position
        # clean the tile
        r = self.room.cleanTileAtPosition(self.position)

        # set a random direction
        self.direction = random.randint(0,359)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        validPos = False
        while validPos == False:
            ## calculate new position
            newPos = Position([self.position.getX(), self.position.getY()])
            newPos = newPos.getNewPosition(self.direction, self.speed)

            if self.room.isPositionInRoom(newPos):
                validPos = True
                self.position = newPos

            else:
                self.direction = random.randint(0, 359)

        self.room.cleanTileAtPosition(self.position)

class Position(object):
    def __init__(self, pos):
        self.pos = pos

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
        Does NOT test whether the returned position fits inside the room.
        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed
        Returns: a Position object representing the new position.
        """
        newPos = [float(0), float(0)]

        newPos[0] = (self.pos[0] + (speed * math.sin(math.radians(angle))))
        newPos[1] = (self.pos[1] + (speed * math.cos(math.radians(angle))))
        self.pos = [newPos[0], newPos[1]]
        return self

    def getX(self):
        """
        Get the x value of the current position
        :return:
        """
        return self.pos[0]

    def getY(self):
        """
        get the y value of the current position
        :return:
        """
        return self.pos[1]

    def setPos(self, pos):
        self.pos = pos

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    trial_ticks = []
    # now let's run trials
    for i in range(0,num_trials):

        # let's instantiate the room
        room = RectangularRoom(width, height)

        # let's instantiate our robots
        robots = []
        for i in range(0, num_robots):
            robots.append(robot_type(room, speed))

        anim = ps6_visualize.RobotVisualization(num_robots, width, height)

        cleaned_coverage = 0.0
        ticks = 0 # track the number of ticks
        while cleaned_coverage < min_coverage:
            # update the position of each of the robots
            for r in robots:
                r.updatePositionAndClean()

            # calculate new cleaned pct
            cleaned_coverage = (room.getNumCleanedTiles() / float(room.getNumTiles()))
            # print cleaned_coverage

            #increment ticks and animation
            ticks = ticks + 1
            anim.update(room, robots)


        # finish off
        trial_ticks.append(ticks)
        anim.done()

    # print "Number of Robots: " + str(num_robots)
    # print "Robot Type: " + str(robot_type)
    # print "Robot Speed: " + str(speed)
    # print "Room Size: " + str(width) + 'x' + str(height)
    # print "Number of Trials: " + str(num_trials)
    # print "Mean clock ticks: " + str(float(sum(trial_ticks)) / num_trials)

    return sum(trial_ticks) / float(len(trial_ticks))
# === Problem 4
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    times = []
    robots = range(1,11)

    # num_robots = 10
    speed = 1.0
    width = 20
    height = 20
    min_coverage = 0.8
    num_trials = 100
    robot_type = StandardRobot

    for n in range(1,11):
        times.append(runSimulation(n, speed, width, height, min_coverage,num_trials,robot_type))

    pylab.plot(robots, times)
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Mean Time')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    times = []
    rooms = [[20,20],
             [25,16],
             [40,10],
             [50,8],
             [80,5],
             [100,4]]

    num_robots = 2
    speed = 1.0
    # width = 20
    # height = 20
    min_coverage = 0.8
    num_trials = 100
    robot_type = StandardRobot

    ratios = []
    for r in rooms:
        width = r[0]
        height = r[1]
        ratios.append(width / float(height))

        times.append(runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type))

    pylab.plot(ratios, times)
    pylab.xlabel('Ratio of Width to Height')
    pylab.ylabel('Mean Time')
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        validPos = False
        while validPos == False:
            ## calculate new position
            self.direction = random.randint(0,359)
            newPos = Position([self.position.getX(), self.position.getY()])
            newPos = newPos.getNewPosition(self.direction, self.speed)

            if self.room.isPositionInRoom(newPos):
                validPos = True
                self.position = newPos

        self.room.cleanTileAtPosition(self.position)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    # Comparison between RandomWalk vs Standard as coverage required changes for a large room (30x30)

    num_robots = 2
    speed = 1.0
    width = 10
    height = 10
    # min_coverage = 0.8
    num_trials = 50
    robot_type1 = StandardRobot
    robot_type2 = RandomWalkRobot

    times_std = []
    times_rdm_walk = []
    coverage_goal = np.arange(0,1.05,0.05)
    for r in coverage_goal:

        times_std.append(runSimulation(num_robots, speed, width, height, r, num_trials, robot_type1))
        times_rdm_walk.append(runSimulation(num_robots, speed, width, height, r, num_trials, robot_type2))

    pylab.plot(coverage_goal, times_std, label='Standard')
    pylab.plot(coverage_goal, times_rdm_walk, label='Random Walk')
    pylab.xlabel('Coverage Required')
    pylab.ylabel('Mean Time')
    pylab.legend()
    pylab.show()

if __name__ == '__main__':

    num_robots = 1
    speed = 1.0
    width = 10
    height = 10
    min_coverage = 1.0
    num_trials = 1
    robot_type = StandardRobot

    avg = runSimulation(num_robots, speed, width, height, min_coverage,num_trials,robot_type)
    # print "avg: " + str(avg)

    # showPlot1()
    # showPlot2()
    # showPlot3()