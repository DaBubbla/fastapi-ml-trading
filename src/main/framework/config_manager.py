"""
Config retrieval and management.
"""
import os
import json


def find_parent_dir(path: str) -> str:
    parent_directory = os.path.dirname(path)
    return parent_directory


class LocalConfigManager:
    """
    ConfigManger mock that pulls local config files from
    `configs` dir, for testing updates before deploy.
    Overlays ConfigManger configs.
    """
    def __init__(self, stage: str, cfg_mgr: object={}):
        self.config_path = os.path.join(
            find_parent_dir("src"),
            "configs",
            stage
        )

        self.cfg_mgr = cfg_mgr

    def get_configs(self) -> dict:
        """
        Matching get_configs method to ConfigManger class.
        Pulls regular ConfigManager configs, then overlays configs from local.
        """
        # configs = self.cfg_mgr.get_configs()
        configs = {}

        try:
            with open(f"{self.config_path}/common.json", "r") as file:
                configs.update(json.loads(file.read()))
        except (FileNotFoundError, TypeError) as error:
            print(error)

        return configs
    
class ConfigManagerFactory:
    def __init__(self):
        self.run_local = os.getenv("run_local", "false").lower() == "true"
        self.stage = os.getenv('stage', 'dev')
        self.region = os.getenv('region', 'us-east-2')

    def __call__(self):
        # cfg_mgr = ConfigManager(
        #     secret_prefixes=[],
        #     s3_only=[],
        #     secrets_manager_only=[],
        #     config_bucket_prefix="",
        #     runtime=RuntimeArgs(
        #         stage=self.stage,
        #         region_name=self.region
        #     )
        # )
        cfg_mgr = {}

        if self.run_local:
            return LocalConfigManager(self.stage)
    
        return cfg_mgr  
    
APP_CONFIG = ConfigManagerFactory()()


