import pytest
from subprocess import run


@pytest.fixture
def with_tag():
    """Create a tag and remove it when the test is done"""
    run(["git", "tag", "-a", "unittest_tag", "-m", "If i'm still here, remove me.."])
    yield
    run(["git", "tag", "-d", "unittest_tag"], check=False)


@pytest.fixture
def with_local_branch():
    """Create a branch and remove it when the test is done"""
    run(["git", "branch", "unittest_branch"])
    yield
    run(["git", "branch", "-d", "unittest_branch"], check=False)


@pytest.fixture
def local_branch_with_changes(with_local_branch):
    """Create a local branch with a change so we can test the force option"""
    run(["git", "checkout", "unittest_branch"])
    run(["git", "commit", "--allow-empty", "-m", "empty unittest commit"])
    run(["git", "checkout", "master"])
    yield
    run(["git", "branch", "-D", "unittest_branch"], check=False)
