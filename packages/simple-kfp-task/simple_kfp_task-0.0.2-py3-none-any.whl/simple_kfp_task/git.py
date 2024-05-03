from git import Repo
import os
import sys

try:
    repo = Repo('.', search_parent_directories=True)
except:
    print(f"{os.getcwd()} is not a Git repository.")
    sys.exit(1)


def get_remote_url(remote='origin'):
    """
    Get the URL of the remote Git origin.

    Returns:
        str: The URL of the remote Git origin.
        None: If the Git origin URL cannot be retrieved.
    """
    try:
        git_origin = repo.remotes[remote].url
        return git_origin
    except:
        return None


def is_git_dirty():
    """
    Checks if the current Git repository is dirty.

    Returns:
        bool: True if the repository is dirty, False otherwise.
    """
    try:
        return repo.is_dirty()
    except:
        return False


def get_current_branch():
    """
    Get the name of the current branch in the Git repository.

    Returns:
        str: The name of the current branch.
        None: If the current branch cannot be determined.
    """
    try:
        return repo.active_branch.name
    except:
        return None


def get_current_commit():
    """
    Get the hash of the current commit in the Git repository.

    Returns:
        str: The hash of the current commit.
        None: If the current commit cannot be determined.
    """
    try:
        return repo.head.commit.hexsha
    except:
        return None


def get_last_commit_on_remote(remote='origin'):
    """
    Get the hash of the last commit on the remote.

    Args:
        remote (str): The name of the remote. Default is 'origin'.

    Returns:
        str: The hash of the last commit on the remote.
        None: If the last commit on the remote cannot be determined.
    """
    try:
        remote_branch = repo.remotes[remote].refs[repo.active_branch.name]
        last_commit = remote_branch.commit.hexsha
        return last_commit
    except:
        return None


def build_git_diff(commit=None):
    """
    Build the git diff to the last committed remote commit.

    Returns:
        str: The git diff.
        None: If the git diff cannot be built.
    """
    try:
        remote_branch = repo.remotes.origin.refs[repo.active_branch.name]
        diff = repo.git.diff(commit if commit else remote_branch.commit)
        return diff
    except Exception as e:
        return None


def is_branch_available_on_remote(remote='origin', branch=None):
    """
    Check if the current branch is available on a remote.

    Returns:
        bool: True if the branch is available on a remote, False otherwise.
    """
    try:
        if branch is None:
            current_branch = repo.active_branch
        else:
            current_branch = repo.branches[branch]
        remote_branches = repo.remotes[remote].refs
        return current_branch.name in remote_branches
    except:
        return False


def is_commit_available_on_remote(commit):
    """
    Check if a specific commit is available on the remote.

    Args:
        commit (str): The hash of the commit to check.

    Returns:
        bool: True if the commit is available on the remote, False otherwise.
    """
    try:
        remote_branches = repo.remotes.origin.refs
        for branch in remote_branches:
            if commit in repo.git.rev_list(branch):
                return True
        return False
    except:
        return False


def get_git_root(path):
    """
    Get the relative path to the root folder of the Git repository.

    Args:
        path (str): The path to a file or directory within the Git repository.

    Returns:
        str: The relative path to the root folder of the Git repository.
        None: If the Git root folder cannot be found.
    """
    try:
        git_root = repo.git.rev_parse("--show-toplevel")
        relative_path = os.path.relpath(path, git_root)
        return relative_path
    except:
        return None
