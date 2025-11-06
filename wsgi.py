import sys
path = '/home/TU_USERNAME/subasta'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

# Opcional: logging
import logging
logging.basicConfig(stream=sys.stderr)