from src.scripts import load_data, turn_raw_data
from src.config import load_config

class FeaturePipeline:
    def __init__(self, config: dict):
        self.config = config

    def execute(self):
        self.raw_data = load_data.from_supabase(self.config)
        self.preprocessed_data = turn_raw_data.to_preprocessed_data(self.raw_data, self.config)
        # load_data.to_hopsworks()
        print(raw_data.height)

if __name__ == "__main__":
    import os
    print(os.getcwd())
    config = {}
    instance = FeaturePipeline(config)
    instance.execute()