# SPDX-FileCopyrightText: 2019-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences
# SPDX-FileCopyrightText: 2020-2021 Helmholtz-Zentrum Geesthacht GmbH
# SPDX-FileCopyrightText: 2021-2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Command-line options for the backend module."""
from __future__ import annotations

import argparse
import json
import logging
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Type

import yaml

from demessaging.config import (
    LoggingConfig,
    ModuleConfig,
    PulsarConfig,
    WebsocketURLConfig,
)

if TYPE_CHECKING:
    from pydantic import BaseModel

UNKNOWN_TOPIC = "__NOTSET"
UNKNOWN_MODULE = "__NOTSET"


def split_namespace(
    ns: argparse.Namespace,
) -> Tuple[argparse.Namespace, Dict[str, argparse.Namespace]]:
    """Split a namespace into multiple namespaces.

    This utility function takes a namespace and looks for attributes with a
    ``.`` inside. These are then splitted and returned as the second attribute.

    Example
    -------
    Consider the following namespace::

        >>> from argparse import Namespace
        >>> ns = Namespace(**{"main": 1, "sub.main": 2})
        >>> split_namespace(ns)
        (Namespace(main=1), {'sub': Namespace(main=2)})
    """
    main_kws: Dict[str, Any] = {}
    namespace_kws: Dict[str, Dict[str, Any]] = {}
    for key, val in vars(ns).items():
        if "." in key:
            identifier, subkey = key.split(".", 1)
            sub_kws = namespace_kws.setdefault(identifier, {})
            sub_kws[subkey] = val
        else:
            main_kws[key] = val
    namespaces = {
        identifier: argparse.Namespace(**kws)
        for identifier, kws in namespace_kws.items()
    }
    return argparse.Namespace(**main_kws), namespaces


class MessagingArgumentParser(argparse.ArgumentParser):
    """An :class:`argparse.ArgumentParser` for the messaging framework."""

    def parse_known_args(self, args=None, namespace=None):
        ns, remaining_args = super().parse_known_args(args, namespace)
        ns, namespaces = split_namespace(ns)
        if "messaging_config" not in namespaces:
            return ns, remaining_args
        messaging_config = namespaces["messaging_config"]
        wsu_config = namespaces["websocketurl_config"]
        pulsar_config = namespaces["pulsar_config"]
        remaining_messaging_config = (
            wsu_config
            if (
                wsu_config.websocket_url
                or (wsu_config.producer_url and wsu_config.consumer_url)
            )
            else pulsar_config
        )
        ns.messaging_config = dict(
            chain(
                vars(messaging_config).items(),
                vars(remaining_messaging_config).items(),
            )
        )
        return ns, remaining_args


def get_parser(
    module_name: str = "__main__", config: Optional[ModuleConfig] = None
) -> argparse.ArgumentParser:
    """Generate the command line parser."""

    pulsar_config = PulsarConfig(topic=UNKNOWN_TOPIC)
    websocketurl_config = WebsocketURLConfig(topic=UNKNOWN_TOPIC)

    log_config = LoggingConfig()

    if config is None:
        config = ModuleConfig(
            messaging_config=PulsarConfig(topic=UNKNOWN_TOPIC)
        )
    elif isinstance(config.messaging_config, PulsarConfig):
        pulsar_config = config.messaging_config
    elif isinstance(config.messaging_config, WebsocketURLConfig):
        websocketurl_config = config.messaging_config

    conf_dict = config.model_dump()
    messaging_config = config.messaging_config.model_dump()

    parser = MessagingArgumentParser()

    add = parser.add_argument

    connection_group = parser.add_argument_group(
        "Connection options", "General options for the backend module"
    )

    pulsar_group = parser.add_argument_group(
        "Pulsar connection options",
        "Arguments for connecting to a pulsar. This is the default connection "
        "method unless you specify a websocket-url (see below).",
    )

    websocketurl_group = parser.add_argument_group(
        "Websocket URL group",
        "Arguments for connecting to an arbitrary websocket service.",
    )

    logging_group = parser.add_argument_group(
        "Logging Configuration group",
        "Arguments for configuring the logging within DASF.",
    )

    def desc(name, conf: Type[BaseModel] = ModuleConfig, default: Any = None):
        field_info = conf.model_fields[name]
        desc = field_info.description or ""
        if default or field_info.default:
            desc += " Default: %(default)s"
        return desc

    topic_help = desc("topic", PulsarConfig)
    if messaging_config["topic"] == UNKNOWN_TOPIC:
        topic_help += " This option is required!"
    else:
        topic_help += " Default: %(default)s"

    connection_group.add_argument(
        "-t",
        "--topic",
        help=topic_help,
        required=messaging_config["topic"] == UNKNOWN_TOPIC,
        dest="messaging_config.topic",
        default=messaging_config["topic"],
    )

    connection_group.add_argument(
        "--header",
        help=desc("header", PulsarConfig),
        metavar='{"authorization": "Token ..."}',
        dest="messaging_config.header",
        default=messaging_config["header"],
    )

    module_help = "Name of the backend module."
    if module_name == UNKNOWN_MODULE:
        module_help += " This option is required!"
    else:
        module_help += " Default: %(default)s"

    add(
        "-m",
        "--module",
        default=module_name,
        required=module_name == UNKNOWN_MODULE,
        dest="module_name",
        help=module_help,
    )

    add(
        "-d",
        "--description",
        help=desc("doc"),
        default=conf_dict["doc"],
        dest="doc",
    )

    add(
        "--debug",
        help=desc("debug"),
        action="store_true",
    )

    default_host = messaging_config.get("host", pulsar_config.host)
    pulsar_group.add_argument(
        "-H",
        "--host",
        help=desc("host", PulsarConfig, default_host),
        default=default_host,
        dest="pulsar_config.host",
    )

    default_port = messaging_config.get("port", pulsar_config.port)
    pulsar_group.add_argument(
        "-p",
        "--port",
        help=desc("port", PulsarConfig, default_port),
        default=default_port,
        dest="pulsar_config.port",
    )

    default_persistent = messaging_config.get(
        "persistent", pulsar_config.persistent
    )
    pulsar_group.add_argument(
        "--persistent",
        help=desc("persistent", PulsarConfig, default_persistent),
        default=default_persistent,
        dest="pulsar_config.persistent",
    )

    default_tenant = messaging_config.get("tenant", pulsar_config.tenant)
    pulsar_group.add_argument(
        "--tenant",
        help=desc("tenant", PulsarConfig, default_tenant),
        default=default_tenant,
        dest="pulsar_config.tenant",
    )

    default_namespace = messaging_config.get(
        "namespace", pulsar_config.namespace
    )
    pulsar_group.add_argument(
        "--namespace",
        help=desc("namespace", PulsarConfig, default_namespace),
        default=default_namespace,
        dest="pulsar_config.namespace",
    )

    default_max_workers = messaging_config.get(
        "max_workers", pulsar_config.max_workers
    )
    connection_group.add_argument(
        "--max-workers",
        help=desc("max_workers", PulsarConfig, default_max_workers),
        default=default_max_workers,
        type=int,
        dest="messaging_config.max_workers",
    )

    default_queue_size = messaging_config.get(
        "queue_size", pulsar_config.queue_size
    )
    connection_group.add_argument(
        "--queue_size",
        help=desc("queue_size", PulsarConfig, default_queue_size),
        default=default_queue_size,
        type=int,
        dest="messaging_config.queue_size",
    )

    default_max_payload_size = messaging_config.get(
        "max_payload_size", pulsar_config.max_payload_size
    )
    connection_group.add_argument(
        "--max_payload_size",
        help=desc("max_payload_size", PulsarConfig, default_max_payload_size),
        default=default_max_payload_size,
        type=int,
        dest="messaging_config.max_payload_size",
    )

    default_producer_keep_alive = messaging_config.get(
        "producer_keep_alive", pulsar_config.producer_keep_alive
    )
    connection_group.add_argument(
        "--producer-keep-alive",
        help=desc(
            "producer_keep_alive", PulsarConfig, default_producer_keep_alive
        ),
        default=default_producer_keep_alive,
        type=int,
        dest="messaging_config.producer_keep_alive",
    )

    default_producer_connection_timeout = messaging_config.get(
        "producer_connection_timeout",
        pulsar_config.producer_connection_timeout,
    )
    connection_group.add_argument(
        "--producer-connection-timeout",
        help=desc(
            "producer_connection_timeout",
            PulsarConfig,
            default_producer_connection_timeout,
        ),
        default=default_producer_connection_timeout,
        type=int,
        dest="messaging_config.producer_connection_timeout",
    )

    default_websocket_url = messaging_config.get(
        "websocket_url", websocketurl_config.websocket_url
    )
    websocketurl_group.add_argument(
        "--websocket-url",
        help=desc("websocket_url", WebsocketURLConfig, default_websocket_url),
        default=default_websocket_url,
        dest="websocketurl_config.websocket_url",
    )

    websocketurl_group.add_argument(
        "--producer-url",
        help=desc("producer_url", WebsocketURLConfig, default_websocket_url),
        default=default_websocket_url,
        dest="websocketurl_config.producer_url",
    )

    websocketurl_group.add_argument(
        "--consumer-url",
        help=desc("consumer_url", WebsocketURLConfig, default_websocket_url),
        default=default_websocket_url,
        dest="websocketurl_config.consumer_url",
    )

    add(
        "--members",
        help=desc("members"),
        nargs="+",
        metavar="member",
        default=conf_dict["members"],
    )

    # logging config
    logging_group.add_argument(
        "--log-config",
        default=log_config.config_file,
        dest="log_config.config_file",
        type=Path,
        help=desc("config_file", LoggingConfig),
    )

    logging_group.add_argument(
        "--log-level",
        default=log_config.level,
        dest="log_config.level",
        help=desc("level", LoggingConfig),
        type=int,
        choices=[
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ],
    )

    logging_group.add_argument(
        "--log-file",
        default=log_config.logfile,
        type=Path,
        dest="log_config.logfile",
        help=desc("logfile", LoggingConfig),
    )

    logging_group.add_argument(
        "--merge-log-config",
        action="store_true",
        dest="log_config.merge_config",
        help=desc("merge_config", LoggingConfig),
    )

    logging_group.add_argument(
        "--log-overrides",
        dest="log_config.config_overrides",
        type=_load_dict,
        help=(
            "Any valid YAML string, YAML file or JSON file that is merged "
            "into the logging configuration. This option can be used to "
            "quickly override some default logging functionality."
        ),
    )

    # ----------------------------- Subparsers --------------------------------
    subparsers = parser.add_subparsers(dest="command", title="Commands")

    # subparser for testing the connection
    sp = subparsers.add_parser(
        "test-connect",
        help="Connect the backend module to the pulsar message handler.",
    )
    sp.set_defaults(method_name="test_connect")

    # connect subparser (to connect to the pulsar messaging system)
    subparsers.add_parser(
        "listen",
        help="Connect the backend module to the pulsar message handler.",
    )

    # schema subparser (to print the module schema)
    sp = subparsers.add_parser(
        "schema", help="Print the schema for the backend module."
    )
    sp.add_argument("-i", "--indent", help="Indent the JSON dump.", type=int)
    sp.set_defaults(method_name="schema_json", command_params=["indent"])

    # test subparser (to test the connection to the connect to the pulsar
    # messaging system)
    sp = subparsers.add_parser(
        "send-request", help="Test a request via the pulsar messaging system."
    )
    sp.add_argument(
        "request",
        help="A JSON-formatted file with the request.",
        type=argparse.FileType("r"),
    )
    sp.set_defaults(method_name="send_request", command_params=["request"])

    # shell parser. This parser opens a shell to work with the generated Model
    subparsers.add_parser(
        "shell",
        help="Start an IPython shell",
        description=(
            "This command starts an IPython shell where you can access and "
            "work with the generated pydantic Model. This model class is "
            "available via the ``Model`` variable in the shell."
        ),
    )

    # generate parser. This parser renders the backend module and generates a
    # *frontend* API
    sp = subparsers.add_parser(
        "generate",
        help="Generate an API module",
        description=(
            "This command generates an API module that connects to the "
            "backend module via the pulsar and can be used on the client side."
            " We use isort and black to format the generated python file."
        ),
    )

    sp.add_argument(
        "-l",
        "--line-length",
        default=79,
        type=int,
        help=("The line-length for the output API. " "Default: %(default)s"),
    )

    sp.add_argument(
        "--no-formatters",
        action="store_false",
        dest="use_formatters",
        help=(
            "Do not use any formatters (isort, black or autoflake) for the "
            " generated code."
        ),
    )

    sp.add_argument(
        "--no-isort",
        action="store_false",
        dest="use_isort",
        help="Do not use isort for formatting.",
    )

    sp.add_argument(
        "--no-black",
        action="store_false",
        dest="use_black",
        help="Do not use black for formatting.",
    )

    sp.add_argument(
        "--no-autoflake",
        action="store_false",
        dest="use_autoflake",
        help="Do not use autoflake for formatting.",
    )

    sp.set_defaults(
        command_params=[
            "line_length",
            "use_formatters",
            "use_autoflake",
            "use_black",
            "use_isort",
        ]
    )

    return parser


def _load_dict(fname):
    data = yaml.safe_load(fname)
    if isinstance(data, str):  # assume a file and load from disc
        with open(data) as f:
            if data.endswith(".yml") or data.endswith(".yaml"):
                return yaml.safe_load(f)
            elif data.endswith(".json"):
                return json.load(f)
    return data


if __name__ == "__main__":
    parser = get_parser()
    parser.parse_args()
