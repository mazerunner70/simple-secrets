from enum import Enum
from typing import Dict, Any


class Colour(Enum):
    BLACK =          "\u001b[30m"
    RED =            '\u001b[31m'
    GREEN =          '\u001b[32m'
    YELLOW =         '\u001b[33m'
    BLUE =           '\u001b[34m'
    MAGENTA =        '\u001b[35m'
    CYAN =           '\u001b[36m'
    WHITE =          '\u001b[37m'
    BRIGHT_BLACK =   "\u001b[30m"
    BRIGHT_RED =     '\u001b[31m'
    BRIGHT_GREEN =   '\u001b[32m'
    BRIGHT_YELLOW =  '\u001b[33m'
    BRIGHT_BLUE =    '\u001b[34m'
    BRIGHT_MAGENTA = '\u001b[35m'
    BRIGHT_CYAN =    '\u001b[36m'
    BRIGHT_WHITE =   '\u001b[37m'
    RESET =          '\u001b[0m'



class Table:
    def colour_table(self, tcontents, column_headings=None, row_headings=None, content_colours=None,
                     column_headings_colour=None, row_headings_colour=None):
        displaylist = self.create_display_grid(tcontents, column_headings, row_headings)
        widths = self.get_column_widths(displaylist)
        colourmap = self.create_colourmap(tcontents, column_headings, row_headings, content_colours,
                                          column_headings_colour, row_headings_colour)
        return self.getcontent_rows(displaylist, colourmap, widths, column_headings is not None)

    def get_column_widths(self, grid):
        # transpose and get max width of each row
        return [max(map(len, list(row))) for row in zip(*grid)]


    def create_display_grid(self, src_list, column_headings, row_headings):
        displaylist = src_list.copy()
        if column_headings:
            displaylist.insert(0, column_headings)
        if row_headings:
            topleft_cell = (column_headings and ['']) or []
            row_headings = topleft_cell+row_headings
            displaylist = [[row_heading] + row for (row_heading, row) in zip (row_headings, displaylist)]
        return displaylist

    def create_colourmap(self, src_list, column_headings, row_headings, content_colours = None, column_headings_colour = None, row_headings_colour = None):
        display_colours = content_colours
        if display_colours is None:
            display_colours = [[Colour.RESET]*len(row) for row in src_list]
        row_headings_colour = row_headings_colour or Colour.RESET
        if row_headings:
            display_colours = [[row_headings_colour] + row for row in display_colours]
        column_headings_colour = column_headings_colour or Colour.RESET
        if column_headings:
            display_colours.insert(0, [column_headings_colour]*(len(column_headings)+(1 if row_headings else 0)))
        return display_colours

    def get_border_toprow(self, widths):
        return "\u250F" + "\u2533".join(["\u2501" * width for width in widths] ) +"\u2513\n"

    def getcontent_rows(self, grid, colourmap, widths, columnheadings_present):
        contents = self.get_border_toprow(widths)
        index = 0
        if columnheadings_present: #fixme
            contents += self.getcontent_row(grid[0], colourmap[0], widths)
            contents += self.getheading_divider(widths)
            index += 1
        for i in range(index, len(grid)):
            contents += self.getcontent_row(grid[i], colourmap[i], widths)
        contents += self.get_border_bottomrow(widths)
        return contents

    def getcontent_row(self, row, colours, widths):
        return "\u2503" +"\u2503".join \
            ([colour.value +cell + " "*(width-len(cell))+Colour.RESET.value for (cell, colour, width) in zip(row, colours, widths)] ) +"\u2503\n"

    def getheading_divider(self, widths):
        return "\u2523" +"\u254B".join(["\u2501" *cell_width for cell_width in widths] ) +"\u252B\n"

    def get_border_bottomrow(self, widths):
        return "\u2517" + "\u253B".join(["\u2501" * width for width in widths] ) +"\u251B\n"





