"""
utils for app
"""
import os
import tempfile
from PIL import Image


class TempImageFile:
    """
    Temporary image file
    """
    def __init__(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(tmp_file.name)
        tmp_file.close()
        self.file_name = tmp_file.name
        self.file = open(self.file_name, "rb")

    def __del__(self):
        if self.file:
            self.file.close()
            os.unlink(self.file_name)
