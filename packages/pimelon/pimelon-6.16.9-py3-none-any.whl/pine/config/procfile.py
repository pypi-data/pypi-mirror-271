import os
import platform

import click

import pine
from pine.app import use_rq
from pine.pine import Pine
from pine.utils import which


def setup_procfile(pine_path, yes=False, skip_redis=False):
	config = Pine(pine_path).conf
	procfile_path = os.path.join(pine_path, "Procfile")

	is_mac = platform.system() == "Darwin"
	if not yes and os.path.exists(procfile_path):
		click.confirm(
			"A Procfile already exists and this will overwrite it. Do you want to continue?",
			abort=True,
		)

	procfile = (
		pine.config.env()
		.get_template("Procfile")
		.render(
			node=which("node") or which("nodejs"),
			use_rq=use_rq(pine_path),
			webserver_port=config.get("webserver_port"),
			CI=os.environ.get("CI"),
			skip_redis=skip_redis,
			workers=config.get("workers", {}),
			is_mac=is_mac,
		)
	)

	with open(procfile_path, "w") as f:
		f.write(procfile)
