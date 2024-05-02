from os.path import join, dirname
from jtd_codebuild.config.project.model import ProjectConfig
from jtd_codebuild.utils.io import write_json

if __name__ == "__main__":
    write_json(
        join(dirname(__file__), "..", "config.json"),
        ProjectConfig.model_json_schema(),
    )
