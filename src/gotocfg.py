#!/usr/bin/python
import sys
import argparse
import enum
from gotolib.config import Config
from path import Path

# TODO: Use a format which can be viewed/edited by a human being.
import pickle


class CMDChoices(enum.Enum):
    CD = "prepare-cd"
    SET = "set-path"
    GET = "get-path"
    LIST_PATHS = "list-paths"
    LIST_KEYS = "list-keys"
    REMOVE = "remove-path"

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser()
parser.add_argument("cmd", type=CMDChoices, choices=list(CMDChoices))
parser.add_argument(
    "-k",
    "--key",
    type=str,
)
parser.add_argument(
    "-p",
    "--path",
    type=str,
)
parser.add_argument(
    "params",
    type=str,
    nargs="*",
    default=list(),
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

config_file_path = Path("~/.config/goto-config.pickle").expand()


def load_config() -> Config:
    if not config_file_path.exists():
        return Config()

    with config_file_path.open("rb") as f:
        return pickle.load(f)
    return None


def save_config(cfg: Config):
    with config_file_path.open("wb") as f:
        pickle.dump(cfg, f)
    return None


def set_path():
    cfg = load_config()
    key = args.key
    path = args.path
    cfg.set_path(key, path)
    save_config(cfg)
    return None


def get_path():
    cfg = load_config()
    key = args.key
    params = args.params
    try:
        path = cfg.get_path(key)
    except KeyError:
        print(f"Unknown key {key}", file=sys.stderr)
        return 1

    path = Path(path.format(*params))
    print(path)
    return None


def remove_path():
    cfg = load_config()
    key = args.key
    cfg.remove_path(key)
    save_config(cfg)
    return None


def list_paths():
    cfg = load_config()
    keys = cfg._paths.keys()
    max_key_len = max(len(k) for k in keys)
    for key in sorted(keys):
        print(f"{key:{max_key_len}}: {cfg._paths[key]}")
    return None


def list_keys():
    cfg = load_config()
    keys = list(cfg._paths.keys())
    print(*keys)


def print_cd_path():
    cfg = load_config()
    key = args.key
    params = args.params
    try:
        path = cfg.get_path(key)
    except KeyError:
        print(f"Unknown key {key}", file=sys.stderr)
        return 1

    path = Path(path.format(*params))
    if not path.exists():
        print(f"Path '{path}' does not exist", file=sys.stderr)
        return 1

    print(f'cd "{path}"')


if cmd is CMDChoices.CD:
    err = print_cd_path()
elif cmd is CMDChoices.SET:
    err = set_path()
elif cmd is CMDChoices.GET:
    err = get_path()
elif cmd is CMDChoices.LIST_PATHS:
    err = list_paths()
elif cmd is CMDChoices.LIST_KEYS:
    err = list_keys()
elif cmd is CMDChoices.REMOVE:
    err = remove_path()
else:
    raise NotImplementedError()

exit(err)
