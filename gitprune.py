from subprocess import run
from typing import Set

from fire import Fire  # type: ignore


def git_prune(include_tags: bool = False):
    """Prune the remote branches and tags

    Because for some reason git does not prune removed tags properly, delete all
    local tags and fetch the remotes
    """
    if include_tags:
        tags = run(["git", "tag", "-l"], capture_output=True, text=True).stdout.split(
            "\n"
        )
        for tag in tags:
            if tag:
                run(["git", "tag", "-d", tag])
    run(["git", "fetch", "--prune", "--tags"])


def get_remote_branches(remote_name: str = "origin") -> Set[str]:
    """Return all remote branches with its origin stripped"""
    len_ori = len(remote_name + "/")
    remote_branches = run(
        ["git", "branch", "-r"], capture_output=True, text=True
    ).stdout.split("\n")
    return {
        branch.strip()[len_ori:]
        for branch in remote_branches
        if "origin/HEAD" not in branch and branch
    }


def get_local_branches() -> Set[str]:
    """List all local branches"""
    local_branches = run(
        ["git", "branch"], capture_output=True, text=True
    ).stdout.split("\n")
    return {branch.strip("*").strip() for branch in local_branches if branch}


def get_stale_branches() -> Set[str]:
    """Return all local branches no longer available on the remote"""
    remote_branches = get_remote_branches()
    local_branches = get_local_branches()
    return local_branches - remote_branches


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


def prune(force: bool = False, tags: bool = False):
    """Prune all local and remote branches that are no longer available on the server

    :param force: Delete unmerged branches that no longer exist on the server
    :param tags: Delete and recreate all local tags. Usefull when a tag was moved or
    deleted

    """
    git_prune(include_tags=tags)
    stale_branches = get_stale_branches()
    delete_branches(stale_branches, force=force)


def main():
    Fire(prune)


if __name__ == "__main__":
    main()
