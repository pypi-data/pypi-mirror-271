import os
import numpy as np


def calculate_stats(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    return mean, std_dev


def hello_world():
    return "Hello, World!"


def get_environment_variables():
    return os.environ


if __name__ == "__main__":
    print(hello_world())
    env_vars = get_environment_variables()
    for key, value in env_vars.items():
        print(f"{key}: {value}")
