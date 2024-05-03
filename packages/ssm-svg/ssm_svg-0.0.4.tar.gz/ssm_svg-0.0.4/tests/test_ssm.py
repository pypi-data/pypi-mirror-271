import unittest
import subprocess
import os
import shutil
from pathlib import Path
from lxml import etree


SVG_XMLNS = {"xmlns": "http://www.w3.org/2000/svg"}
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ARTIFACT_DIR = f"{TEST_DIR}/artifacts"
SPRITESHEET_NEW = f"{TEST_DIR}/spritesheet_new.svg"
SPRITESHEET_VOID = f"{ARTIFACT_DIR}/spritesheet_void.svg"
SPRITESHEET_ONE_SPRITE = f"{ARTIFACT_DIR}/spritesheet_one_sprite.svg"
SPRITESHEET_TWO_SPRITES = f"{ARTIFACT_DIR}/spritesheet_two_sprites.svg"
SEARCH_SPRITE = f"{TEST_DIR}/search.svg"
MENU_SPRITE = f"{TEST_DIR}/menu.svg"
SEARCH_ID = "search"
MENU_ID = "menu"


class TestSsm(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(ARTIFACT_DIR):
            os.makedirs(ARTIFACT_DIR)
        shutil.copy(f"{TEST_DIR}/spritesheet_void.svg",
                    SPRITESHEET_VOID)
        shutil.copy(f"{TEST_DIR}/spritesheet_one_sprite.svg",
                    SPRITESHEET_ONE_SPRITE)
        shutil.copy(f"{TEST_DIR}/spritesheet_two_sprites.svg",
                    SPRITESHEET_TWO_SPRITES)

    def tearDown(self):
        shutil.rmtree(ARTIFACT_DIR)
        if os.path.exists(SPRITESHEET_NEW):
            os.remove(SPRITESHEET_NEW)

    def test_create(self):
        self.assertTrue(subprocess.run(["python",
                                        "-m",
                                        "ssm",
                                        "create",
                                        "-f",
                                        f"{SPRITESHEET_NEW}",
                                        f"{SEARCH_SPRITE}"]).returncode == 0,
                        "Failed to create spritesheet.")

        tree = etree.parse(SPRITESHEET_NEW)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:defs/xmlns:symbol[@id='search']", # noqa
                                        namespaces=SVG_XMLNS)), 1,
                         "Malformed spritesheet.")

    def test_list(self):
        completed_process = subprocess.run(["python",
                                            "-m",
                                            "ssm",
                                            "list",
                                            "-f",
                                            f"{SPRITESHEET_TWO_SPRITES}"],
                                           capture_output=True)
        self.assertListEqual(completed_process.stdout.decode().split("\n"),
                             ["menu", "search", ""],
                             "Failed to list IDs in spritesheet.")

    def test_add(self):
        tree = etree.parse(SPRITESHEET_VOID)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:defs/xmlns:symbol[@id='menu']", # noqa
                                        namespaces=SVG_XMLNS)), 0,
                         "Malformed spritesheet.")

        self.assertTrue(subprocess.run(["python",
                                        "-m",
                                        "ssm",
                                        "add",
                                        "-f",
                                        f"{SPRITESHEET_VOID}",
                                        f"{MENU_SPRITE}"]).returncode == 0,
                        "Failed to add sprite to spritesheet.")

        tree = etree.parse(SPRITESHEET_VOID)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:defs/xmlns:symbol[@id='menu']",  # noqa
                                        namespaces=SVG_XMLNS)), 1,
                         "Malformed spritesheet.")

    def test_remove(self):
        tree = etree.parse(SPRITESHEET_ONE_SPRITE)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:defs/xmlns:symbol[@id='menu']",  # noqa
                                        namespaces=SVG_XMLNS)), 1,
                         "Malformed spritesheet.")

        self.assertTrue(subprocess.run(["python",
                                        "-m",
                                        "ssm",
                                        "remove",
                                        "-f",
                                        f"{SPRITESHEET_ONE_SPRITE}",
                                        f"{MENU_ID}"]).returncode == 0,
                        "Failed to remove sprite from spritesheet.")

        tree = etree.parse(SPRITESHEET_ONE_SPRITE)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:defs/xmlns:symbol[@id='menu']",  # noqa
                                        namespaces=SVG_XMLNS)), 0,
                         "Malformed spritesheet.")

    def test_export(self):
        completed_process = subprocess.run(["python",
                                            "-m",
                                            "ssm",
                                            "export",
                                            "-f",
                                            f"{SPRITESHEET_TWO_SPRITES}",
                                            f"{SEARCH_ID}",
                                            "/dev/null"],
                                           capture_output=True)
        self.assertTrue(completed_process.returncode == 0,
                        "Failed to export sprite from spritesheet.")
        tree = etree.fromstring(completed_process.stdout)
        self.assertEqual(len(tree.xpath("/xmlns:svg/xmlns:path",
                                        namespaces=SVG_XMLNS)), 1,
                         "Malformed spritesheet.")

    def test_export_with_use(self):
        completed_process = subprocess.run(["python",
                                            "-m",
                                            "ssm",
                                            "export",
                                            "-f",
                                            f"{SPRITESHEET_TWO_SPRITES}",
                                            f"{SEARCH_ID}",
                                            "--use"],
                                           capture_output=True)
        self.assertTrue(completed_process.returncode == 0,
                        "Failed to export sprite from spritesheet.")
        tree = etree.fromstring(completed_process.stdout)
        self.assertEqual(len(tree.xpath(f"/svg/use[@href='{Path(SPRITESHEET_TWO_SPRITES).name}#{SEARCH_ID}']")), 1,  # noqa
                         "Malformed spritesheet.")


if __name__ == '__main__':
    unittest.main()
