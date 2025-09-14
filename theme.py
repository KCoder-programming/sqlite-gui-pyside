"""Module loading QPalette."""
from PySide6.QtGui import QColor, QPalette

light_palette = QPalette()

# base
light_palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
light_palette.setColor(QPalette.ColorRole.Button, QColor("#f6f6f6"))
light_palette.setColor(QPalette.ColorRole.Text, QColor("#242424"))
light_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#095eb8"))
light_palette.setColor(QPalette.ColorRole.Base, QColor("#f6f6f6"))
light_palette.setColor(QPalette.ColorRole.Window, QColor("#cecece"))
light_palette.setColor(QPalette.ColorRole.Highlight, QColor("#127def"))
light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#f6f6f6"))
light_palette.setColor(QPalette.ColorRole.Link, QColor("#f6f6f6"))
light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#e9e9e9"))
light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#4d4d4d"))
light_palette.setColor(QPalette.ColorRole.LinkVisited, QColor("#660098"))
light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#4d4d4d"))
if hasattr(QPalette.ColorRole, "Foreground"):
    light_palette.setColor(QPalette.ColorRole.Foreground, QColor("#4d4d4d"))  # type: ignore
if hasattr(QPalette.ColorRole, "PlaceholderText"):
    light_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#696969"))

light_palette.setColor(QPalette.ColorRole.Light, QColor("#dadada"))
light_palette.setColor(QPalette.ColorRole.Midlight, QColor("#dadada"))
light_palette.setColor(QPalette.ColorRole.Dark, QColor("#4d4d4d"))
light_palette.setColor(QPalette.ColorRole.Mid, QColor("#dadada"))
light_palette.setColor(QPalette.ColorRole.Shadow, QColor("#dadada"))

# disabled
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#bababa"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#bababa"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#dadada"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor("#dadada"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor("#bababa"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor("#bababa"))
light_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor("#bababa"))

# inactive
light_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor("#e4e4e4"))

LIGHT_PALETTE = light_palette



dark_palette = QPalette()

# base
dark_palette.setColor(QPalette.ColorRole.WindowText, QColor("#e4e4e4"))
dark_palette.setColor(QPalette.ColorRole.Button, QColor("#303030"))
dark_palette.setColor(QPalette.ColorRole.Text, QColor("#efefef"))
dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#d2aa02"))
dark_palette.setColor(QPalette.ColorRole.Base, QColor("#2d2d2d"))
dark_palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
dark_palette.setColor(QPalette.ColorRole.Highlight, QColor("#d2aa02"))
dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#202020"))
dark_palette.setColor(QPalette.ColorRole.Link, QColor("#202020"))
dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#303030"))
dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#292929"))
dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#e4e4e4"))
dark_palette.setColor(QPalette.ColorRole.LinkVisited, QColor("#c58af8"))
dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#292929"))
dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#e4e4e4"))
if hasattr(QPalette.ColorRole, "Foreground"):
    dark_palette.setColor(QPalette.ColorRole.Foreground, QColor("#e4e4e4"))  # type: ignore
if hasattr(QPalette.ColorRole, "PlaceholderText"):
    dark_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#8a8a8a"))

dark_palette.setColor(QPalette.ColorRole.Light, QColor("#404040"))
dark_palette.setColor(QPalette.ColorRole.Midlight, QColor("#404040"))
dark_palette.setColor(QPalette.ColorRole.Dark, QColor("#e4e4e4"))
dark_palette.setColor(QPalette.ColorRole.Mid, QColor("#404040"))
dark_palette.setColor(QPalette.ColorRole.Shadow, QColor("#404040"))

# disabled
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#696969"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#696969"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#404040"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor("#535353"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor("#696969"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor("#696969"))
dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor("#696969"))

# inactive
dark_palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor("#393939"))

DARK_PALETTE = dark_palette


MENU_QSS_LIGHT = """
QMenuBar {
    background-color: #cecece;
    color: #000000;
}
QMenuBar::item:selected {
    background: #f6f6f6;
}
QMenu {
    background-color: #f6f6f6;
    color: #242424;
}
QMenu::item:selected {
    background: #dcdcdc;
}
"""

MENU_QSS_DARK = """
QMenuBar {
    background-color: #1e1e1e;
    color: #e4e4e4;
}
QMenuBar::item:selected {
    background: #404040;
}
QMenu {
    background-color: #303030;
    color: #efefef;
}
QMenu::item:selected {
    background: #505050;
}
"""
