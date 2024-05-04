from typing import Union
from tkfontselector.tkfontselector import FontSelector
from tkinter import Tk, Toplevel


def ask_font(
    master: Union[Tk, Toplevel, None] = None,
    text: str = "Abcd",
    title: str = "Font Selector",
    fixed_only: bool = False,
    **font_args
) -> dict:
    """
    Open the Font Selector and return a dictionary of the font properties.

    General Arguments:
        master: Tk or Toplevel instance
            master window
        text: str
            sample text to be displayed in the Font Selector
        title: str
            dialog title
        fixed_only: bool
            Display fixed only families

    Font arguments:
        family: str
            font family
        size: int
            font size
        slant: str
            "roman" or "italic"
        weight: str
            "normal" or "bold"
        underline: bool
            whether the text is underlined
        overstrike: bool
            whether the text is overstriked

    Output:

        dictionary is similar to the one returned by the ``actual`` method of a tkinter ``Font`` object:
            {'family': str,
             'size': int,
             'weight': 'bold'/'normal',
             'slant': 'italic'/'roman',
             'underline': bool,
             'overstrike': bool}

    """
    chooser = FontSelector(master, font_args, text, title, fixed_only)
    chooser.wait_window(chooser)
    return chooser.get_res()
