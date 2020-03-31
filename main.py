#! /usr/bin/env python

import os
import subprocess
from pathlib import Path

import yaml

app = "jupyterhub"

app_dir = Path(app)

with open(app_dir / "meta.yaml") as f:
    app_meta = yaml.safe_load(f)

extra_args = " ".join(f"{k}={v}" for k, v in app_meta["variables"].items())

r = subprocess.run(
    ["ansible-playbook", "--extra-vars", extra_args, app_dir / "install.yaml"],
    env=dict({"ANSIBLE_ROLES_PATH": "roles:~/.ansible/roles"}, **os.environ),
    #stdout=subprocess.PIPE,
    #stderr=subprocess.PIPE,
)

#print(r.stdout.decode())
