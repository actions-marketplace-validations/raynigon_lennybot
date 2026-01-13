import tempfile
import unittest
from pathlib import Path
import yaml

from lennybot.actions.update_yaml import UpdateYamlAction
from lennybot.config.config import LennyBotActionConfig
from test.utils import create_yaml_file, read_file


class TestUpdateYamlAction(unittest.TestCase):
    def test_constructor_raises_when_target_file_missing(self):
        config = LennyBotActionConfig()
        config._target_file = None
        config._yaml_path = "spec.imageTag"
        with self.assertRaises(Exception):
            UpdateYamlAction("app", "1.0", "2.0", config)

    def test_constructor_raises_when_yaml_path_missing(self):
        config = LennyBotActionConfig()
        config._target_file = "somefile"
        config._yaml_path = None
        with self.assertRaises(Exception):
            UpdateYamlAction("app", "1.0", "2.0", config)

    def test_run_sets_value_in_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_file = Path(tmpdir) / "file.yaml"
            create_yaml_file(yaml_file, {"spec": {"imageTag": "old"}})

            config = LennyBotActionConfig()
            config._target_file = str(yaml_file)
            config._yaml_path = "spec.imageTag"
            config._value_pattern = "v{{version}}"

            action = UpdateYamlAction("app", "1.0", "3.3.3", config)
            action.run()

            content = yaml.safe_load(read_file(yaml_file))
            # Expect value to be replaced; YAML path syntax may vary depending on yamlpath library
            self.assertEqual(content["spec"]["imageTag"], "v3.3.3")
