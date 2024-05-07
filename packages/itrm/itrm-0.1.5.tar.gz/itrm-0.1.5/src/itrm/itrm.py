"""
Copyright 2024 David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "David Woodburn"
__license__ = "MIT"
__date__ = "2024-04-24"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import os
import sys
import signal
import termios
import time
import math
import numpy as np


# Constants
NORMAL_COLORS = [39, 40, 220, 202, 201] # blue, green, yellow, orange, magenta
BRIGHT_COLORS = [87, 82, 228, 216, 213] # blue, green, yellow, orange, magenta
COLOR_CNT = 5 # number of colors in the color map


class config: # configuration settings
    uni = True # flag to use Unicode characters
    cols = 60 # default column width
    rows = 20 # default row height
    ar = 2.1 # aspect ratio of characters


class persistent: # persistent, run-time values
    t_last = None # last time value
    orig_term_attr = None # original terminal attributes


class limits: # x and y data limits
    def __init__(self, x_min=None, x_max=None, y_min=None, y_max=None):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


class term_ws: # terminal window size and sub-character resolution
    def __init__(self, rows, cols, subrows=None, subcols=None):
        self.rows = rows
        self.cols = cols
        self.subrows = subrows
        self.subcols = subcols

# ------------------
# Plotting functions
# ------------------

def plot(x, y=None, label=None, rows=1, cols=1, equal=0):
    """
    Create a text-based plot of the path defined by (`x`, `y`) using characters.
    If the size of the terminal can be found, that will be used for sizing the
    plot. Otherwise, the default dimensions (config.cols, config.rows) will be
    used. Note that this function does not plot connecting lines, only the
    points specified by the (`x`, `y`) pairs.

    Parameters
    ----------
    x : (K,) or (J, K) np.ndarray
        Array of x-axis values or matrix of rows of x-axis values.
    y : (K,) or (J, K) np.ndarray, default None
        Array of y-axis values or matrix of rows of y-axis values. If `y` is not
        provided, `x` will be used as the `y` array and `x` will be defined to
        be an array of indices (starting at zero).
    label : str, default ''
        Text to place at top of the plot, centered in the border.
    rows : int, default 1
        Desired number of rows if greater than 1 or fraction of existing rows if
        less than 1.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of window
        columns if less than 1.
    equal : float, default 0
        Axis scaling, `y` to `x`. A value of 0 leaves the scaling alone. A value
        of 1 would approximate equal axis scaling. However, because the aspect
        ratio of characters in the terminal is not exactly 2 to 1, this value
        can be adjusted to compensate.

    Notes
    -----
    Non-finite values will be ignored.
    """

    # Check and (possibly) adjust the shapes of x and y.
    x, y = shape_xy(x, y)

    # Choose the canvas size.
    tws = screen_size(rows, cols)

    # Get the data limits, adjusting for the terminal window size.
    lims, row_zero = limits_xy(x, y, tws, equal)

    # Map x and y to the expanded canvas, M, and the foreground color matrix, F.
    M, F = data_to_matrix(x, y, lims, tws)

    # Convert the expanded matrix, M, to a matrix of character values, C.
    C = matrix_to_braille(M) if config.uni else matrix_to_ascii(M)

    # Get the ranges text.
    ranges = f"({ftostr(lims.x_min)}:{ftostr(lims.x_max)}, " \
            + f"{ftostr(lims.y_min)}:{ftostr(lims.y_max)})"

    # Draw the plot.
    draw_graph(C, ranges, label, F, row_zero)


def iplot(x, y=None, label=None, rows=1, cols=1):
    """
    Create an interactive, text-based plot of the path defined by (`x`, `y`)
    using characters. If the size of the terminal can be found, that will be
    used for sizing the plot. Otherwise, the default dimensions (config.cols,
    config.rows) will be used. Note that this function does not plot connecting
    lines, only the points specified by the (`x`, `y`) pairs. Once the function
    has been called, the terminal will be in interactive mode. The user can then
    control the cursor position and x-axis zoom with keyboard shortcuts.

    Parameters
    ----------
    x : (K,) or (J, K) np.ndarray
        Array of x-axis values or matrix of rows of x-axis values.
    y : (K,) or (J, K) np.ndarray, default None
        Array of y-axis values or matrix of rows of y-axis values. If `y` is not
        provided, `x` will be used as the `y` array and `x` will be defined to
        be an array of indices (starting at zero).
    label : str, default ''
        Text to place at top of the plot, centered in the border.
    rows : int, default 1
        Desired number of rows if greater than 1 or fraction of existing rows if
        less than 1.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of window
        columns if less than 1.

    Shortcuts
    ---------
    q, x, ⌫  : exit interactive plot
    h, a, ←  : move cursor left
    l, d, →  : move cursor right
    H, A, ⇧← : move cursor left fast
    L, D, ⇧→ : move cursor right fast
    g        : move cursor to start
    G        : move cursor to end
    j, s, ↓  : zoom in
    k, w, ↑  : zoom out
    J, S, ⇧↓ : zoom in fast
    K, W, ⇧↑ : zoom out fast
    n        : next data row
    p        : previous data row
    c, z     : center view on cursor

    Notes
    -----
    Non-finite values will be ignored.
    """

    # Check if this is a tty.
    if not istty():
        print("The iplot function will not work in this terminal.")
        return

    # Set signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Set raw mode
    try:
        persistent.orig_term_attr = termios.tcgetattr(0)
        tty_mode = persistent.orig_term_attr.copy()
        tty_mode[3] &= ~termios.ICANON & ~termios.ECHO
        tty_mode[3] |= termios.ISIG  # Enable ISIG flag (Ctrl-c to exit)
        termios.tcsetattr(0, termios.TCSANOW, tty_mode)
    except termios.error:
        print("The iplot function will not work in this terminal.")
        return

    # Hide the cursor.
    sys.stdout.write("\033[?25l")

    # Check and (possibly) adjust the shapes of x and y.
    x, y = shape_xy(x, y)
    J, K = x.shape

    # Get the canvas size.
    tws = screen_size(rows, cols)

    # Get the data limits, adjusting for the terminal window size.
    lims, _ = limits_xy(x, y, tws, 0) # ignore row_zero

    # --------------------
    # Draw a blank canvas.
    # --------------------

    # Create a blank expanded canvas.
    Rows = tws.subrows*tws.rows
    Cols = tws.subcols*tws.cols
    M = np.zeros((Rows, Cols), dtype=int)

    # Convert the expanded canvas, M, to a matrix of character values, C.
    C = matrix_to_braille(M) if config.uni else matrix_to_ascii(M)

    # Draw the canvas.
    draw_graph(C)

    # ----------------------------------
    # Fill in the details on the canvas.
    # ----------------------------------

    # Define the current view rectangle.
    view = limits(lims.x_min, lims.x_max, lims.y_min, lims.y_max)

    # Define the cursor.
    cstate = -1 # cursor state ("-1" means all data rows)
    xc = (view.x_max + view.x_min)/2 # cursor at mid-point
    xc = move_cursor(xc, 0, x) # align xc with closest x values
    ccol = get_column(xc, view, tws) # cursor column index
    yc_min, yc_max = get_cursor_y(ccol, tws, x, y, view) # y range at cursor
    if yc_min == yc_max:
        cstr = f"({ftostr(xc)}, {ftostr(yc_max)})" # cursor readout
    else:
        cstr = f"({ftostr(xc)}, {ftostr(yc_min)}:{ftostr(yc_max)})"
    cF = "\x1b[0m" # cursor foreground color
    dx = (view.x_max - view.x_min)/tws.cols # cursor jump size

    # Map x and y to the expanded canvas, M, and the color matrix, F.
    M, F = data_to_matrix(x, y, view, tws)

    # Convert the expanded canvas, M, to a matrix of character values, C.
    C = matrix_to_braille(M) if config.uni else matrix_to_ascii(M)

    # Set the deltas based on what is not a white-space character.
    s = 0x2800 if config.uni else 0x20 # white-space character
    D = (C != s) # wherever C is not a white space
    D[:, ccol] = True # wherever the cursor is

    # Get the ranges text.
    ranges = f"({ftostr(lims.x_min)}:{ftostr(lims.x_max)}, " \
            + f"{ftostr(lims.y_min)}:{ftostr(lims.y_max)})"

    # Draw the data to the canvas.
    redraw_graph(C, D, ranges, label, F, ccol, cstr, cF, view, lims)

    # --------------------------------
    # Cycle through the state machine.
    # --------------------------------

    jump_sf = 0.0 # cursor jump scale factor
    zoom_sf = 1.0 # scale factor
    recursor = False
    remap = False

    while True:
        # Read a character. Wait for input.
        char = sys.stdin.read(1)

        # Exit on 'q', 'x', delete, new line, or carriage return.
        if (char == 'q') or (char == 'x') or \
                (char == '\x7f') or (char == '\n') or (char == '\r'):
            break
        #else:
        #    print(char)
        #    continue

        # Interpret the shortcut keys pressed.
        if char == '\x1b': # escape
            char = sys.stdin.read(1)
            if char == '[': # CSI
                char = sys.stdin.read(1)
                if char == 'A': # slow zoom out
                    zoom_sf = 1.4142135623730950488
                elif char == 'B': # slow zoom in
                    zoom_sf = 0.70710678118654752440
                elif char == 'C': # slow right
                    jump_sf = 1.0
                    recursor = True
                elif char == 'D': # slow left
                    jump_sf = -1.0
                    recursor = True
                elif char == '1': # possible shift arrow
                    chars = sys.stdin.read(3)
                    if chars == ';2A': # fast zoom out
                        zoom_sf = 4.0
                    elif chars == ';2B': # fast zoom in
                        zoom_sf = 0.25
                    elif chars == ';2C': # fast right
                        jump_sf = 10.0
                        recursor = True
                    elif chars == ';2D': # fast left
                        jump_sf = -10.0
                        recursor = True
                    else: # unrecognized escape sequence
                        termios.tcflush(sys.stdin, termios.TCIFLUSH)
                        continue
                else: # unrecognized escape sequence
                    termios.tcflush(sys.stdin, termios.TCIFLUSH)
                    continue
            else: # unrecognized escape sequence
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
                continue
        elif (char == 'l') or (char == 'd'): # slow right
            jump_sf = 1.0
            recursor = True
        elif (char == 'h') or (char == 'a'): # slow left
            jump_sf = -1.0
            recursor = True
        elif (char == 'L') or (char == 'D'): # fast right
            jump_sf = 10.0
            recursor = True
        elif (char == 'H') or (char == 'A'): # fast left
            jump_sf = -10.0
            recursor = True
        elif (char == 'k') or (char == 'w'): # slow zoom out
            zoom_sf = 1.4142135623730950488
        elif (char == 'j') or (char == 's'): # slow zoom in
            zoom_sf = 0.70710678118654752440
        elif (char == 'K') or (char == 'W'): # fast zoom out
            zoom_sf = 4.0
        elif (char == 'J') or (char == 'S'): # fast zoom in
            zoom_sf = 0.25
        elif char == 'n':
            cstate = cstate + 1 if cstate < J - 1 else -1
            recursor = True
        elif char == 'p':
            cstate = cstate - 1 if cstate > -1 else J - 1
            recursor = True
        elif (char == 'c') or (char == 'z'):
            view = center_view(xc, view)
            view = limit_view(view, lims)
            recursor = True
            remap = True
        elif char == 'g':
            jump_sf = (lims.x_min - xc)/dx
            recursor = True
        elif char == 'G':
            jump_sf = (lims.x_max - xc)/dx
            recursor = True
        else:
            continue

        # Process the zoom scaling factor.
        if zoom_sf != 1.0:
            if (zoom_sf > 1) and (view.x_min == lims.x_min) \
                    and (view.x_max == lims.x_max): # skip if zoomed out
                pass
            else:
                # Adjust the x-axis of the view.
                x_span = view.x_max - view.x_min
                p = 0.75*(xc - view.x_min)/x_span + 0.25*(0.5)
                x_span *= zoom_sf # change to the new span
                view.x_min = xc - p*x_span
                view.x_max = view.x_min + x_span
                # Adjust the y-axis of the view.
                x_set = x if cstate == -1 else x[cstate:cstate+1]
                y_set = y if cstate == -1 else y[cstate:cstate+1]
                view = get_view_y(x_set, y_set, view)
                # Limit the view and adjust the cursor jump size.
                view = limit_view(view, lims)
                dx = (view.x_max - view.x_min)/tws.cols
                recursor = True # update the cursor
                remap = True # remap the data to the canvas
            zoom_sf = 1.0 # reset the zoom scale factor

        # Update the cursor.
        if recursor:
            if cstate == -1:
                x_set = x
                y_set = y
                cF = "\x1b[0m"
            else:
                x_set = x[cstate:cstate+1]
                y_set = y[cstate:cstate+1]
                cF = f"\x1b[38;5;{NORMAL_COLORS[cstate % COLOR_CNT]}m"
            if jump_sf != 0.0:
                xc = move_cursor(xc, jump_sf*dx, x_set)
                jump_sf = 0.0 # reset the cursor jump scale factor
            if (xc < view.x_min) or (xc > view.x_max):
                # Adjust the view to center on xc.
                view = center_view(xc, view)
                # Adjust the y-axis of the view.
                view = get_view_y(x_set, y_set, view)
                # Limit the view and adjust the cursor jump size.
                view = limit_view(view, lims)
                remap = True
            ccol = get_column(xc, view, tws)
            yc_min, yc_max = get_cursor_y(ccol, tws, x_set, y_set, view)
            if yc_min == yc_max:
                cstr = f"({ftostr(xc)}, {ftostr(yc_max)})" # cursor readout
            else:
                cstr = f"({ftostr(xc)}, " \
                        + f"{ftostr(yc_min)}:" \
                        + f"{ftostr(yc_max)})" # cursor readout
            D[:, ccol] = True # wherever the cursor is now
            recursor = False

        # Remap the data to the canvas.
        if remap:
            # Map x and y to the expanded canvas, M, and the color matrix, F.
            M, F = data_to_matrix(x, y, view, tws)

            # Convert expanded canvas, M, to a matrix of character values, C.
            C = matrix_to_braille(M) if config.uni else matrix_to_ascii(M)
            D = D | (C != s) # wherever C is not a white space

            # Rebuild the ranges string.
            ranges = f"({ftostr(view.x_min)}:{ftostr(view.x_max)}, " \
                    + f"{ftostr(view.y_min)}:{ftostr(view.y_max)})"
            remap = False

        # Redraw the canvas.
        redraw_graph(C, D, ranges, label, F, ccol, cstr, cF, view, lims)
        D = (C != s) # wherever C is not a white space
        D[:, ccol] = True # wherever the cursor is

    # Restore terminal settings
    termios.tcsetattr(0, termios.TCSADRAIN, persistent.orig_term_attr)

    # Newline and show the cursor.
    sys.stdout.write("\r\033[?25h")
    sys.stdout.flush()


def bars(x, labels=None, cols=1, fat=False):
    """
    Create a bar graph of the data in `x` using the `labels` for each element
    of `x`.

    Parameters
    ----------
    x : float array like
        Set of values to plot as a bar graph.
    labels : string list, default None
        List of strings. This should be the same length as `x`.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of window
        columns if less than 1.
    fat : bool, default False
        Use thicker characters for the progress bar.
    """

    # Get the terminal window size.
    try: # Try to get the true size.
        term_cols, _ = os.get_terminal_size()
        term_cols -= 1
        colorize = True
    except: # If getting terminal size fails, use default values.
        term_cols = config.cols
        colorize = False

    # Convert a fractional `cols` to columns.
    if cols <= 1:
        cols = max(round(term_cols * cols), 18)

    # Get the width of labels.
    label_width = 0
    if labels is not None:
        label_width = max([len(l) for l in labels])

    # Adjust the total width to make room for labels.
    width = cols - label_width - 2
    if width < 1:
        width = 1

    # For each value of x, print the bar.
    span = max(x) - 0
    for n in range(len(x)):
        if labels is None:
            print(" |", end='')
        else:
            sstr = " " * (label_width - len(labels[n]))
            print(f"{sstr}{labels[n]} |", end='')
        ratio = x[n]/span
        draw_bar(width*ratio, width, colorize, fat)
        print("", flush=True)


def heat(matrix):
    """
    Create a surface plot using the input `matrix`. The rows are printed in
    reverse order.
    """

    # Scale the matrix.
    m_min = np.min(matrix)
    m_max = np.max(matrix)
    M = np.round((matrix - m_min)/(m_max - m_min)*23).astype(int) + 232
    rows, cols = M.shape

    # Print the matrix.
    if config.uni:
        for row in range(0, (rows - rows%2), 2):
            for col in range(cols):
                print("\x1b[38;5;%dm\x1b[48;5;%dm\u2580" %
                        (M[row, col], M[row + 1, col]), end='', flush=True)
            print("\x1b[0m", flush=True)
        if rows % 2 == 1:
            for col in range(cols):
                print("\x1b[38;5;%dm\u2580" % (M[-1, col]), end='', flush=True)
            print("\x1b[0m", flush=True)
    else:
        for row in range(rows):
            for col in range(cols):
                print("\x1b[48;5;%dm  " % (M[row, col]), end='')
            print("\x1b[0m")


def table(matrix, head=None, left=None, width=10, sep='  '):
    """
    Print a table to the terminal.

    Parameters
    ----------
    matrix : list of lists of values
        Table of values.
    head : list of strings, default []
        List of header labels.
    left : list of strings, default []
        List of left-most column labels.
    width : int, default 10
        Width in characters of each cell.
    sep : string, default '   '
        String separating columns.
    """

    # -----------------
    # Check the inputs.
    # -----------------

    # Check the type of matrix.
    if isinstance(matrix, (str, float, int)):
        matrix = [[matrix]]
    elif isinstance(matrix, list):
        is_2d = False
        for n, datum in enumerate(matrix):
            if isinstance(datum, np.ndarray):
                is_2d = True
                matrix[n] = datum.tolist()
            elif isinstance(datum, list):
                is_2d = True
        if not is_2d:
            matrix = [matrix]
    elif isinstance(matrix, np.ndarray):
        matrix = matrix.tolist()
        if not isinstance(matrix[0], list):
            matrix = [matrix]
    else:
        raise Exception('heat: matrix must be a list!')

    # Check the type of head.
    if head is None:
        head = []
    elif isinstance(head, (str, float, int)):
        head = [head]
    elif isinstance(head, np.ndarray):
        head = head.tolist()
    elif not isinstance(head, list):
        raise Exception('heat: head must be a list!')

    # Check the type of left.
    if left is None:
        left = []
    elif isinstance(left, (str, float, int)):
        left = [left]
    elif isinstance(left, np.ndarray):
        left = left.tolist()
    elif not isinstance(left, list):
        raise Exception('heat: left must be a list!')

    # Check that width is within 3 to 30.
    if width < 6:
        width = 6
    elif width > 30:
        width = 30

    # -------------
    # Print header.
    # -------------

    def f2str(num, width=6):
        """
        Convert a floating-point number, `num`, to a string, keeping the total
        width in characters equal to `width`.
        """

        # Ensure width is not less than 6, and check if padding should not be
        # used (i.e., width was negative).
        if width < 0:
            width = -width
            skip_padding = True
        else:
            skip_padding = False
        if width < 6:
            width = 6

        # Make num non-negative but remember the minus.
        if num < 0:
            sw = 1
            s = "-"
            num = -num
            ei = int(np.floor(np.log10(num))) # integer exponent
        elif num > 0:
            sw = 0
            s = ""
            ei = int(np.floor(np.log10(num))) # integer exponent
        else:
            sw = 0
            s = ""
            ei = 0

        # Build number string without leading spaces.
        if ei >= 4:     # 10000 to inf
            f_str = s + "%.*g" % (width - 2 - len(str(ei)) - sw,
                    num*(10**(-ei)))
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
            f_str += "e%d" % (ei)
        elif ei >= 0:   # 1 to 10-
            f_str = s + "%.*f" % (width - 2 - ei - sw, num)
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
        elif ei >= -3:  # 0.001 to 1-
            f_str = s + "%.*f" % (width - 2 - sw, num)
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
        else:           # -inf to 0.001-
            f_str = s + "%.*g" % (width - 3 - len(str(-ei)) - sw,
                    num*(10**(-ei)))
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
            f_str += "e%d" % (ei)

        # Add leading spaces for padding.
        if not skip_padding:
            f_str = " "*(width - len(f_str)) + f_str

        return f_str

    def fixed_width_string(C, width=6):
        """
        Convert a string or numeric value, `C`, to a string, keeping the total
        width in characters equal to `width`.
        """

        if isinstance(C, str):
            L = len(C)
            if L > width:
                L = width - 3
                return C[:L] + '...'
            elif L == width:
                return C
            else:
                return ' '*(width-L) + C
        elif isinstance(C, float):
            return f2str(C, width)
        else:
            return f2str(float(C), width)

    if len(head) > 0:
        row_str = ""
        if len(left) > 0:
            row_str += " "*width + " | "
        for n_col, val in enumerate(head):
            if n_col > 0:
                row_str += sep
            row_str += fixed_width_string(val, width)
        print(row_str)

        row_str = ""
        if len(left) > 0:
            row_str += "-"*width + " | "
        for n_col in range(len(head)):
            if n_col > 0:
                row_str += sep
            row_str += "-"*width
        print(row_str)

    # -------------
    # Print matrix.
    # -------------

    for n_row, vals in enumerate(matrix):
        row_str = ""
        if len(left) > n_row:
            row_str += fixed_width_string(left[n_row], width) + " | "
        elif len(left) > 0:
            row_str += " "*width + " | "
        for n_col, val in enumerate(vals):
            if n_col > 0:
                row_str += sep
            row_str += fixed_width_string(val, width)
        print(row_str)


def sparsity(matrix, label=''):
    """
    Print the sparsity of a matrix. Note, if you are using SciPy sparse arrays
    or matrices, use the method `toarray()` on the input to this function.
    """

    # Convert matrix to zeros and ones.
    M = (np.abs(matrix) > 1e-30).astype(int)

    # Convert the large matrix to a smaller matrix of character values.
    C = matrix_to_braille(M) if config.uni else matrix_to_stars(M)

    # Create the shape string.
    shape_str = f"{matrix.shape[0]}x{matrix.shape[1]}"

    # Draw the plot.
    draw_graph(C, shape_str, label)


def progress(k, K, t_init=None, cols=1, fat=False):
    """
    Output a simple progress bar with percent complete to the terminal. When `k`
    equals `K - 1`, the progress bar will complete and start a new line.

    Parameters
    ----------
    k : int
        Index which should grow monotonically from 0 to K - 1.
    K : int
        Final index value of `k` plus 1.
    t_init : float, default None
        Initial process time (s). If provided, an estimated time remaining will
        be displayed. If left as None, no time will be shown. When the progress
        bar completes, the total duration will be shown.
    cols : int, default 1
        Desired width of the full string, including the percent complete, the
        bar, and the clock if greater than 1 or fraction of window columns if
        less than 1.
    fat : bool, default False
        Use thicker characters for the progress bar.
    """

    # Skip this call if the bar is not done but not enough time has passed.
    t_now = time.perf_counter()
    if (k + 1 < K) and (persistent.t_last is not None) and \
            (t_now - persistent.t_last < 0.1):
        return
    persistent.t_last = t_now

    # Get the terminal window size.
    try: # Try to get the true size.
        term_cols, _ = os.get_terminal_size()
        term_cols -= 1
        colorize = True
    except: # If getting terminal size fails, use default values.
        term_cols = config.cols
        colorize = False

    # Convert a fractional `cols` to columns.
    if cols <= 1:
        cols = max(round(term_cols * cols), 18)

    # Get the ratio.
    ratio = (k + 1)/K if k < K - 1 else 1

    # Get the clock string.
    if t_init is not None:
        t_diff = t_now - t_init
        if k + 1 == K:
            clk_str = "  " + time_str(t_diff)
        else:
            t_left = 0.0 if ratio <= 0 else t_diff*(1 - ratio)/ratio
            clk_str = " -" + time_str(t_left)
    else:
        clk_str = ""

    # Maximum length of bar
    N = cols - 5 - len(clk_str)

    # Build the progress bar.
    print(f"\r{int(100*ratio):3d}% ", end='')
    draw_bar(N*ratio, N, colorize, fat)
    if k + 1 >= K:
        print(f"{clk_str}", flush=True)
    else:
        print(f"{clk_str}", end='', flush=True)

# -----------------
# Support functions
# -----------------

def signal_handler(sig, frame):
    # Restore terminal settings
    termios.tcsetattr(0, termios.TCSADRAIN, persistent.orig_term_attr)

    # Newline and show the cursor.
    sys.stdout.write("\r\033[?25h")
    sys.stdout.flush()

    # Exit.
    sys.exit(0)


def istty():
    """
    Try to determine if the current standard output is a teletype output. If it
    is we might assume it can handle ANSI escape codes.
    """
    is_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return is_tty


def screen_size(rows, cols):
    # Get the terminal window size.
    try: # Try to get the true size.
        term_cols, term_rows = os.get_terminal_size()
    except: # If getting terminal size fails, use default values.
        term_cols = config.cols
        term_rows = config.rows
    term_rows -= 1 # Account for the prompt line.

    # Convert a fractional canvas size to columns and rows.
    if cols < 0:
        raise ValueError(f"cols should be positive: {cols}!")
    elif cols <= 1:
        cols = max(round(term_cols * cols), 3)
    if rows < 0:
        raise ValueError(f"rows should be positive: {rows}!")
    elif rows <= 1:
        rows = max(round(term_rows * rows), 3)

    # Adjust for the bounding box and ensure integer type.
    rows = int(rows) - 2
    cols = int(cols) - 2

    # Define the sub-columns and sub-rows.
    if config.uni:
        subcols = 2
        subrows = 4
    else:
        subcols = 1
        subrows = 3

    # Load the dimensions into an object.
    tws = term_ws(rows, cols, subrows, subcols)

    return tws


def shape_xy(x, y):
    # If only `x` is provided, copy to `y`
    # and make `x` an array of integers.
    if y is None:
        y = x + 0
        if np.ndim(y) == 0:
            x = 1.0
        elif np.ndim(y) == 1:
            x = np.arange(len(y))
        elif np.ndim(y) == 2:
            J, K = y.shape
            x = np.arange(K)
            x = np.outer(np.ones(J), x)
    if isinstance(y, str):
        raise ValueError(f"y should not be a string: {y}!")

    # Ensure x and y are both 2D arrays.
    x = np.array(x)
    y = np.array(y)
    if np.ndim(x) == 0:
        x = np.array([[x]])
    elif np.ndim(x) == 1:
        x = np.array([x])
    if np.ndim(y) == 0:
        y = np.array([[y]])
    elif np.ndim(y) == 1:
        y = np.array([y])

    # Ensure x and y have compatible shapes.
    Jx, Kx = x.shape
    Jy, Ky = y.shape
    if Jx != Jy:
        if Jx == 1 and Jy > 1:
            x = np.outer(np.ones(Jy), x)
            Jx = Jy
        elif Jx > 1 and Jy == 1:
            y = np.outer(np.ones(Jx), y)
            Jy = Jx
        else:
            raise ValueError("x and y must have 1 or the same number of rows.")
    if Kx != Ky:
        raise ValueError("x and y must have the same number of columns.")

    return x, y


def limits_xy(x, y, tws, equal):
    # Get the data shape and array of indices.
    J, K = x.shape
    nn = np.arange(K)

    # Get the limits.
    x_min = np.inf; x_max = -np.inf
    y_min = np.inf; y_max = -np.inf
    # For each row of data,
    for j in range(J):
        # Get this curve.
        xj = x[j].copy()
        yj = y[j].copy()

        # Find the valid points by index.
        nn_valid = np.intersect1d(nn[np.isfinite(xj)], nn[np.isfinite(yj)])

        # Expand the limits.
        x_min = min(x_min, np.min(xj[nn_valid]))
        x_max = max(x_max, np.max(xj[nn_valid]))
        y_min = min(y_min, np.min(yj[nn_valid]))
        y_max = max(y_max, np.max(yj[nn_valid]))

    # Enforce differentiation.
    eps = 1e-16
    if x_min == x_max:
        x_min -= eps
        x_max += eps
    if y_min == y_max:
        y_min -= eps
        y_max += eps

    # Apply axis scaling.
    if equal != 0:
        x_scale = (1/config.ar)*cols/(x_max - x_min)
        y_scale = tws.rows/(y_max - y_min)
        if x_scale*equal < y_scale:
            y_scale = x_scale*equal
            y_span = tws.rows/y_scale
            y_mid = (y_max + y_min)*0.5
            y_min = y_mid - y_span*0.5
            y_max = y_mid + y_span*0.5
        elif y_scale < x_scale*equal:
            x_scale = y_scale/equal
            x_span = (1/config.ar)*cols/x_scale
            x_mid = (x_max + x_min)*0.5
            x_min = x_mid - x_span*0.5
            x_max = x_mid + x_span*0.5

    # Expand the limits to align zero with the nearest half row so that the zero
    # marker is true. FIXME This formula is likely wrong!
    if (y_min < 0) and (y_max > 0):
        idx_zero = round((tws.rows - 1.0/tws.subrows)
            * y_max/(y_max - y_min) - 0.5)*tws.subrows + tws.subrows/2
        slope = max((tws.subrows*tws.rows - 1 - idx_zero)/y_min,
            -idx_zero/y_max)
        y_min = (tws.subrows*tws.rows - 1 - idx_zero)/slope
        y_max = -idx_zero/slope
        row_zero = math.floor((tws.rows - 1/tws.subrows)*
                (y_max)/(y_max - y_min))
    else:
        row_zero = -1

    # Put limits into an object.
    lims = limits(x_min, x_max, y_min, y_max)

    return lims, row_zero


def data_to_matrix(x, y, view, tws):
    # Get the shape of the data.
    J, K = x.shape
    x_span = view.x_max - view.x_min
    y_span = view.y_max - view.y_min

    # Get total numbers of subrows and subcolumns.
    Rows = tws.subrows*tws.rows
    Cols = tws.subcols*tws.cols

    # Check if colors are likely supported.
    colorize = istty()

    # Initialize the data and color matrices.
    M = np.zeros((Rows, Cols), dtype=int)
    if (J > 1) and (colorize):
        F = np.zeros((tws.rows, tws.cols), dtype=int)
    else:
        F = None

    # For each curve, set the points and colors.
    kk = np.arange(K)
    for j in range(J):
        # Find the valid points by index.
        x_valid = np.isfinite(x[j]) & \
                (x[j] >= view.x_min) & (x[j] <= view.x_max)
        y_valid = np.isfinite(y[j]) & \
                (y[j] >= view.y_min) & (y[j] <= view.y_max)
        kk_valid = np.intersect1d(kk[x_valid], kk[y_valid])

        # Scale the data to dots. First dot is 0; last dot is Cols - 1.
        X_jk = Cols*(x[j, kk_valid] - view.x_min)/x_span - 0.5
        Y_jk = Rows*(view.y_max - y[j, kk_valid])/y_span - 0.5
        X = np.clip(np.round(X_jk).astype(int), 0, Cols - 1)
        Y = np.clip(np.round(Y_jk).astype(int), 0, Rows - 1)

        # Map locations to a large matrix.
        M[Y, X] = 1 # Puts a 1 wherever the curve coordinates are.

        # Scale the data to dots.
        if (J > 1) and (colorize):
            u = X//tws.subcols
            v = Y//tws.subrows
            F[v, u] = NORMAL_COLORS[j % COLOR_CNT]

    return M, F


def move_cursor(xc, dx, x):
    # Get the target x value.
    xcp = xc + dx

    # For each row, get the best-fit index in `x`.
    J, K = x.shape
    kkc = np.zeros(J, dtype=int)
    for j in range(J):
        if dx > 0:
            if x[j, -1] <= xcp:
                kkc[j] = K - 1
            else:
                kkc[j] = np.where(x[j] >= xcp, x, np.inf).argmin()
        elif dx < 0:
            if x[j, 0] >= xcp:
                kkc[j] = 0
            else:
                kkc[j] = np.where(x[j] <= xcp, x, -np.inf).argmax()
        else:
            kkc[j] = np.abs(x[j] - xcp).argmin()

    # Find closest match in `x`.
    jc = np.abs(x[:, kkc] - xcp).argmin()
    kc = kkc[jc]
    xc = x[jc, kc]

    return xc


def limit_view(view, lims):
    x_span = view.x_max - view.x_min
    if view.x_min < lims.x_min:
        view.x_min = lims.x_min
        view.x_max = view.x_min + x_span
    if view.x_max > lims.x_max:
        view.x_max = lims.x_max
        view.x_min = view.x_max - x_span
    if view.x_min < lims.x_min:
        view.x_min = lims.x_min
    if view.x_max > lims.x_max:
        view.x_max = lims.x_max
    if view.y_min < lims.y_min:
        view.y_min = lims.y_min
    if view.y_max > lims.y_max:
        view.y_max = lims.y_max
    return view


def center_view(xc, view):
    x_span = view.x_max - view.x_min
    view.x_min = xc - x_span/2
    view.x_max = view.x_min + x_span
    return view

def get_column(xc, view, tws):
    x_span = view.x_max - view.x_min
    ccol = round(tws.cols*(xc - view.x_min)/x_span - 0.5)
    ccol = min(max(ccol, 0), tws.cols - 1)
    return ccol


def get_cursor_y(ccol, tws, x, y, view):
    # Get range of x values from left to right of cursor.
    x_span = view.x_max - view.x_min
    xc_a = x_span*(ccol/tws.cols) + view.x_min
    xc_b = xc_a + x_span/tws.cols

    # Initialize the y limits.
    yc_min = np.inf
    yc_max = -np.inf

    # Search each row of (x, y).
    J, K = x.shape
    for j in range(J):
        kc_a = np.where(x[j] >= xc_a, x, np.inf).argmin()
        kc_b = np.where(x[j] <= xc_b, x, -np.inf).argmax()
        y_min = y[j, kc_a:kc_b + 1].min()
        y_max = y[j, kc_a:kc_b + 1].max()
        yc_min = min(yc_min, y_min)
        yc_max = max(yc_max, y_max)

    return yc_min, yc_max


def get_view_y(x, y, view):
    # Initialize the y limits.
    yv_min = np.inf
    yv_max = -np.inf

    # Search each row of (x, y).
    J, K = x.shape
    for j in range(J):
        kc_a = np.where(x[j] >= view.x_min, x, np.inf).argmin()
        kc_b = np.where(x[j] <= view.x_max, x, -np.inf).argmax()
        y_min = y[j, kc_a:kc_b + 1].min()
        y_max = y[j, kc_a:kc_b + 1].max()
        yv_min = min(yv_min, y_min)
        yv_max = max(yv_max, y_max)

    view.y_min = yv_min
    view.y_max = yv_max
    return view


def ftostr(f):
    """ Convert a floating-point value to a string, without the useless `+` sign
    or leading zeros in the exponent. """
    return f"{f:0.6g}".replace("e+0", "e").replace("e-0", "e-")


def time_str(t_seconds):
    """ Convert time in seconds to a clock string of the form
    `HH:MM:SS.S`. """
    t_seconds = abs(t_seconds)
    hours = int(t_seconds/3600)
    minutes = int((t_seconds - hours*3600)//60)
    seconds = (t_seconds % 60)
    clock_str = "%02d:%02d:%04.1f" % (hours, minutes, seconds)
    return clock_str


def matrix_to_braille(M):
    # Pad the matrix with zeros.
    I, J = M.shape
    II = math.ceil(I/4)*4
    JJ = math.ceil(J/2)*2
    MM = np.zeros((II, JJ), dtype=int)
    MM[:I, :J] = M

    # Convert the matrix of ones and zeros to braille characters.
    C = (0x2800 + MM[::4, ::2] +   8*MM[::4, 1::2]
            +  2*MM[1::4, ::2] +  16*MM[1::4, 1::2]
            +  4*MM[2::4, ::2] +  32*MM[2::4, 1::2]
            + 64*MM[3::4, ::2] + 128*MM[3::4, 1::2])
    return C


def matrix_to_ascii(M):
    # Pad the matrix with zeros.
    I, J = M.shape
    II = math.ceil(I/3)*3
    MM = np.zeros((II, J), dtype=int)
    MM[:I, :J] = M[:I, :J]

    # Convert the matrix of ones and zeros to braille characters.
    glyphs = np.array([ # " `-'.!:|"
        0x20, 0x60, 0x2D, 0x27, 0x2E, 0x21, 0x3A, 0x7C])
    C = glyphs[M[::3] + 2*M[1::3] + 4*M[2::3]]
    return C


def matrix_to_stars(M):
    I, J = M.shape
    C = 0x20*np.ones((I, 2*J + 1), dtype=int)
    C[:, 1:-1:2] += 0xA*M
    return C


def draw_graph(C, left=None, right=None, F=None, row_zero=-1):
    """
    Parameters
    ----------
    C : (I, J) int np.ndarray
        Matrix of character values.
    left : string, default None
        String to place on the left of the box.
    right : string, default None
        String to place on the right of the box.
    F : (I, J) int np.ndarray, default None
        Matrix of foreground 8-bit color values.
    row_zero : int, default -1
        Row index of y = 0.
    """

    # Define the box drawing characters.
    if config.uni:
        b = ["\u250C", "\u2500", "\u2510",  # . - .
                "\u2502", "\u2502",         # |   |
                "\u251C", "\u2524",         # +   +
                "\u2514", "\u2518"]         # '   '
        s = 0x2800 # braille space
    else:
        b = [".", "-", ".", "|", "|", "+", "+", "'", "'"]
        s = 0x20 # ASCII space

    # Replace zeros with spaces.
    C = np.where(C == 0, s, C)

    # Draw the top edge of the box.
    rows, cols = C.shape
    print(b[0], end='', flush=True)
    for col in range(cols):
        print(b[1], end='', flush=True)
    print(b[2], flush=True)

    # For each row of the matrix, draw the contents and two sides of the box.
    for row in range(rows):
        # Get the side characters.
        if row != row_zero:
            l = b[3]
            r = b[4]
        else:
            l = b[5]
            r = b[6]

        # Get this row of data.
        F_row = 0 if F is None else F[row]
        C_row = C[row]

        # Draw this row.
        print(l + "\x1b[1m", end='', flush=True)
        f_last = 0
        for col in range(cols):
            # Get this column color.
            f = 0 if F is None else F_row[col]

            if f_last != f:
                if f == 0:
                    print("\x1b[0;1m", end='')
                else:
                    print(f"\x1b[38;5;{f}m", end='')
                f_last = f
            print(chr(C_row[col]), end='', flush=True)
        if f_last != 0:
            print("\x1b[0;1m", end='')
        print(r, flush=True)

    # Get the number of middle dashes.
    mid_dashes = cols - 2
    if left is not None:
        mid_dashes -= len(left) + 2
    if right is not None:
        mid_dashes -= len(right) + 2

    # Draw the bottom of the box and the left and right strings.
    if mid_dashes >= 0:
        print(f"{b[7]}{b[1]}", end='', flush=True)
        if left is not None:
            print(f" {left} ", end='', flush=True)
        for col in range(mid_dashes):
            print(b[1], end='', flush=True)
        if right is not None:
            print(f" {right} ", end='', flush=True)
        print(f"{b[1]}{b[8]}", flush=True)
    else:
        print(f"{b[7]}", end='', flush=True)
        for col in range(cols):
            print(b[1], end='', flush=True)
        print(f"{b[8]}", flush=True)
        if left is not None:
            print(left, end='', flush=True)
        if right is not None:
            if left is not None:
                print(", ", end='', flush=True)
            print(right, end='', flush=True)
        print('', flush=True)


def redraw_graph(C, D, left=None, right=None,
        F=None, ccol=None, cstr=None, cF=None, view=None, lims=None):
    """
    Parameters
    ----------
    C : (I, J) int np.ndarray
        Matrix of character values.
    D : (I, J) int np.ndarray
        Matrix of boolean values marking changed characters.
    left : string, default None
        String to place on the left of the box.
    right : string, default None
        String to place on the right of the box.
    F : (I, J) int np.ndarray, default None
        Matrix of foreground 8-bit color values.
    ccol : int, default None
        Column index of cursor.

    Notes
    -----
    0.022614872267481156 1.00 # baseline
    0.007898384667653082 2.86 # skipping to deltas
    0.007420537999439004 3.05 # removing the recalculation of C
    """

    # Define the box drawing characters.
    if config.uni:
        b = ["\u250C", "\u2500", "\u2510",  # . - .
                "\u2502", "\u2502",         # |   |
                "\u251C", "\u2524",         # +   +
                "\u2514", "\u2518"]         # '   '
        s = 0x2800 # braille space
    else:
        b = [".", "-", ".", "|", "|", "+", "+", "'", "'"]
        s = 0x20 # ASCII space

    # Replace zeros with spaces.
    C = np.where(C == 0, s, C)

    # Move the cursor up to the top left corner of the border.
    rows, cols = C.shape
    print(f"\x1b[{rows + 2}A", end='', flush=True)

    # Draw the zoom bar.
    print(b[0] + "\x1b[1m", end='', flush=True)
    if (view.x_min > lims.x_min) or (view.x_max < lims.x_max):
        # Get the start and stop columns of the zoom bar.
        x_span = lims.x_max - lims.x_min
        bar_width = round(cols*(view.x_max - view.x_min)/x_span)
        bar_width = max(1, bar_width)
        if view.x_min == lims.x_min:
            col_a = 0
            col_b = col_a + bar_width
        elif view.x_max == lims.x_max:
            col_b = cols
            col_a = col_b - bar_width
        else:
            x_view = (view.x_max + view.x_min)/2
            col_center = round(cols*(x_view - lims.x_min)/x_span)
            col_a = max(0, round(col_center - bar_width/2))
            col_b = min(cols - 1, col_a + bar_width)
        # Draw the bar.
        print("\x1b[38;5;238m", end="", flush=True)
        for col in range(cols):
            if col == col_a:
                print("\x1b[0;1m", end="", flush=True)
            if col == col_b:
                print("\x1b[38;5;238m", end="", flush=True)
            print(b[1], end='', flush=True)
        print("\x1b[0;1m", end="", flush=True)
    else:
        for col in range(cols):
            print(b[1], end='', flush=True)
    print(f"{b[2]}", flush=True)

    # For each row of the matrix, draw the contents.
    for row in range(rows):
        # Get this row of data.
        F_row = 0 if F is None else F[row]
        C_row = C[row]

        # Draw this row.
        print("\x1b[1C\x1b[1m", end='', flush=True) # Move past left border
        f_last = 0
        col_last = -1
        for col in range(cols):
            # Skip where there is no delta.
            if not D[row, col]:
                continue

            # Jump to new character location.
            if col > col_last + 1:
                print(f"\x1b[{col - col_last - 1}C", end='', flush=True)
            col_last = col

            # Get this column color.
            f = 0 if F is None else F_row[col]
            if F is None:
                f = 0
            else:
                f = F_row[col]
                if (col == ccol) and (f != 0): # Switch to bright colors.
                    f = BRIGHT_COLORS[NORMAL_COLORS.index(f)]

            # Display the cursor.
            if (col == ccol) and (C_row[col] == s):
                print(cF + b[3] + '\x1b[0;1m', end='', flush=True)
                f_last = 0
            else:
                if f_last != f:
                    if f == 0:
                        print("\x1b[0;1m", end='')
                    else:
                        print(f"\x1b[38;5;{f}m", end='')
                    f_last = f
                print(chr(C_row[col]), end='', flush=True)
        if f_last != 0:
            print("\x1b[0;1m", end='', flush=True)
        print('', flush=True)

    # Get the number of middle dashes.
    mid_dashes = cols - 2
    if left is not None:
        mid_dashes -= len(left) + 2
    if right is not None:
        mid_dashes -= len(right) + 2
    if cstr is not None:
        mid_dashes -= len(cstr) + 2

    # Draw the bottom of the box and the left and right strings.
    if mid_dashes >= 0:
        print(f"{b[7]}{b[1]}", end='', flush=True)
        if left is not None:
            print(f" {left} ", end='', flush=True)
        if cstr is not None:
            print(f" {cF}", end='', flush=True)
            print(f"{cstr}", end='', flush=True)
            print("\x1b[0m ", end='', flush=True)
        for col in range(mid_dashes):
            print(b[1], end='', flush=True)
        if right is not None:
            print(f" {right} ", end='', flush=True)
        print(f"{b[1]}{b[8]}", flush=True)
    else:
        print(f"{b[7]}", end='', flush=True)
        for col in range(cols):
            print(b[1], end='', flush=True)
        print(f"{b[8]}", flush=True)
        if left is not None:
            print(left, end='', flush=True)
        if cstr is not None:
            print(" " + cF, end='', flush=True)
            print(cstr, end='', flush=True)
            print("\x1b[0m", end='', flush=True)
        if right is not None:
            if (left is not None) or (cstr is not None):
                print(", ", end='', flush=True)
            print(right, end='', flush=True)
        print('', flush=True)


def draw_bar(n, N, colorize, fat):
    # Define the left, center, and right characters and color commands.
    if colorize:
        grey = '\x1b[100m' if config.uni and fat else '\x1b[90m'
    else:
        grey = ''
    if config.uni:
        if fat:
            l = chr(0x2588)
            frac = int(n*8) % 8 # 0 to 7
            c = ' ' if frac == 0 else chr(0x2588 + 8 - frac)
            c = grey + c
            r = ' '
        else:
            l = chr(0x2501)
            if (n) % 1 < 0.5:
                c = grey + chr(0x257A) if colorize else ' '
            else:
                c = chr(0x2578) + grey
            r = chr(0x2501) if colorize else ' '
    else:
        if fat:
            l = '/'
            c = grey + '-' if (n % 1 < 0.5) else '/' + grey
            r = '-'
        else:
            l = '='
            c = grey + '-' if (n % 1 < 0.5) else '=' + grey
            r = '-'

    # Build the progress bar.
    if n >= N:
        for j in range(N):
            print(l, end='', flush=True)
    else:
        bar_len = int(n)
        spc_len = N - 1 - bar_len
        for j in range(bar_len):
            print(l, end='', flush=True)
        print(c, end='', flush=True)
        for j in range(spc_len):
            print(r, end='', flush=True)
        if colorize:
            print('\x1b[0m', end='', flush=True)
