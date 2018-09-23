""" Utils for dealing with vim """

import vim


class BufferRange(object):
    """ BufferRange is an iterable object between a start point and end point
        in the current buffer
    """
    def __init__(self, start_line, end_line, start_col=None, end_col=None):

        # Information about the range
        self._range = vim.current.buffer.range(start_line, end_line)
        self._start_col = start_col
        self._end_col = end_col + 1

        # Iterator count and max number of elements
        self._current = 0
        self._max = end_line - start_line

    def reset(self):
        """ Reset the iterator so it can be used again """
        self._current = 0

    def __iter__(self):
        return self

    def next(self):
        """ Get the next line in the range

        Returns:
            str: next line segment
        """

        # Check to make sure we haven't passed the number of lines in the range
        if self._current > self._max:
            raise StopIteration

        # Get the line
        line = self._range[self._current]
        self._current += 1

        # Return the segment of the line between the start and end columns
        return line[self._start_col: self._end_col]
