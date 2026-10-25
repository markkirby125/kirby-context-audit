"""Run: python3 -m unittest discover -s tests

audit_directory must skip empty folders and the learned/imported containers,
and must still report real problems (a non-empty folder with no entrypoint,
a dead symlink).
"""
import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "ai-context-audit"
loader = importlib.machinery.SourceFileLoader("ai_context_audit", str(SCRIPT))
spec = importlib.util.spec_from_loader("ai_context_audit", loader)
audit = importlib.util.module_from_spec(spec)
loader.exec_module(audit)


class SkipDirsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def statuses(self):
        return {r["name"]: r["status"] for r in audit.audit_directory(str(self.root))}

    def make_skill(self, name):
        d = self.root / name
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: %s\ndescription: test skill\n---\n# %s\n" % (name, name))

    def test_empty_folder_is_skipped(self):
        (self.root / "empty").mkdir()
        self.assertNotIn("empty", self.statuses())

    def test_learned_and_imported_containers_are_skipped(self):
        for name in ("learned", "imported"):
            (self.root / name / "child").mkdir(parents=True)  # non-empty, no SKILL.md at the root
        got = self.statuses()
        self.assertNotIn("learned", got)
        self.assertNotIn("imported", got)

    def test_non_empty_folder_without_entrypoint_is_still_reported(self):
        d = self.root / "broken-skill"
        d.mkdir()
        (d / "notes.txt").write_text("no entrypoint here")
        self.assertEqual(self.statuses()["broken-skill"], "NO_ENTRYPOINT")

    def test_dead_symlink_is_still_reported(self):
        (self.root / "dead").symlink_to(self.root / "does-not-exist")
        self.assertEqual(self.statuses()["dead"], "BROKEN")

    def test_real_skill_is_still_audited(self):
        self.make_skill("real")
        self.assertEqual(self.statuses()["real"], "OPTIMAL")


if __name__ == "__main__":
    unittest.main()
