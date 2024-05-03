################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R, 5737-L65
# (c) Copyright IBM Corp. 2019-2024. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

import logging.config

from autoai_libs.version import __version__

logging_cfg = {
    "version": 1,
    "formatters": {},
    "filters": {},
    "handlers": {},
    "loggers": {
        "autoai_libs": {"propagate": False},  # top-level library logger
    },
    "disable_existing_loggers": False,
}

logging.config.dictConfig(logging_cfg)
