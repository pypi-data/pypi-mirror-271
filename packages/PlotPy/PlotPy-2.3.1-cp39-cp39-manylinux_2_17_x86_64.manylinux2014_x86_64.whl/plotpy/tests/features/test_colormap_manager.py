# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see plotpy/LICENSE for details)

"""
ColorMapManager test

This plotpy widget can be used to manage colormaps (visualize, edit, create ans save).
"""

# guitest: show

import qtpy.QtCore as QC
import qtpy.QtGui as QG
from guidata.env import execenv
from guidata.qthelpers import exec_dialog, qt_app_context

from plotpy.mathutils.colormap import ALL_COLORMAPS
from plotpy.widgets.colormap.manager import ColorMapManager
from plotpy.widgets.colormap.widget import EditableColormap


def test_colormap_manager() -> None:
    """Test the colormap manager widget."""
    with qt_app_context():
        red = QG.QColor(QC.Qt.GlobalColor.red)
        blue = QG.QColor(QC.Qt.GlobalColor.blue)
        yellow = QG.QColor(QC.Qt.GlobalColor.yellow)
        cmap = EditableColormap(blue, yellow, name="kinda_viridis")
        ALL_COLORMAPS["kinda_viridis"] = cmap
        dlg = ColorMapManager(None, active_colormap="YlGn")
        dlg.colormap_editor.colormap_widget.add_handle_at_relative_pos(0.5, red)
        dlg.get_colormap()
        dlg.colormap_editor.update_colormap_widget()
        dlg.colormap_editor.update_current_dataset()
        result = exec_dialog(dlg)
        execenv.print("Dialog result:", result)
        cmap = dlg.get_colormap()
        execenv.print("Selected colormap:", None if cmap is None else cmap.name)


if __name__ == "__main__":
    test_colormap_manager()
