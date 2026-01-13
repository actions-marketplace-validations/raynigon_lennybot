import tempfile
import unittest
from pathlib import Path
from test.utils import create_sample_dockerfile, read_file

from lennybot.actions.update_dockerfile import UpdateDockerfileAction
from lennybot.config.config import LennyBotActionConfig


class TestUpdateDockerfileAction(unittest.TestCase):
    def test_constructor_raises_when_target_file_missing(self):
        config = LennyBotActionConfig()
        setattr(config, "_target_file", None)
        setattr(config, "_image", "nginx")
        with self.assertRaises(Exception):
            UpdateDockerfileAction("app", "1.0", "2.0", config)

    def test_run_replaces_from_line_with_default_pattern(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile = Path(tmpdir) / "Dockerfile"
            create_sample_dockerfile(dockerfile, ["nginx:1.2", "redis:3.0"])
            config = LennyBotActionConfig()
            setattr(config, "_target_file", str(dockerfile))
            setattr(config, "_image", "nginx")

            action = UpdateDockerfileAction("app", "1.2", "2.0", config)
            action.run()

            content = read_file(dockerfile)
            self.assertIn("FROM nginx:2.0\n", content)
            self.assertIn("FROM redis:3.0\n", content)

    def test_run_respects_value_pattern(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile = Path(tmpdir) / "Dockerfile"
            create_sample_dockerfile(dockerfile, ["redis:9.9-alpine"])
            config = LennyBotActionConfig()
            setattr(config, "_target_file", str(dockerfile))
            setattr(config, "_image", "redis")
            setattr(config, "_value_pattern", "v{{version}}-alpine")

            action = UpdateDockerfileAction("app", "9.9", "3.4", config)
            action.run()

            content = read_file(dockerfile)
            self.assertIn("FROM redis:v3.4-alpine\n", content)

    def test_run_leaves_file_unchanged_when_image_not_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile = Path(tmpdir) / "Dockerfile"
            create_sample_dockerfile(dockerfile, ["busybox:1.0"])
            config = LennyBotActionConfig()
            setattr(config, "_target_file", str(dockerfile))
            setattr(config, "_image", "nginx")

            action = UpdateDockerfileAction("app", "1.0", "2.0", config)
            action.run()

            content = read_file(dockerfile)
            self.assertIn("FROM busybox:1.0\n", content)
