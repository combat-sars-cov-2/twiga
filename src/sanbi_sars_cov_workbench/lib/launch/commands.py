from __future__ import annotations

from pathlib import Path

import click

from loguru import logger
from src.sanbi_sars_cov_workbench.lib.shared.galaxy import launch as galaxy_launch
from src.sanbi_sars_cov_workbench.lib.shared.irida import launch as irida_launch
from src.sanbi_sars_cov_workbench.lib.utils.helpers.misc import read_config_file
from src.sanbi_sars_cov_workbench.lib.utils.helpers.ssh import SshBasic, SshKeyBase
from src.sanbi_sars_cov_workbench.lib.utils.services.galaxy import factory as galaxy_factory
from src.sanbi_sars_cov_workbench.lib.utils.services.irida import factory as irida_factory

CONFIG_DEFAULTS = {"file": f"{Path.home()}/.okapi.yaml"}

#
# def launch_all(cfg, ssh_session):
#     """
#     Using
#     :return:
#     """
#     cmd = f"cd {cfg['root_path']};"
#     cmd += (
#         "docker-compose -f docker-compose.yml -f docker-compose.singularity.yml -f docker-compose.irida_workbench.yml -f "
#         "docker-compose.irida_ssl.yml up -d "
#     )
#     ssh_session.exec(cmd)
#
#
# def shut_all(cfg, ssh_session):
#     """
#     Using
#     :return:
#     """
#     cmd = f"cd {cfg['root_path']};"
#     cmd += (
#         "docker-compose -f docker-compose.yml -f docker-compose.singularity.yml -f docker-compose.irida_workbench.yml -f "
#         "docker-compose.irida_ssl.yml down "
#     )
#     ssh_session.exec(cmd)
#

FUNC_MAP = {"irida": irida_launch, "galaxy": galaxy_launch}


@click.command()
@click.option(
    "-c",
    "--conf",
    type=click.Path(exists=True),
    help=f"Location of the client config files (default={Path.home()}/.okapi.yaml)",
)
@click.argument(
    "instance", type=click.Choice(["irida", "galaxy"]), required=True
)
def launch(instance, conf):
    """
    Launch a service of the sanbi_sars_cov_workbench
    \f
    """
    cfg = read_config_file(conf) if conf else read_config_file(CONFIG_DEFAULTS["file"])
    func = FUNC_MAP[instance]
    import pdb
    pdb.set_trace()
    ssh_session = (
        SshBasic(cfg[instance])
        if cfg["auth"]["basic_auth"]
        else SshKeyBase(cfg[instance])
    )

    func(cfg[instance], ssh_session)