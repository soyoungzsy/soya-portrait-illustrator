import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_pose_library_exists_and_is_linked_from_skill(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        pose_path = ROOT / "references" / "pose-library.md"
        self.assertTrue(pose_path.is_file(), "missing references/pose-library.md")
        self.assertIn("references/pose-library.md", skill)

        pose = pose_path.read_text(encoding="utf-8")
        for required in (
            "neutral-relaxed",
            "friendly-wave",
            "walking",
            "thinking",
            "working",
            "presenting",
            "reading",
            "clasped hands",
            "hands behind the back",
            "pigeon-toed",
        ):
            self.assertIn(required, pose)

    def test_anime_style_has_light_beautification_boundary(self) -> None:
        anime = (ROOT / "references" / "anime-bean-eye.md").read_text(encoding="utf-8")
        self.assertIn("approximately 80%", anime)
        self.assertIn("lightly beautified", anime)
        self.assertIn("not reproduce exact photographic facial proportions", anime)
        self.assertIn("cute, modest, non-sexualized silhouette", anime)
        self.assertIn("no exaggerated bust, waist, or hip curves", anime)


if __name__ == "__main__":
    unittest.main()
