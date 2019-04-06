from unittest import TestCase
from simplesecrets.ui.table import Table
from simplesecrets.ui.table import Colour

class TestTable(TestCase):




    def test_getcontent_row(self):
        table = Table()
        text = table.getcontent_row(['asd', 'dfg'], [Colour.RED, Colour.BLACK], [3, 3])
        self.assertEqual('┃'+Colour.RED.value+'asd'+Colour.RESET.value+'┃'+Colour.BLACK.value+'dfg'+Colour.RESET.value+'┃\n', text)
        text = table.getcontent_row(['asd', 'dfg'], [Colour.RED, Colour.BLACK], [5, 3])
        self.assertEqual('┃'+Colour.RED.value+'asd  '+Colour.RESET.value+'┃'+Colour.BLACK.value+'dfg'+Colour.RESET.value+'┃\n', text)

    def test_create_display_grid(self):
        table = Table()
        grid = table.create_display_grid([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], None, ['row 1', 'row 2'])
        self.assertListEqual([['row 1', 'r1c1', 'r1c2'],['row 2', 'r2c1', 'r2c2']], grid)

    def test_get_column_widths(self):
        table = Table()
        widths = table.get_column_widths([['r1c1', 'r1c2-xtra'], ['r2c1', 'r2c2']])
        self.assertListEqual([4, 9], widths)
        widths = table.get_column_widths([['r1c1', 'r1c2-xtra'], ['r2c1-ct', 'r2c2']])
        self.assertListEqual([7, 9], widths)

    def test_colour_table(self):
        table = Table()
        # basic table
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']])
        self.assertEqual('┏━━━━┳━━━━┓\n' +
                         '┃'+Colour.RESET.value+'r1c1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c2'+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'r2c1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c2'+Colour.RESET.value+'┃\n' +
                         '┗━━━━┻━━━━┛\n', text)
        # with rows named
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], None, ['row 1', 'row 2'])
        self.assertEqual('┏━━━━━┳━━━━┳━━━━┓\n' +
                         '┃'+Colour.RESET.value+'row 1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c2'+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'row 2'+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c2'+Colour.RESET.value+'┃\n' +
                         '┗━━━━━┻━━━━┻━━━━┛\n', text)
        # with columns named
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], ['column 1', 'column 2'])
        self.assertEqual('┏━━━━━━━━┳━━━━━━━━┓\n' +
                         '┃'+Colour.RESET.value+'column 1'+Colour.RESET.value+'┃'+Colour.RESET.value+'column 2'+Colour.RESET.value+'┃\n' +
                         '┣━━━━━━━━╋━━━━━━━━┫\n' +
                         '┃'+Colour.RESET.value+'r1c1    '+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c2    '+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'r2c1    '+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c2    '+Colour.RESET.value+'┃\n' +
                         '┗━━━━━━━━┻━━━━━━━━┛\n', text)
        # with columns and rows named
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], ['column 1', 'column 2'], ['row 1', 'row 2'])
        self.assertEqual('┏━━━━━┳━━━━━━━━┳━━━━━━━━┓\n' +
                         '┃'+Colour.RESET.value+'     '+Colour.RESET.value+'┃'+Colour.RESET.value+'column 1'+Colour.RESET.value+'┃'+Colour.RESET.value+'column 2'+Colour.RESET.value+'┃\n' +
                         '┣━━━━━╋━━━━━━━━╋━━━━━━━━┫\n' +
                         '┃'+Colour.RESET.value+'row 1'+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c1    '+Colour.RESET.value+'┃'+Colour.RESET.value+'r1c2    '+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'row 2'+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c1    '+Colour.RESET.value+'┃'+Colour.RESET.value+'r2c2    '+Colour.RESET.value+'┃\n' +
                         '┗━━━━━┻━━━━━━━━┻━━━━━━━━┛\n', text)
        # with columns and rows named, content coloured
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], ['column 1', 'column 2'], ['row 1', 'row 2'],
                                  [[Colour.BLUE]*2, [Colour.YELLOW]*2])
        self.assertEqual('┏━━━━━┳━━━━━━━━┳━━━━━━━━┓\n' +
                         '┃'+Colour.RESET.value+'     '+Colour.RESET.value+'┃'+Colour.RESET.value+'column 1'+Colour.RESET.value+'┃'+Colour.RESET.value+'column 2'+Colour.RESET.value+'┃\n' +
                         '┣━━━━━╋━━━━━━━━╋━━━━━━━━┫\n' +
                         '┃'+Colour.RESET.value+'row 1'+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c1    '+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c2    '+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'row 2'+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c1    '+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c2    '+Colour.RESET.value+'┃\n' +
                         '┗━━━━━┻━━━━━━━━┻━━━━━━━━┛\n', text)
        # with columns and rows named, content coloured, column names coloured
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], ['column 1', 'column 2'], ['row 1', 'row 2'],
                                  [[Colour.BLUE]*2, [Colour.YELLOW]*2], Colour.BRIGHT_GREEN)
        self.assertEqual('┏━━━━━┳━━━━━━━━┳━━━━━━━━┓\n' +
                         '┃'+Colour.BRIGHT_GREEN.value+'     '+Colour.RESET.value+'┃'+Colour.BRIGHT_GREEN.value+'column 1'+Colour.RESET.value+'┃'+Colour.BRIGHT_GREEN.value+'column 2'+Colour.RESET.value+'┃\n' +
                         '┣━━━━━╋━━━━━━━━╋━━━━━━━━┫\n' +
                         '┃'+Colour.RESET.value+'row 1'+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c1    '+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c2    '+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.RESET.value+'row 2'+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c1    '+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c2    '+Colour.RESET.value+'┃\n' +
                         '┗━━━━━┻━━━━━━━━┻━━━━━━━━┛\n', text)
        # with columns and rows named, content coloured, column names and row names coloured
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']], ['column 1', 'column 2'], ['row 1', 'row 2'],
                                  [[Colour.BLUE]*2, [Colour.YELLOW]*2], Colour.BRIGHT_GREEN, Colour.BRIGHT_WHITE)
        self.assertEqual('┏━━━━━┳━━━━━━━━┳━━━━━━━━┓\n' +
                         '┃'+Colour.BRIGHT_GREEN.value+'     '+Colour.RESET.value+'┃'+Colour.BRIGHT_GREEN.value+'column 1'+Colour.RESET.value+'┃'+Colour.BRIGHT_GREEN.value+'column 2'+Colour.RESET.value+'┃\n' +
                         '┣━━━━━╋━━━━━━━━╋━━━━━━━━┫\n' +
                         '┃'+Colour.BRIGHT_WHITE.value+'row 1'+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c1    '+Colour.RESET.value+'┃'+Colour.BLUE.value+'r1c2    '+Colour.RESET.value+'┃\n' +
                         '┃'+Colour.BRIGHT_WHITE.value+'row 2'+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c1    '+Colour.RESET.value+'┃'+Colour.YELLOW.value+'r2c2    '+Colour.RESET.value+'┃\n' +
                         '┗━━━━━┻━━━━━━━━┻━━━━━━━━┛\n', text)

