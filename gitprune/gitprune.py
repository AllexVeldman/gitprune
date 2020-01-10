from subprocess import run
from typing import Set
from fire import Fire


def git_prune():
    """Prune the remote branches"""
    run(["git", "fetch", "--prune"])


def get_remote_branches(remote_name: str = "origin") -> Set[str]:
    """Return all remote branches with it's origin stripped"""
    len_ori = len(remote_name + "/")
    remote_branches = run(["git", "branch", "-r"], capture_output=True, text=True).stdout.split("\n")
    return {branch.strip()[len_ori:] for branch in remote_branches if
                       "origin/HEAD" not in branch and branch}


def get_local_branches() -> Set[str]:
    """List all local branches"""
    local_branches = run(["git", "branch"], capture_output=True, text=True).stdout.split("\n")
    return {branch.strip("*").strip() for branch in local_branches if branch}


def get_stale_branches() -> Set[str]:
    """Return all local branches no longer available on the remote"""
    remotes = get_remote_branches()
    locals = get_local_branches()
    return locals - remotes


def delete_branch(branch: str, force: bool):
    """Delete a git branch"""
    if force:
        delete = "-D"
    else:
        delete = "-d"
    run(["git", "branch", delete, branch])


def delete_branches(branches: Set[str], force: bool):
    """Delete a set of branches"""
    [delete_branch(branch, force) for branch in branches]


def prune(force: bool = False):
    """Prune all local and remote branches that are no longer available on the server"""
    git_prune()
    stale_branches = get_stale_branches()
    delete_branches(stale_branches, force=force)


if __name__ == "__main__":
    Fire(prune)