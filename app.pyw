import sys
from PyQt5.QtWidgets import QApplication
from Interface import *
from PyQt5.QtGui import QFont

# Initialize the PyQt application
app = QApplication(sys.argv)

font = QFont()
font.setPointSize(20)  # Set the desired font size here
app.setFont(font)

# Create the main window
window = IokharicApp()

# Show the window
window.show()

# Run the application loop
sys.exit(app.exec_())