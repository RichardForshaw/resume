"""MkDocs build hook: fix mkdocs-blogging-plugin's no-git fallback.

mkdocs-blogging-plugin dates a post by: its `date`/`time` front-matter field if set,
otherwise the file's first git-commit date. If git isn't installed, or the build
context has no `.git` directory (both true for our Docker/CodeBuild build image),
the plugin's own fallback is `time.time()` - the moment the build ran. That collapses
every undated post to today's date, destroying ordering.

This patches that specific fallback to use the file's filesystem mtime instead, which
gives a reasonable real date instead of "now". It does not touch the plugin's existing
priority of an explicit front-matter date/time field over git, and does not modify any
content files - it only changes what happens when git history isn't available.
"""
import os
import subprocess
from functools import lru_cache

from mkdocs_blogging_plugin import util as blogging_util


def _get_git_commit_timestamp_with_fs_fallback(self, path, is_first_commit=False):
    realpath = os.path.realpath(path)
    args = ["git", "log", "--format=%at", "--follow"]
    # --diff-filter=A: the commit that added the file (its "first" date); -n 1: latest commit
    args += ["--diff-filter=A"] if is_first_commit else ["-n", "1"]
    args += ["--", realpath]

    try:
        # cwd must be inside the repo so git can find it via realpath alone
        result = subprocess.run(
            args, cwd=os.path.dirname(realpath),
            capture_output=True, text=True, check=True,
        )
        timestamps = result.stdout.split()
        if timestamps:
            # git log lists newest-first; the first commit is the oldest entry
            return int(timestamps[-1] if is_first_commit else timestamps[0])
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        # No repo, git not installed, or file has no history - use mtime, not "now"
        pass

    return int(os.path.getmtime(realpath))


def on_config(config, **kwargs):
    # Patch the class (not an instance) so it applies no matter when/where the
    # plugin constructs its GitUtil - lookup happens at call time, not bind time.
    # Re-wrap in lru_cache since assignment replaces the original cached method.
    blogging_util.Util.get_git_commit_timestamp = lru_cache(maxsize=None)(
        _get_git_commit_timestamp_with_fs_fallback
    )
    return config
