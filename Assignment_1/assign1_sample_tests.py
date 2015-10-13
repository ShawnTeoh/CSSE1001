""" CSSE1001 Sem 2 2013, Assignment 1 Sample Test Cases

Save this in the same folder as the files assign1.py, maze1.txt,
maze2.txt, and maze3.txt. Then, run this program in IDLE. Each test will
output the line of code which is being tested, then the result of the
test ("ok", "FAIL", "ERROR" or "skipped" - the tests pass if all are "ok").

If you have difficulty understanding the output of this program, ask a
tutor in a practical session, or post the output (not your code!) in the
course newsgroup.

NOTE:
* This set of test cases is not comprehensive - even if you pass these
  tests, your program may still have errors.
* This program does not test the interact() function - you should run
  interact() yourself to check it is correct.

Tip: After running the tests, you can copy-paste lines of code from the
printed output into the Python Shell to see the output, and you can call
>>> run()  to re-run the tests.

This program uses many concepts that have not yet been taught. It is
not expected that you can read or understand this code; however some
students may wish to modify it (e.g. to add extra tests).

"""

import StringIO
import unittest
import sys

import assign1

MAZE1 = [['#', '#', '#', '#', '#'],
         ['#', ' ', ' ', ' ', '#'],
         ['#', '#', '#', ' ', '#'],
         ['#', 'X', ' ', ' ', '#'],
         ['#', '#', '#', '#', '#']]

MAZE2 = [['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
         ['#',' ',' ',' ','#',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ','#'],
         ['#','#','#',' ','#','#','#',' ','#',' ','#','#','#',' ','#','#','#'],
         ['#',' ','#',' ',' ',' ','#',' ','#',' ',' ',' ','#',' ',' ',' ','#'],
         ['#',' ','#','#','#',' ','#',' ','#','#','#',' ','#','#','#',' ','#'],
         ['#',' ',' ',' ','#',' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ','#'],
         ['#',' ','#','#','#',' ','#',' ','#','#','#','#','#','#','#',' ','#'],
         ['#',' ','#',' ',' ',' ','#',' ','#',' ','#',' ',' ',' ',' ',' ','#'],
         ['#',' ','#',' ','#','#','#',' ','#',' ','#',' ','#','#','#',' ','#'],
         ['#',' ','#',' ',' ',' ','#',' ',' ',' ','#',' ','#',' ',' ',' ','#'],
         ['#',' ','#','#','#',' ','#','#','#',' ','#',' ','#','#','#','#','#'],
         ['#',' ',' ',' ',' ',' ','#','X',' ',' ','#',' ',' ',' ',' ',' ','#'],
         ['#',' ','#','#','#','#','#','#','#','#','#','#','#','#','#',' ','#'],
         ['#',' ',' ',' ','#',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' ','#'],
         ['#','#','#',' ','#','#','#',' ','#',' ','#',' ','#',' ','#',' ','#'],
         ['#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' ',' ',' ','#'],
         ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]

def skip_if_undefined(func_name):
    if hasattr(assign1, func_name):
        return lambda f: f
    return unittest.skip(func_name + " is not defined")

@skip_if_undefined('load_maze')
class TestLoadMaze(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def test_maze1(self):
        """maze1 = load_maze('maze1.txt')"""
        maze = assign1.load_maze('maze1.txt')
        self.assertEqual(maze, MAZE1, "\n\nload_maze() returned incorrectly")

    def test_maze2(self):
        """maze2 = load_maze('maze2.txt')"""
        maze = assign1.load_maze('maze2.txt')
        self.assertEqual(maze, MAZE2, "\n\nload_maze() returned incorrectly")


@skip_if_undefined('get_position_in_direction')
class TestGetPositionInDirection(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def test_east(self):
        """get_position_in_direction((2, 3), 'e')"""
        result = assign1.get_position_in_direction((2, 3), 'e')
        self.assertEqual(result, (2, 4),
                         "\n\nget_position_in_direction() returned"
                         " incorrectly")

    def test_south(self):
        """get_position_in_direction((2, 3), 's')"""
        result = assign1.get_position_in_direction((2, 3), 's')
        self.assertEqual(result, (3, 3),
                         "\n\nget_position_in_direction() returned"
                         " incorrectly")


@skip_if_undefined('move')
class TestMove(unittest.TestCase):
    def setUp(self):
        self.maze1 = [list(row) for row in MAZE1]
        self.maze1_copy = [list(row) for row in self.maze1]
        self.maze2 = [list(row) for row in MAZE2]
        self.maze2_copy = [list(row) for row in self.maze2]

    def test_invalid(self):
        """move(maze1, (1, 1), 's')"""
        result = assign1.move(self.maze1, (1, 1), 's')
        self.assertEqual(result, ((1, 1), '#'), 'move() returned incorrectly')
        self.assertEqual(self.maze1, self.maze1_copy,
                         'move() modified the maze')

    def test_valid(self):
        """move(maze1, (1, 1), 'e')"""
        result = assign1.move(self.maze1, (1, 1), 'e')
        self.assertEqual(result, ((1, 2), ' '), 'move() returned incorrectly')
        self.assertEqual(self.maze1, self.maze1_copy,
                         'move() modified the maze')

    def test_finish(self):
        """move(maze1, (3, 2), 'w')"""
        result = assign1.move(self.maze1, (3, 2), 'w')
        self.assertEqual(result, ((3, 1), 'X'), 'move() returned incorrectly')
        self.assertEqual(self.maze1, self.maze1_copy,
                         'move() modified the maze')

    def test_finish_maze2(self):
        """move(maze2, (11, 8), 'w')"""
        result = assign1.move(self.maze2, (11, 8), 'w')
        self.assertEqual(result, ((11, 7), 'X'), 'move() returned incorrectly')
        self.assertEqual(self.maze2, self.maze2_copy,
                         'move() modified the maze')


@skip_if_undefined('print_maze')
class TestPrintMaze(unittest.TestCase):
    EXPECTED = """#####\n#O  #\n### #\n#X  #\n#####\n"""

    def setUp(self):
        self.maze1 = [list(row) for row in MAZE1]
        self.maze1_copy = [list(row) for row in self.maze1]
        self.real_stdout = sys.stdout
        self.fake_stdout = StringIO.StringIO()

    def test(self):
        """print_maze(maze1, (1, 1))"""
        sys.stdout = self.fake_stdout
        result = assign1.print_maze(self.maze1, (1, 1))
        sys.stdout = self.real_stdout
        output = self.fake_stdout.getvalue()
        self.assertEqual(output, self.EXPECTED)
        self.assertEqual(result, None, 'print_maze should not return')
        self.assertEqual(self.maze1, self.maze1_copy,
                         'print_maze() modified the maze')


@skip_if_undefined('get_possible_directions')
class TestGetPossibleDirections(unittest.TestCase):
    def setUp(self):
        self.longMessage = True
        self.maze1 = [list(row) for row in MAZE1]
        self.maze1_copy = [list(row) for row in self.maze1]
        self.maze2 = [list(row) for row in MAZE2]
        self.maze2_copy = [list(row) for row in self.maze2]

    def test1(self):
        """get_possible_directions(maze1, (1, 2))"""
        result = assign1.get_possible_directions(self.maze1, (1, 2))
        self.assertItemsEqual(result, ['e', 'w'])
        self.assertEqual(self.maze1, self.maze1_copy,
                         '\n\nget_possible_directions() modified the maze')

    def test2(self):
        """get_possible_directions(maze2, (5, 7))"""
        result = assign1.get_possible_directions(self.maze2, (5, 7))
        self.assertItemsEqual(result, ['n', 's', 'e'])
        self.assertEqual(self.maze2, self.maze2_copy,
                         '\n\nget_possible_directions() modified the maze')


class AssignmentTestResult(unittest.TextTestResult):
    def getDescription(self, test):
        return test.shortDescription() + "  #"

    def addSkip(self, test, reason):
        super(unittest.TextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln("skipped: {0}".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()


def suite():
    tests = (map(TestLoadMaze, ['test_maze1', 'test_maze2']) +
             map(TestGetPositionInDirection, ['test_east', 'test_south']) +
             map(TestMove, ['test_invalid', 'test_valid',
                            'test_finish', 'test_finish_maze2']) +
             map(TestPrintMaze, ['test']) +
             map(TestGetPossibleDirections, ['test1', 'test2']))

    return unittest.TestSuite(tests)

def run():
    reload(assign1)

    tests = suite()
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2,
                                     resultclass=AssignmentTestResult)
    result = runner.run(tests)
    if not result.wasSuccessful():
        print >> sys.stderr, "Failures/Errors found."
    if result.skipped:
        print >> sys.stderr, "Some functions are not defined."

    # put assign1.py variables into globals for easy use.
    for name in dir(assign1):
        if not name.startswith("__"):
            globals()[name] = getattr(assign1, name)

    global maze1, maze2
    maze1 = [list(row) for row in MAZE1]
    maze2 = [list(row) for row in MAZE2]

if __name__ == '__main__':
    run()
