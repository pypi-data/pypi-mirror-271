from cli_ui import debug as verbose

from gitlabform.gitlab import GitLab
from gitlabform.gitlab.core import NotFoundException, UnexpectedResponseException
from gitlabform.processors.abstract_processor import AbstractProcessor


class ResourceGroupsProcessor(AbstractProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__("resource_groups", gitlab)

    def _process_configuration(self, project_and_group: str, configuration: dict):
        for config_resource_group_name in configuration["resource_groups"]:
            config_process_mode = configuration["resource_groups"][
                config_resource_group_name
            ]["process_mode"]

            try:
                gitlab_resource_group = self.gitlab.get_specific_resource_group(
                    project_and_group, config_resource_group_name
                )
            except NotFoundException:
                raise Exception(
                    f"Project is not configured to use resource group: {config_resource_group_name}.\n"
                    f"Add the resource group in your project's .gitlab-ci.yml file.\n"
                    f"For more information, visit https://docs.gitlab.com/ee/ci/resource_groups/#add-a-resource-group.",
                )

            # compare the resource group process mode between the config entity and gitlab entity
            if config_process_mode != gitlab_resource_group["process_mode"]:
                try:
                    self.gitlab.update_resource_group(
                        project_and_group,
                        config_resource_group_name,
                        {"process_mode": config_process_mode},
                    )
                except UnexpectedResponseException:
                    raise Exception(
                        f"process_mode does not have a valid value: {config_process_mode}"
                    )
                verbose(f"Setting resource group process mode to {config_process_mode}")
