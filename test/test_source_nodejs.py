import unittest
from unittest.mock import patch, MagicMock

from lennybot.config.config import LennyBotSourceConfig
from lennybot.service.source.source_nodejs import NodeJSVersionSource


class TestParseImage(unittest.TestCase):

    def setUp(self) -> None:
        self.config = LennyBotSourceConfig()

    @patch("lennybot.service.source.source_nodejs.requests.get")
    def test_lts_only_false(self, mock_get):
        # returns first release when lts_only is False
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = [
            {"version": "v25.0.0", "lts": False},
            {"version": "v24.13.0", "lts": "Gallium"},
        ]
        mock_get.return_value = mock_resp

        self.config.lts_only = False
        release = NodeJSVersionSource("test-node-version", self.config)
        version = release.latest_version()

        self.assertEqual(version, "25.0.0")

    @patch("lennybot.service.source.source_nodejs.requests.get")
    def test_lts_only_true(self, mock_get):
        # returns first LTS release when lts_only is True
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = [
            {"version": "v25.0.0", "lts": False},
            {"version": "v24.13.0", "lts": "Gallium"},
        ]
        mock_get.return_value = mock_resp

        self.config.lts_only = True
        lts_release = NodeJSVersionSource("test-node-version", self.config)
        version = lts_release.latest_version()

        self.assertEqual(version, "24.13.0")
