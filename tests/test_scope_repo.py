"""Run: python3 -m unittest discover -s tests

--scope repo must gate only on skills whose real path is inside the repo, and
must report everything outside it as excluded rather than dropping it silently.
"""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "ai-context-audit"
loader = importlib.machinery.SourceFileLoader("ai_context_audit", str(SCRIPT))
spec = importlib.util.spec_from_loader("ai_context_audit", loader)
audit = importlib.util.module_from_spec(spec)
loader.exec_module(audit)


class SplitByRepoScopeTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(os.path.realpath(tmp.name))
        self.repo = base / "kirby-skills"
        self.outside = base / "elsewhere"
        self.repo.mkdir()
        self.outside.mkdir()

    def skill(self, parent, name, status="OPTIMAL"):
        d = parent / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text("---\nname: %s\ndescription: test\n---\n" % name)
        return {"name": name, "path": str(d), "status": status}

    def test_repo_skill_is_inside_and_third_party_is_outside(self):
        mine = self.skill(self.repo / "kirby-x", "kirby-x")
        theirs = self.skill(self.outside, "other-skill", status="BLOAT_RISK")
        inside, out = audit.split_by_repo_scope([mine, theirs], self.repo)
        self.assertEqual([e["name"] for e in inside], ["kirby-x"])
        self.assertEqual([e["name"] for e in out], ["other-skill"])

    def test_symlink_from_outside_into_repo_counts_as_inside(self):
        target = self.skill(self.repo / "kirby-y", "kirby-y")
        link = self.outside / "kirby-y"
        os.symlink(target["path"], link)
        entry = {"name": "kirby-y", "path": str(link), "status": "OPTIMAL"}
        inside, out = audit.split_by_repo_scope([entry], self.repo)
        self.assertEqual(len(inside), 1)
        self.assertEqual(out, [])

    def test_symlink_from_repo_out_to_third_party_counts_as_outside(self):
        target = self.skill(self.outside, "other-skill", status="BLOAT_RISK")
        link = self.repo / "linked-other"
        os.symlink(target["path"], link)
        entry = {"name": "linked-other", "path": str(link), "status": "BLOAT_RISK"}
        inside, out = audit.split_by_repo_scope([entry], self.repo)
        self.assertEqual(inside, [])
        self.assertEqual(len(out), 1)

    def test_prefix_lookalike_directory_is_not_inside(self):
        # /x/kirby-skills-other must not match a repo root of /x/kirby-skills.
        lookalike = self.outside / "kirby-skills-other" / "skill"
        lookalike.mkdir(parents=True)
        (lookalike / "SKILL.md").write_text("---\nname: s\ndescription: test\n---\n")
        entry = {"name": "skill", "path": str(lookalike), "status": "OPTIMAL"}
        inside, out = audit.split_by_repo_scope([entry], self.repo)
        self.assertEqual(inside, [])
        self.assertEqual(len(out), 1)

    def test_excluded_bloat_risks_are_counted_separately(self):
        mine = self.skill(self.repo / "kirby-x", "kirby-x")
        theirs = [
            self.skill(self.outside, "big-1", status="BLOAT_RISK"),
            self.skill(self.outside, "big-2", status="BLOAT_RISK"),
            self.skill(self.outside, "fine", status="OPTIMAL"),
        ]
        inside, out = audit.split_by_repo_scope([mine] + theirs, self.repo)
        in_counts = audit.empty_status_counts()
        audit.tally_statuses(inside, in_counts)
        out_counts = audit.empty_status_counts()
        audit.tally_statuses(out, out_counts)
        self.assertEqual(in_counts["bloat_risks"], 0)
        self.assertEqual(out_counts["bloat_risks"], 2)
        self.assertEqual(out_counts["optimal_skills"], 1)


class ScopeRepoCliTest(unittest.TestCase):
    def test_repo_scope_json_lists_only_repo_skills(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--json", "--scope", "repo"],
            capture_output=True, text=True, timeout=300,
        )
        self.assertIn(proc.returncode, (0, 1), proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["scope"], "repo")
        self.assertIn("excluded", report)
        repo_root = os.path.realpath(str(audit.REPO_ROOT))
        for app in report["apps"].values():
            for skill in app.get("skills", []):
                real = os.path.realpath(skill["path"])
                self.assertTrue(
                    real.startswith(repo_root + os.sep),
                    f"out-of-scope skill leaked into repo scope: {skill['path']}",
                )


if __name__ == "__main__":
    unittest.main()
