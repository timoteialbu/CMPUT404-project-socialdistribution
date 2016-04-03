import os
from os import remove, close
from tempfile import mkstemp
from shutil import move

import re

if __name__ == '__main__':
	os.system("python manage.py migrate")
	os.system("python manage.py collectstatic")
