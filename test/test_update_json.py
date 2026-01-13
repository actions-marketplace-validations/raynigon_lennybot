import tempfile
import unittest
from pathlib import Path
import json

from lennybot.actions.update_json import UpdateJsonAction
from lennybot.config.config import LennyBotActionConfig
from test.utils import create_json_file, read_file


class TestUpdateJsonAction(unittest.TestCase):
    def test_constructor_raises_when_target_file_missing(self):
        config = LennyBotActionConfig()
        config._target_file = None
        config._json_path = "$.a.b"
        with self.assertRaises(Exception):
            UpdateJsonAction("app", "1.0", "2.0", config)

    def test_constructor_raises_when_json_path_missing(self):
        config = LennyBotActionConfig()
        config._target_file = "somefile"
        config._json_path = None
        with self.assertRaises(Exception):
            UpdateJsonAction("app", "1.0", "2.0", config)

    def test_run_updates_json_value(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            json_file = Path(tmpdir) / "file.json"
            create_json_file(json_file, {"a": {"b": "old"}})

            config = LennyBotActionConfig()
            config._target_file = str(json_file)
            config._json_path = "$.a.b"
            config._value_pattern = "v{{version}}"

            action = UpdateJsonAction("app", "1.0", "3.3.3", config)
            action.run()

            content = json.loads(read_file(json_file))
            self.assertEqual(content["a"]["b"], "v3.3.3")
