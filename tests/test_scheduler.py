import os
import json
import unittest
import tempfile
from unittest.mock import patch
import types
import sys

# Create minimal stubs for external dependencies so ui.py can be imported
_dummy_tk = types.ModuleType('tkinter')
_dummy_tk.messagebox = types.ModuleType('messagebox')
_dummy_tk.simpledialog = types.ModuleType('simpledialog')
_dummy_tk.font = types.ModuleType('font')

sys.modules.setdefault('tkinter', _dummy_tk)

_tkcalendar = types.ModuleType('tkcalendar')
class Calendar:  # dummy Calendar class
    pass
_tkcalendar.Calendar = Calendar
sys.modules.setdefault('tkcalendar', _tkcalendar)

sys.modules.setdefault('pystray', types.ModuleType('pystray'))

_pil = types.ModuleType('PIL')
_pil.Image = types.ModuleType('Image')
_pil.ImageDraw = types.ModuleType('ImageDraw')
sys.modules.setdefault('PIL', _pil)
sys.modules.setdefault('PIL.Image', _pil.Image)
sys.modules.setdefault('PIL.ImageDraw', _pil.ImageDraw)

import ui

class TestSchedulerIO(unittest.TestCase):
    def test_load_missing_file_returns_empty_dict(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'missing.json')
            with patch.object(ui, 'SCHEDULE_FILE', path):
                self.assertEqual(ui.load_schedules(), {})

    def test_save_schedules_writes_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'out.json')
            data = {'2024-01-01': True}
            with patch.object(ui, 'SCHEDULE_FILE', path):
                ui.save_schedules(data)
                with open(path, 'r') as f:
                    loaded = json.load(f)
            self.assertEqual(loaded, data)

if __name__ == '__main__':
    unittest.main()
