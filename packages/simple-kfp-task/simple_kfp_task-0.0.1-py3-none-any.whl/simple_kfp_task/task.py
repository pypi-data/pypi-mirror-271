from simple_kfp_task.deploykf import create_kfp_client
from simple_kfp_task.git import build_git_diff, get_current_branch, get_current_commit, get_git_root, get_remote_url, is_branch_available_on_remote, is_commit_available_on_remote, is_git_dirty
from typing import Callable
from simple_kfp_task.pipeline import simple_task_pipeline
from simple_kfp_task.utils import encode_string_to_base64, generate_function_code, get_caller_filename
import os

GIT_DIFF_MAX_LENGTH = 10000

def run(
        # kfp
        namespace=None,
        run_name=None,
        experiment_name=None,
        # command
        func: Callable = None,
        command=None,
        command_args=None,
        # git
        remote="origin",
        remote_url=None,
        branch=None,
        commit=None,
        # pip
        requirements=None,
        packages=None,
        # volume
        volume_size="1Gi",
        # container settings
        container_image="python:3.12.3-slim",
        gpu_limit=0,
        gpu_vendor='nvidia.com/gpu',
        # additional
        dry_run=False):

    if os.environ.get('INSIDE_KFP_FUNC_CONTAINER') and not func:
        return func()
    
    if func:
        command = get_caller_filename()

    if command:
        command = get_git_root(command)

    if remote_url is None:
        raise ValueError("Could not determine remote origin")

    if branch:
        branch = branch
    else:
        branch = get_current_branch()

    if not is_branch_available_on_remote(remote=remote, branch=branch):
        raise ValueError(f"Branch is {branch} not available on remote")

    if commit:
        commit = commit
    else:
        commit = get_current_commit()

    git_diff = None
    if not is_commit_available_on_remote(commit) or is_git_dirty():
        git_diff = encode_string_to_base64(build_git_diff())

    if git_diff and len(git_diff) > GIT_DIFF_MAX_LENGTH:
        raise ValueError(f"Git diff is too long {len(git_diff)}. Please commit your changes first.")

    if dry_run is False:
        kfp_client = create_kfp_client(namespace=namespace)
        kfp_client.create_run_from_pipeline_func(
            pipeline_func=simple_task_pipeline,
            experiment_name=experiment_name,
            run_name=run_name,
            arguments={
                # command
                "command": command if command else "",
                "command_args": " ".join(command_args) if command_args else "",
                # git
                "remote_url": remote_url,
                "branch": branch,
                "commit": commit,
                "git_diff": git_diff if git_diff else "",
                # pip
                "requirements": requirements if requirements else "",
                "packages": " ".join(packages) if packages else "",
                # volume
                "volume_size": volume_size,
                # container settings
                "gpu_limit": gpu_limit,
                "gpu_vendor": gpu_vendor,
                "container_image": container_image
            }
        )
