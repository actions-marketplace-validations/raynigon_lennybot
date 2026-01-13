import unittest

import yaml


class TestConfigValidation(unittest.TestCase):
    def setUp(self) -> None:
        with open("test/config.yaml", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def test_update_dockerfile_target_contains_image_name(self):
        for app in self.config.get("applications", []):
            for action in app.get("actions", []):
                if action.get("type") != "update-dockerfile":
                    continue
                image = action.get("image")
                target = action.get("targetFile")
                # If image is present and a target file is set, the target file should contain the image base name
                if image is not None and target is not None:
                    image_base = image.split("/")[-1]
                    self.assertIn(
                        image_base,
                        target,
                        f"targetFile '{target}' does not contain image base '{image_base}' for app {app.get('name')}",
                    )

    def test_actions_have_required_keys(self):
        requirements = {
            "update-dockerfile": ["image", "targetFile"],
            "update-image-tag": ["image", "kustomizePath"],
            "update-yaml": ["targetFile", "yamlPath"],
            "update-json": ["targetFile", "jsonPath"],
        }
        for app in self.config.get("applications", []):
            for action in app.get("actions", []):
                a_type = action.get("type")
                if a_type in requirements:
                    for req in requirements[a_type]:
                        self.assertIn(
                            req, action, f"Action {a_type} in app {app.get('name')} missing required key '{req}'"
                        )
