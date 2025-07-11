# config.py
import yaml


class Config:
    

    @classmethod
    def load_configs(cls, config_path='src/config/config.yaml'):
        
        with open(config_path, 'r', encoding='utf-8') as file:
            static_configs = yaml.safe_load(file)
        return static_configs

STATIC_CONFIGS = Config.load_configs()
