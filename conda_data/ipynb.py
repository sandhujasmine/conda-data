from IPython.html import widgets  # Widget definitions
from IPython.display import display  # Used to display widgets in the notebook


def progress():
    widget = widgets.IntProgress()
    display(widget)

    def inner(value, total):
        widget.max = total
        widget.value = value

    return inner
