'''
This file is part of the domino-detection distribution (https://github.com/jmherzog-de/domino-detection).
Copyright (c) 2021 Adam Mueller and Jean-Marcel Herzog.
  
This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.
 
This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import sys
from PySide6.QtWidgets  import QApplication
from mainwindow         import MainWindow
from os.path            import join, dirname
from dotenv             import load_dotenv

if __name__ == '__main__':
    
    # load environment file
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    app = QApplication()
    w = MainWindow()
    w.show()
    sys.exit(app.exec())