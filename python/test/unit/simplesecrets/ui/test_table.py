from unittest import TestCase
from simplesecrets.ui.table import Table
from simplesecrets.ui.table import Colour

class TestTable(TestCase):

    def test_colour_table(self):
        table = Table()
        text = table.colour_table([['r1c1', 'r1c2'], ['r2c1', 'r2c2']])
        print (text)


    def test_getcontent_row(self):
        table = Table()
        text = table.getcontent_row(['asd', 'dfg'], [Colour.RED, Colour.BLACK], [3, 3])
        self.assertEqual('┃'+Colour.RED.value+'asd'+Colour.RESET.value+'┃'+Colour.BLACK.value+'dfg'+Colour.RESET.value+'┃\n', text)
        text = table.getcontent_row(['asd', 'dfg'], [Colour.RED, Colour.BLACK], [5, 3])
        self.assertEqual('┃'+Colour.RED.value+'asd  '+Colour.RESET.value+'┃'+Colour.BLACK.value+'dfg'+Colour.RESET.value+'┃\n', text)



