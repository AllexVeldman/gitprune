"""
All these unittests will run against the repo containing this code

This is because i'm lazy and don't want to spend time creating repos for the unittests
So make sure you checked-in your code!!
"""

from subprocess import run

import gitprune


def test_git_prune(with_tag):
    """Test if git_prune deletes all existing tags

    Tags will be re-populated after a pull
    """
    gitprune.git_prune(include_tags=True)
    tags = run(["git", "tag", "-l"], capture_output=True, text=True).stdout.split("\n")
    assert "unittest_tag" not in tags


def test_get_remote_branches(with_local_branch):
    """Test if locals not in remote are not returned"""
    branches = gitprune.get_remote_branches()
    assert "unittest_branch" not in branches
    assert "main" in branches


def test_get_local_branches(with_local_branch):
    """Test if local branches get returned"""
    branches = gitprune.get_local_branches()
    assert "unittest_branch" in branches
    assert "main" in branches


def test_get_stale_branches(with_local_branch):
    """Test if we get only the local branches"""
    branches = gitprune.get_stale_branches()
    assert "unittest_branch" in branches
    assert "main" not in branches


def test_delete_branch(with_local_branch):
    """Test if we can delete a branch"""
    assert "unittest_branch" in gitprune.get_local_branches()
    gitprune.delete_branch("unittest_branch", force=False)
    assert "unittest_branch" not in gitprune.get_local_branches()


def test_delete_branches(with_local_branch):
    """Test if we can delete a branch"""
    assert "unittest_branch" in gitprune.get_local_branches()
    gitprune.delete_branches({"unittest_branch"}, force=False)
    assert "unittest_branch" not in gitprune.get_local_branches()


def test_force_delete(local_branch_with_changes):
    """Test if we can delete a non-merged local branch"""
    assert "unittest_branch" in gitprune.get_local_branches()
    gitprune.delete_branch("unittest_branch", force=False)
    assert "unittest_branch" in gitprune.get_local_branches()
    gitprune.delete_branch("unittest_branch", force=True)
    assert "unittest_branch" not in gitprune.get_local_branches()


def test_prune(with_local_branch, with_tag):
    """Test the whole flow"""
    gitprune.prune(tags=True)
    assert "unittest_branch" not in gitprune.get_local_branches()
    tags = run(["git", "tag", "-l"], capture_output=True, text=True).stdout.split("\n")
    assert "unittest_tag" not in tags
