import yaml

# load configuration file
with open("dot_game/etc/server_config.yaml") as f:
    config = yaml.safe_load(f)