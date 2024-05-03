"""
Helper functions for applying styles to plots from configurations.

Each `style` function takes at least two arguments. The first argument is the
object to be styled. The remaining arguments are properties that should be
applied as part of the styling. In most cases, they are direct maps to a `Set..`
function of the object. The argument can either be a string or the type expected
by the object functon. In case of string, automatic conversion is attempted.
"""

import ROOT

def style(obj, **kwargs):
    """
    Apply style to `obj` based on `kwargs`. This forwards all necessary style
    functions based on the inherted classes by `obj`.
    """
    if obj.InheritsFrom('TAttLine'):
        style_TAttLine(obj, **kwargs)

def style_TAttLine(obj, **kwargs):
    """
    Apply style to a TAttLine object. The following properties are supported:
     - `color` or `linecolor` -> `SetLineColor`
     - `linewidth` -> `SetLineWidth`
    """
    linecolor=None
    if 'color' in kwargs:
        linecolor=kwargs['color']
    if 'linecolor' in kwargs:
        linecolor=kwargs['linecolor']

    if linecolor is not None:
        if type(linecolor) is str:
            linecolor=getattr(ROOT, linecolor)
        obj.SetLineColor(linecolor)

    if 'linewidth' in kwargs:
        obj.SetLineWidth(kwargs['linewidth'])

def style_TAttMarker(obj, **kwargs):
    """
    Apply style to a TAttMarker object. The following properties are supported:
     - `color` or `markercolor` -> `SetMarkerColor`
    """
    markercolor=None
    if 'color' in kwargs:
        markercolor=kwargs['color']
    if 'markercolor' in kwargs:
        markercolor=kwargs['markercolor']

    if markercolor is not None:
        if type(markercolor) is str:
            markercolor=getattr(ROOT, markercolor)
        obj.SetmarkerColor(markercolor)
