import os
import platform

import logging.config

import loguru

from .const import *


def get_variable(key=None, default=None):
    if key != None and isinstance(key, str):
        if os.environ.get(key, None):
            return os.environ.get(key, None)
        else:
            return key
    elif default != None and isinstance(default, str):
        return default
    else:
        return None


def get_logger(
    log_path: str, log_file: str, log_target: dict, log_level={}, **log_config
):
    """
    log_target: 是否启用不同的数据源
    不同数据源会使用对应的数据驱动
    代号可见如下：
    * local
    * aliyun
    * aws
    """
    if (
        log_target.get("aliyun", True)
        or log_target.get("aws", True)
        or log_target.get("webhook", True)
    ):
        logging_config = {
            "version": 1,
            "formatters": {
                "rawformatter": {
                    "class": "logging.Formatter",
                    "format": "%(message)s",
                }
            },
            "handlers": {
                "aliyun_sls_python_sdk": {
                    "()": "aliyun.log.QueuedLogHandler",
                    "level": log_level.get("aliyun", "INFO"),
                    "formatter": "rawformatter",
                    "end_point": get_variable(
                        key=log_config.get("LOG_CONFIG_ALIYUN_ENDPOINT", None),
                        default=LOG_CONFIG_ALIYUN_ENDPOINT,
                    ),
                    "access_key_id": get_variable(
                        key="ALIYUN_ACCESSKEY_ID",
                        default=LOG_CONFIG_ALIYUN_ACCESSKEY_ID,
                    ),
                    "access_key": get_variable(
                        key="ALIYUN_ACCESSKEY_SECRET",
                        default=LOG_CONFIG_ALIYUN_ACCESSKEY_SECRET,
                    ),
                    "project": get_variable(
                        key=log_config.get("LOG_CONFIG_ALIYUN_PROJECT", None),
                        default=LOG_CONFIG_ALIYUN_PROJECT,
                    ),
                    "log_store": get_variable(
                        key=log_config.get("LOG_CONFIG_ALIYUN_LOGSTORE", None),
                        default=LOG_CONFIG_ALIYUN_LOGSTORE,
                    ),
                }
            },
            "loggers": {
                "aliyun_sls": {
                    "handlers": [
                        "aliyun_sls_python_sdk",
                    ],
                    "level": log_level.get("aliyun", "INFO"),
                    "propagate": False,
                }
            },
        }
        logging.config.dictConfig(logging_config)
        logging_handler_aliyun = logging.getLogger("aliyun_sls").handlers[0]

    loguru_config = {}
    loguru_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
    logger = loguru.logger

    # for pytest project may need to record logs write by framework
    # pytest-loguru

    if log_path == None or isinstance(log_path, str) == False:
        log_path = LOG_PATH

    # local_file
    logger.add(
        sink=os.path.join(log_path, log_file),
        format=loguru_format,
        level="TRACE",
        **loguru_config,
    )
    # saas_aliyun_sls
    if log_target.get("aliyun", True):
        logger.add(
            sink=logging_handler_aliyun,
            format=loguru_format,
            level=log_level.get("aliyun", "INFO"),
            **loguru_config,
        )
    # saas_aws_cloudwatch
    # logger.add(sink=logging_handler_aws) # WIP
    # db_clickhouse
    # logger.add(sink=logging_handler_clickhouse) # WIP
    # db_elasticsearch
    # logger.add(sink=logging_handler_elasticsearch) # WIP
    # protocal_syslog
    # logger.add(sink=logging_handler_syslog) # WIP
    # protocal_webhook
    # logger.add(sink=logging_handler_webhook) # WIP

    def get_plain_dict(
        logger_status_name: str, logger_status_dict: dict
    ) -> str:
        plain_dict = []
        for key, value in logger_status_dict.items():
            plain_dict.append(f"{logger_status_name}.{key}: {value}")
        return "\n".join(plain_dict)

    def get_platform() -> None:
        result = {}
        try:
            result["system"] = platform.system()
            result["architecture"] = platform.architecture()
            result["machine"] = platform.machine()
            result["node"] = platform.node()
            result["platform"] = platform.platform()
            result["processor"] = platform.processor()
            result["python_implementation"] = platform.python_implementation()
            result["python_version"] = platform.python_version()
            result["python_build"] = platform.python_build()
            result["python_compiler"] = platform.python_compiler()

        except Exception:
            result["warning"] = "Failed to fetch"
        return result

    fence_length = 30
    logger.success(
        "\n"
        + ("=" * fence_length + "\n")
        + (f"[Hellologger {HELLOLOGGER_VERSION}] logger enabled" + "\n")
        + ("=" * fence_length + "\n")
        + (f"platform.platform: {platform.platform()}" + "\n")
        + (
            f"platform.python_implementation: {platform.python_implementation()}"
            + "\n"
        )
        + (f"platform.python_version: {platform.python_version()}" + "\n")
        + (get_plain_dict("log_target", log_target) + "\n")
        + (get_plain_dict("log_level", log_level) + "\n")
        + (get_plain_dict("log_config", log_config) + "\n")
        + ("=" * fence_length + "\n")
    )
    logger.trace(
        "\n"
        + (get_plain_dict("platform", get_platform()) + "\n")
        + ("=" * fence_length + "\n")
    )
    return logger


def main():
    print("Sorry, this package is not intended to run directly.")


if __name__ == "__main__":
    main()
