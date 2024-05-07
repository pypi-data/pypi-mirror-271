import logging
import pathlib
import json


def set_system(system: str):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.system = system
        return record

    logging.setLogRecordFactory(record_factory)


def set_group(group: str):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.group = group
        return record

    logging.setLogRecordFactory(record_factory)


def set_traceID(id: str):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.trace_id = id
        return record

    logging.setLogRecordFactory(record_factory)


def set_context(context: str):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.context = context
        return record

    logging.setLogRecordFactory(record_factory)


def set_level(level: str):
    logging.getLogger().setLevel(level)


def turn_off():
    logging.getLogger().setLevel(logging.CRITICAL+1)


def setup_logging(level=None):
    config_file = pathlib.Path("log_config.json")
    with open(config_file) as f_in:
        logging.config.dictConfig(json.load(f_in))

    set_traceID("default_trace_id")
    set_system("default_system")
    set_group("default_group")
    if level:
        set_level(level)
