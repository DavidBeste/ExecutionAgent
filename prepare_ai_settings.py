import argparse

template=\
"""ai_goals:
- Given the two files Dockerfile and build.sh for installing a project, set up the OSS-Fuzz integration MANUALLY inside the Docker environment. Make sure to add all necessary dependencies to successfully compile the fuzzer. It is important to do this manually first, to be able to interactively fix potential bugs. Do not attempt to build the build.sh and Dockerfile and in zero-shot setting, first confirm that it works in the testing environment. When successful, write a new Dockerfile for an oss-fuzz integration. After that, install the project with support for OSS-fuzz.
- target_project_link: https://libtiff.gitlab.io/libtiff/
- target_project: libtiff
ai_name: OSSFuzzingAgent
ai_role: |
  A specialized AI assistant for automating the fuzzing of a project using OSS-Fuzz.
api_budget: 0.0
"""

settings = template

with open("ai_settings.yaml", "w") as set_yaml:
    set_yaml.write(settings)
