import unittest
from pathlib import Path
from update_module_manifest import (
    apply_name_overrides,
    load_name_overrides,
    resolve_module_name,
)


class ModuleNameOverridesTest(unittest.TestCase):
    def test_resolve_module_name_explicit_override(self):
        overrides = {
            "AIO": "mod-aio",
            "wow-mod-bot-lfg-accept": "mod-bot-lfg-accept",
        }
        self.assertEqual(resolve_module_name("AIO", "cpp", overrides), "mod-aio")
        self.assertEqual(resolve_module_name("wow-mod-bot-lfg-accept", "cpp", overrides), "mod-bot-lfg-accept")
        self.assertEqual(resolve_module_name("mod-normal", "cpp", overrides), "mod-normal")

    def test_resolve_module_name_pattern_fallback(self):
        # Even without explicit entry in overrides dict, cpp wow-mod-* should normalize
        self.assertEqual(resolve_module_name("wow-mod-something-new", "cpp", {}), "mod-something-new")
        # Tools or non-cpp should not be normalized by default pattern
        self.assertEqual(resolve_module_name("wow-mod-portal", "tool", {}), "wow-mod-portal")

    def test_apply_name_overrides(self):
        manifest = {
            "modules": [
                {
                    "key": "MODULE_WOW_MOD_BOT_LFG_ACCEPT",
                    "name": "wow-mod-bot-lfg-accept",
                    "repo": "https://github.com/buildthehomelab/wow-mod-bot-lfg-accept.git",
                    "type": "cpp",
                },
                {
                    "key": "MODULE_AIO",
                    "name": "AIO",
                    "repo": "https://github.com/azerothcore/AIO.git",
                    "type": "cpp",
                },
                {
                    "key": "MODULE_MOD_NORMAL",
                    "name": "mod-normal",
                    "repo": "https://github.com/azerothcore/mod-normal.git",
                    "type": "cpp",
                },
            ]
        }
        overrides = {
            "AIO": "mod-aio",
            "wow-mod-bot-lfg-accept": "mod-bot-lfg-accept",
        }
        updated = apply_name_overrides(manifest, overrides)
        self.assertEqual(updated, 2)
        self.assertEqual(manifest["modules"][0]["name"], "mod-bot-lfg-accept")
        self.assertEqual(manifest["modules"][1]["name"], "mod-aio")
        self.assertEqual(manifest["modules"][2]["name"], "mod-normal")

    def test_load_default_overrides(self):
        overrides = load_name_overrides("config/module-name-overrides.json")
        self.assertIn("wow-mod-bot-lfg-accept", overrides)
        self.assertEqual(overrides["wow-mod-bot-lfg-accept"], "mod-bot-lfg-accept")
        self.assertIn("AIO", overrides)
        self.assertEqual(overrides["AIO"], "mod-aio")


if __name__ == "__main__":
    unittest.main()
