import tempfile
import unittest
from pathlib import Path
from test.utils import create_kustomization, read_file

import yaml

from lennybot.actions.update_image_tag import UpdateImageTagAction
from lennybot.config.config import LennyBotActionConfig


class TestUpdateImageTagAction(unittest.TestCase):
    def test_constructor_raises_without_kustomize_path(self):
        config = LennyBotActionConfig()
        setattr(config, "_image", "node")
        setattr(config, "_kustomize_path", None)
        with self.assertRaises(Exception):
            UpdateImageTagAction("app", "1.0", "2.0", config)

    def test_run_updates_new_tag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            kustomize_file = Path(tmpdir) / "kustomization.yaml"
            create_kustomization(kustomize_file, [{"name": "node", "newTag": "old"}, {"name": "other", "newTag": "x"}])

            config = LennyBotActionConfig()
            setattr(config, "_image", "node")
            setattr(config, "_kustomize_path", str(kustomize_file))
            setattr(config, "_tag_pattern", "v{{version}}")

            action = UpdateImageTagAction("app", "1.0", "3.2.1", config)
            action.run()

            content = yaml.safe_load(read_file(kustomize_file))
            found = [img for img in content["images"] if img["name"] == "node"][0]
            self.assertEqual(found["newTag"], "v3.2.1")

    def test_run_raises_when_image_not_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            kustomize_file = Path(tmpdir) / "kustomization.yaml"
            create_kustomization(kustomize_file, [{"name": "other", "newTag": "x"}])

            config = LennyBotActionConfig()
            setattr(config, "_image", "node")
            setattr(config, "_kustomize_path", str(kustomize_file))

            action = UpdateImageTagAction("app", "1.0", "3.2.1", config)
            with self.assertRaises(Exception):
                action.run()
