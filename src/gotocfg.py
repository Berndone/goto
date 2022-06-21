#!/usr/bin/env python3
import sys
import argparse
import enum
from gotolib.config import Config
import path

# TODO: Use a format which can be viewed/edited by a human being.
import pickle


class CMDChoices(enum.Enum):
    CD = "prepare-cd"
    SET = "set-path"
    LIST = "list-paths"

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser()
parser.add_argument(
    "cmd", type=CMDChoices, choices=list(CMDChoices)
)
parser.add_argument(
    "-k", "--key", type=str,
)
parser.add_argument(
    "-p", "--path", type=str,
)

args = parser.parse_args()
# print(args)

cmd = args.cmd
if cmd is CMDChoices.CD:
    if args.key is None:
        parser.error("prepare-cd requires --key")
if cmd is CMDChoices.SET:
    if args.key is None or args.path is None:
        parser.error("prepare-cd requires --key and --path")

config_file_path = path.Path("~/.config/goto-config.pickle").expand()


def load_config() -> Config:
    if not config_file_path.exists():
        return Config()

    with config_file_path.open("rb") as f:
        return pickle.load(f)


def save_config(cfg: Config):
    with config_file_path.open("wb") as f:
        pickle.dump(cfg, f)


def set_path():
    cfg = load_config()
    key = args.key
    path = args.path
    cfg.set_path(key, path)
    save_config(cfg)


def list_keys():
    cfg = load_config()
    print(cfg._paths)


def print_cd_path():
    cfg = load_config()
    key = args.key
    try:
        path = cfg.get_path(key)
    except KeyError:
        print(f"Unknown key {key}", file=sys.stdout)
        return 1

    if not path.exists():
        print(f"Path '{path}' does not exist", file=sys.stdout)
        return 1

    print(f'cd "{path}"')


if cmd is CMDChoices.CD:
    err = print_cd_path()
elif cmd is CMDChoices.SET:
    err = set_path()
elif cmd is CMDChoices.LIST:
    err = list_keys()
else:
    raise NotImplementedError()

exit(err)