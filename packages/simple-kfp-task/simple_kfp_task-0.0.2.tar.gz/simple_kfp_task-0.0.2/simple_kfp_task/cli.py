#!/usr/bin/env python
from simple_kfp_task.task import run
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('command')
    # kfp
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--experiment-name")
    parser.add_argument("--run-name")
    # git
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--remote-url")
    parser.add_argument("--branch")
    parser.add_argument("--commit")
    parser.add_argument("--ignore-ssh-error")
    # pip
    parser.add_argument("--requirements")
    parser.add_argument("--packages", nargs='+', default=[])
    parser.add_argument("--volume-size", default="1Gi")
    # container
    parser.add_argument("--gpu-limit", default=0)
    parser.add_argument("--gpu-vendor", default="nvidia.com/gpu")
    parser.add_argument("--container-image", default="python:3.12.3-slim")

    args, command_args = parser.parse_known_args()

    run(
        # kfp
        run_name=args.run_name,
        experiment_name=args.experiment_name,
        namespace=args.namespace,
        # command
        command=args.command,
        command_args=command_args,
        # git
        remote=args.remote,
        remote_url=args.remote_url,
        branch=args.branch,
        commit=args.commit,
        # pip
        requirements=args.requirements,
        packages=args.packages,
        # volume
        volume_size=args.volume_size,
        # container
        gpu_limit=args.gpu_limit,
        gpu_vendor=args.gpu_vendor,
        container_image=args.container_image,
    )
