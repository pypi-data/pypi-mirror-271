from kfp import dsl
from kubernetes import client as kubernetes_client


def create_volume_op(volume_size: str, branch: str, remote_url: str):
    """
    Create a volume operation.

    Args:
        volume_size (str): The size of the volume to create.

    Returns:
        dsl.VolumeOp: The volume operation.
    """
    return dsl.VolumeOp(
        name='Create Volume',
        resource_name='data-volume',
        size=volume_size,
        modes=dsl.VOLUME_MODE_RWO,
        annotations={"branch": branch, "remote_url": remote_url}
    )


def create_git_diff_configmap_op(git_diff: str):
    """
    Create a ConfigMap operation.

    Returns:
        dsl.ContainerOp: The ConfigMap operation.
    """

    configmap = kubernetes_client.V1ConfigMap(
        kind="ConfigMap",
        api_version="v1",
        metadata=kubernetes_client.V1ObjectMeta(
            name="{{workflow.name}}-git-diff-config"),
        data={"git_diff": git_diff}
    )

    return dsl.ResourceOp(
        name="Create Git Diff ConfigMap",
        k8s_resource=configmap,
        action="create",
        attribute_outputs={"name": "{.metadata.name}"}
    )


def create_func_configmap_op(func: str):
    """
    Create a ConfigMap operation.

    Returns:
        dsl.ContainerOp: The ConfigMap operation.
    """

    configmap = kubernetes_client.V1ConfigMap(
        kind="ConfigMap",
        api_version="v1",
        metadata=kubernetes_client.V1ObjectMeta(
            name="{{workflow.name}}-func-config"),
        data={"func": func}
    )

    return dsl.ResourceOp(
        name="Create Func ConfigMap",
        k8s_resource=configmap,
        action="create",
        attribute_outputs={"name": "{.metadata.name}"}
    )


def git_clone_op(
    remote_url: str,
    branch: str,
    volume_path: str,
    commit='HEAD'
):
    """
    Clone a Git repository into a specified volume path.

    Args:
        repo_url (str): The URL of the Git repository to clone.
        branch (str): The branch of the Git repository to clone.
        volume_path (str): The path where the repository will be cloned.

    Returns:
        ContainerOp: A ContainerOp object representing the Git clone operation.
    """
    return dsl.ContainerOp(
        name='Clone Git Repository',
        image='alpine/git:2.43.0',
        command=['sh', '-c'],
        arguments=[
            f"""
            if [ -d "{volume_path}/.git" ]; then
                # If repo exists, fetch and reset
                cd {volume_path} && \
                git fetch --all && \
                git reset --hard origin/{branch} && \
                git checkout {commit}
            else
                # If repo doesn't exist, clone it
                git clone --branch {branch} {remote_url} {volume_path}
                cd {volume_path} && \
                git checkout {commit}
            fi
            """
        ]
    )


def create_venv_op(container_image):
    """
    Creates a virtual environment using the python:3.12.3-slim image.

    Returns:
        dsl.ContainerOp: A ContainerOp object representing the operation.
    """
    return dsl.ContainerOp(
        name='Create Virtual Environment',
        image=container_image,
        command=['python', '-m', 'venv', 'venv'],
        container_kwargs={'working_dir': '/app'}
    )


def run_pip_requirements_op(container_image):
    """
    Run a container operation to install requirements using pip.

    Returns:
        dsl.ContainerOp: The container operation to install requirements.
    """
    return dsl.ContainerOp(
        name='Install requirements',
        image=container_image,
        command=['bash', '-c',
                 'source venv/bin/activate && pip install -r requirements.txt'],
        container_kwargs={'working_dir': '/app'}
    )


def run_pip_packages_op(container_image: str, packages: str):
    """
    Run a container operation to install pip packages.

    Args:
        packages (list[str]): A list of pip packages to install.

    Returns:
        dsl.ContainerOp: The container operation to install the specified pip packages.
    """
    return dsl.ContainerOp(
        name='Install packages',
        image=container_image,
        command=['bash', '-c',
                 f'source venv/bin/activate && pip install {packages}'],
        container_kwargs={'working_dir': '/app'}
    )


def apply_git_diff_op(
    branch: str,
    volume_path: str,
    commit='HEAD'
):
    """
    Apply a git diff to the specified branch in a given volume path.

    Args:
        branch (str): The branch to apply the git diff to.
        volume_path (str): The path to the volume where the git repository is located.
        commit (str, optional): The commit to checkout before applying the git diff. Defaults to 'HEAD'.

    Returns:
        kfp.dsl.ContainerOp: A ContainerOp object representing the operation to apply the git diff.
    """

    return dsl.ContainerOp(
        name='Apply git diff',
        image='alpine/git:2.43.0',
        command=['sh', '-c'],
        arguments=[
            f"""
            if [ -d "{volume_path}/.git" ]; then
                # If repo exists, fetch and reset
                cd {volume_path} && \
                git fetch --all && \
                git reset --hard origin/{branch} && \
                git checkout {commit} && \
                cat /tmp/git_diff | base64 -d | gunzip | git apply -
            fi
            """
        ],
        container_kwargs={'working_dir': '/app'},
    )


def run_command_op(container_image: str, command: str, command_args: str = ''):
    """
    Creates a ContainerOp object to run a script inside a container.

    Args:
        command (str): The command to be executed inside the container.
        command_args (str, optional): Additional arguments for the command. Defaults to ''.

    Returns:
        ContainerOp: The ContainerOp object representing the script execution inside a container.
    """
    return dsl.ContainerOp(
        name='Run Command',
        image=container_image,
        command=['bash', '-c', 'source venv/bin/activate && python %s %s' %
                 (command, command_args)],
        container_kwargs={'working_dir': '/app'}
    )

def run_func_op(container_image: str):
    return dsl.ContainerOp(
        name='Run Function',
        image=container_image,
        command=['bash', '-c', 'source venv/bin/activate && cat /tmp/func | base64 -d | gunzip | python -'],
        container_kwargs={'working_dir': '/app'}
    )

@dsl.pipeline(
    name='Simple Task Pipeline',
    description='A simple pipeline that clones a Git repository, creates a virtual environment, runs pip, and executes a script.'
)
def simple_task_pipeline(
    remote_url='https://github.com/your/repo.git',
    branch='main',
    commit='HEAD',
    command='script.py',
    command_args='',
    requirements='',
    packages='',
    volume_size='1Gi',
    gpu_limit: int = 0,
    gpu_vendor='nvidia.com/gpu',
    git_diff='',
    container_image='python:3.12.3-slim'
):
    """
    Creates a simple Kubeflow Pipelines (KFP) pipeline for executing a task.

    Args:
        remote_url (str, optional): The URL of the remote Git repository. Defaults to 'https://github.com/your/repo.git'.
        branch (str, optional): The branch of the Git repository. Defaults to 'main'.
        commit (str, optional): The commit hash or reference of the Git repository. Defaults to 'HEAD'.
        command (str, optional): The command to be executed. Defaults to 'script.py'.
        volume_size (str, optional): The size of the volume to be created. Defaults to '1Gi'.
        requirements (str, optional): The path to the requirements file. Defaults to an empty string.
        packages (str, optional): The packages to be installed. Defaults to an empty string.
        git_diff (str, optional): The diff of the Git repository. Defaults to an empty string.
        set_gpu_limit (int, optional): The GPU limit to be set. Defaults to 0.

    Returns:
        None
    """

    with dsl.Condition(git_diff != ''):
        create_git_diff_configmap = create_git_diff_configmap_op(git_diff)

    create_volume = create_volume_op(volume_size, branch, remote_url)

    git_clone = git_clone_op(
        remote_url=remote_url,
        branch=branch,
        commit=commit,
        volume_path="/app"
    ).add_pvolumes({"/app": create_volume.volume})

    git_clone.after(create_volume)
    if create_git_diff_configmap is not None:
        git_clone.after(create_git_diff_configmap)

    with dsl.Condition(git_diff != ''):
        apply_git_diff = apply_git_diff_op(
            branch=branch,
            commit=commit,
            volume_path="/app"
        ).add_pvolumes(
            {"/app": git_clone.pvolume}).add_volume({
                'name': 'simple-kfp-task-config',
                'configMap': {
                    'name': create_git_diff_configmap.outputs['name']
                }
            }).add_volume_mount(kubernetes_client.V1VolumeMount(
                name='simple-kfp-task-config',
                mount_path='/tmp/git_diff',
                sub_path='git_diff'
            )).after(git_clone)

    create_venv = create_venv_op(container_image).add_pvolumes(
        {"/app": create_volume.volume})

    if apply_git_diff is not None:
        create_venv.after(apply_git_diff)
    else:
        create_venv.after(git_clone)

    with dsl.Condition(requirements != ''):
        run_pip_requirements = run_pip_requirements_op(container_image).add_pvolumes(
            {"/app": create_volume.volume}).after(create_venv)

    with dsl.Condition(packages != ''):
        run_pip_packages = run_pip_packages_op(container_image, packages).add_pvolumes(
            {"/app": create_volume.volume}).after(create_venv)

    with dsl.Condition(command != ''):
        run_command = run_command_op(
            container_image=container_image,
            command='/app/%s' % command,
            command_args=command_args
        ).add_pvolumes({"/app": git_clone.pvolume})

        if run_pip_packages is not None:
            run_command.after(run_pip_packages)
        elif run_pip_requirements is not None:
            run_command.after(run_pip_requirements)
        else:
            run_command.after(create_venv)

        if gpu_limit != 0:
            run_command.add_resource_request(gpu_vendor, gpu_limit)
            run_command.add_resource_limit(gpu_vendor, gpu_limit)
        run_command.execution_options.caching_strategy.max_cache_staleness = "P0D"

    dsl.get_pipeline_conf().set_timeout(3600)
