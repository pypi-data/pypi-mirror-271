#!/usr/bin/env python3

import os
import argparse
import logging
from pathlib import Path

from iccore import process
from iccore import logging_utils
from iccore import runtime

from iccicd.deploy import PyPiContext, PythonPackage

logger = logging.getLogger(__name__)


def deploy(repo_dir: Path, pypi_ctx: PyPiContext):

    package = PythonPackage(repo_dir)
    package.build()
    package.upload(pypi_ctx)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("action", 
                        help="Action to perform")
    parser.add_argument("--repo_dir",
                        type=Path,
                        default=Path(os.getcwd()),
                        help="Path to the repo to be deployed")
    parser.add_argument("--dry_run",
                        type=bool,
                        default=False,
                        help="Dry run script - don't make real changes")
    parser.add_argument("--pypi_token",
                        type=str,
                        default="",
                        help="Token for uploading packages to PyPI")
    parser.add_argument("--use_test_pypi",
                        type=bool,
                        default=False,
                        help="Use the testpypi repository rather than production")

    args = parser.parse_args()

    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()

    if args.action == "deploy":
        logger.info("Doing deployment")

        pypi_ctx = PyPiContext(args.pypi_token, args.use_test_pypi)

        deploy(args.repo_dir, pypi_ctx)
