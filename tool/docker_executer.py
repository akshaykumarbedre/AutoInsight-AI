
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

def create_docker_cmd_code_excuter():
    return DockerCommandLineCodeExecutor(
    work_dir='tmp',
    timeout=120,
    stop_container = True,
    # Add volume mapping to access your Excel files
    init_command="pip install pandas matplotlib"
)
