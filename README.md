# Gitprune

A small tool to remove local branches that no longer exist on the origin server.

install:
```commandline
pipx install git+https://github.com/AllexVeldman/gitprune.git
```

```commandline
NAME
    gitprune - Prune all local and remote branches that are no longer available on the server

SYNOPSIS
    gitprune <flags>

DESCRIPTION
    Prune all local and remote branches that are no longer available on the server

FLAGS
    --force=FORCE
        Type: bool
        Default: False
        Delete unmerged branches that no longer exist on the server
    --tags=TAGS
        Type: bool
        Default: False
        Delete and recreate all local tags. Usefull when a tag was moved or deleted
```
