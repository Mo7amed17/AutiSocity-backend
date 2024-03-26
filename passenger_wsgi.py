from importlib.machinery import SourceFileLoader
import sys, os
sys.path.append(os.getcwd())

wsgi = SourceFileLoader('wsgi', 'application.py').load_module()

application = wsgi.app