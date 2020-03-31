#! /usr/bin/env python

import os
import subprocess
from pathlib import Path
from typing import List

import yaml

APPS_ROOT_DIR = Path(__file__).resolve().parent


def list_apps() -> List[str]:
    subdirs = (x for x in APPS_ROOT_DIR.iterdir() if x.is_dir())
    apps_dirs = (s for s in subdirs if (s / "meta.yaml").exists())
    return [a.name for a in apps_dirs]


def install(app: str, **user_variables):
    app_dir = APPS_ROOT_DIR / app

    with open(app_dir / "meta.yaml") as f:
        app_meta = yaml.safe_load(f)

    print(f"Installing {app_meta['name']}")

    variables = {k: v["default"] for k, v in app_meta["variables"].items()}  # Set the defaults

    for var_name, var_value in user_variables.items():
        if var_name not in app_meta["variables"]:
            raise NameError(f"Unrecognised variable '{var_name}' for app '{app}'")
        variables[var_name] = var_value  # Overwrite the default with the user-supplied value

    mapped_variables = {app_meta["variables"][k]["ansible_var"]: v for k, v in variables.items()}

    extra_args = " ".join(f"{k}={v}" for k, v in mapped_variables.items())

    subprocess.run(
        ["ansible-galaxy", "install", "-r", app_dir / "requirements.yml"],
        cwd=APPS_ROOT_DIR,
        check=True
    )

    r = subprocess.run(
        ["ansible-playbook", "--extra-vars", extra_args, app_dir / "install.yaml"],
        env=dict({"ANSIBLE_ROLES_PATH": "roles:~/.ansible/roles"}, **os.environ),
        cwd=APPS_ROOT_DIR,
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
    )

    #print(r.stdout.decode())


if __name__ == "__main__":
    install("jupyterhub")
