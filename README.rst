Cluster in the Cloud app repository
===================================

Install JupyterHub with::

    git clone https://github.com/clusterinthecloud/apps.git
    cd apps
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/python citc-apps/main.py

This will launch JupyterHub at port 8000.
