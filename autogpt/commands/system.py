"""Commands to control the internal state of the program"""

from __future__ import annotations

COMMAND_CATEGORY = "system"
COMMAND_CATEGORY_TITLE = "System"

from typing import NoReturn
import os
import subprocess
from autogpt.agents.agent import Agent
from autogpt.command_decorator import command
from autogpt.commands.docker_helpers_static import execute_command_in_container, stop_and_remove
from autogpt.logs import logger

@command(
    "goals_accomplished",
    "Goals are accomplished and there is nothing left to do",
    {
        "reason": {
            "type": "string",
            "description": "A summary to the user of how the goals were accomplished",
            "required": True,
        }
    },
)
def task_complete(reason: str, agent: Agent) -> NoReturn:
    """
    A function that takes in a string and exits the program

    Parameters:
        reason (str): A summary to the user of how the goals were accomplished.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """
    project_path = agent.project_path
    workspace = "execution_agent_workspace/"
    files_list = [x[0].lower() for x in agent.written_files]
    #if "coverage_results.txt" not in files_list:
    #    return "You cannot claim goal accomplished without running test cases, measuring coverage and saving them to the file 'coverage_results.txt'"
    if "dockerfile" not in files_list:
        return "You have not created a docker file that creates a docker images and installs the project within that image, installs the dependencies and run tests"
    



    #if not any("coverage" in x for x in files_list):
    #    return "You should write test results into a file called: coverage_results.txt"
    #else:
    #    for file in agent.written_files:
    #        if "coverage" in file[0].lower():
    #            condition1 = "coverage" in file[0].lower()
    #            condition2 = any(x not in files[1].lower() for x in ["Tests run:", "Tests passed:", "Tests failed:", "Tests skipped:"])
    #            if not condition1 and not condition2:
    #                pass
    #            break
    #    else:
    #        if condition1:
    #            return "You have to measure test suite coverage, N/A is not an acceptable value"
    #        elif condition2:
    #            return "The coverage_results file should have the following format:\n"+ """Tests run: [PUT CONCRETE VALUE HERE]
#Tests passed: [PUT CONCRETE VALUE HERE]
#Tests failed: [PUT CONCRETE VALUE HERE]
#Tests skipped: [PUT CONCRETE VALUE HERE]
#Average coverage: [PUT CONCRETE VALUE HERE]
#                    """
    logger.info(title="Shutting down...\n", message=reason)
    if not agent.keep_container:
        stop_and_remove(agent.container)
        os.system("docker system prune -af")
    with open(os.path.join("experimental_setups", agent.exp_number, "saved_contexts", project_path, "SUCCESS"), "w") as ssf:
        ssf.write("SUCCESS")
    quit()


@command(
    "build_image",
    "Build the image to check the Dockerfile",
    {
        "name": {
            "type": "string",
            "description": "The name of the project to build for fuzzing with OSS-Fuzz",
            "required": True,
        }
    },
)
def build_image(name: str, agent: Agent) -> str:
    """
    A function that builds the Dockerfile for OSS-Fuzz
    """
    print("Running now!")
    result = subprocess.run(["python3", "execution_agent_workspace/oss-fuzz/infra/helper.py", "build_image", name, "--no-pull"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result)
    print(result.stdout)
    print(result.stderr)
    print("Successfully run!")
    return result.stdout + result.stderr  

@command(
    "build_fuzzers",
    "Build the image to check the Dockerfile",
    {
        "name": {
            "type": "string",
            "description": "The name of the project to build for fuzzing with OSS-Fuzz",
            "required": True,
        }
    },
)
def build_fuzzers(name: str, agent: Agent) -> str:
    """
    A function that builds the Fuzzers for OSS-Fuzz
    """
    print("Running now!")
    result = subprocess.run(["python3", "execution_agent_workspace/oss-fuzz/infra/helper.py", "build_fuzzers", "--sanitizer", "address", name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result)
    print(result.stdout)
    print(result.stderr)
    print("Successfully run!")
    return result.stdout + result.stderr

@command(
    "check_build",
    "Check if the build went correctly",
    {
        "name": {
            "type": "string",
            "description": "The name of the project to check for the integration with OSS-Fuzz",
            "required": True,
        }
    },
)
def check_build(name: str, agent: Agent) -> str:
    """
    A function that checks the build
    """
    print("Running now!")
    result = subprocess.run(["python3", "execution_agent_workspace/oss-fuzz/infra/helper.py", "check_build", name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result)
    print(result.stdout)
    print(result.stderr)
    print("Successfully run!")
    return result.stdout + result.stderr