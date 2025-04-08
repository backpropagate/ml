from omegaconf import OmegaConf

def load_config(config_path: str = "src/conf/config.yaml") -> dict:
    confs = OmegaConf.load(config_path)
    # configs = OmegaConf.to_yaml(conf)
    return confs

if __name__ == "__main__":
    configs = load_config()