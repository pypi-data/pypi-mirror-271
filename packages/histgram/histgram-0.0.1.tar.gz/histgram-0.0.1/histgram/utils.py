import yaml

def load_yaml(path):
    """ Load YAML config file. """
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config