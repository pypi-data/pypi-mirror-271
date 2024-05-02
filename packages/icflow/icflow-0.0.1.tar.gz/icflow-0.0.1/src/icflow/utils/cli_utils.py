import os
from pathlib import Path
import argparse


def get_default_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str, default="train")
    parser.add_argument("--settings", type=str)
    parser.add_argument("--num_epochs", type=int, default=0)
    parser.add_argument("--dataset_cache", type=Path, default=os.getcwd())
    parser.add_argument("--result_dir", type=Path, default=os.getcwd())
    return parser
