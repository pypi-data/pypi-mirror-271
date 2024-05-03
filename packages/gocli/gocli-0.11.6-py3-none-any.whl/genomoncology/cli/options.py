"""Shared state and options for all commands."""

import logging
import uuid
from datetime import datetime

import click
from genomoncology.cli import const
from genomoncology.cli.state import State

_logger = logging.getLogger(__name__)


def debug_option(f):
    def callback(_ctx, _param, value):
        if value:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)

    return click.option(
        "-d",
        "--debug",
        is_flag=True,
        expose_value=False,
        help="Run in debug mode. (debug level logging).",
        callback=callback,
    )(f)


def quiet_option(f):
    def callback(_ctx, _param, value):
        if value:
            logging.basicConfig()
            logging.getLogger().setLevel(logging.WARNING)

    return click.option(
        "-q",
        "--quiet",
        is_flag=True,
        expose_value=False,
        help="Run in quiet mode. (warning level logging).",
        callback=callback,
    )(f)


def pipeline_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.pipeline = value
        return value

    return click.option(
        "-p",
        "--pipeline",
        type=str,
        expose_value=False,
        help="Pipeline identifier.",
        callback=callback,
    )(f)


def build_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.build = value
        return value

    return click.option(
        "-b",
        "--build",
        type=click.Choice(const.BUILDS),
        default=const.GRCH37,
        expose_value=False,
        help="Reference assembly.",
        callback=callback,
    )(f)


def run_id_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.run_id = value or str(uuid.uuid4())
        return value

    return click.option(
        "-r",
        "--run_id",
        type=str,
        expose_value=False,
        help="Unique identifier of this run.",
        callback=callback,
    )(f)


def size_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.batch_size = value
        return value

    return click.option(
        "-s",
        "--size",
        type=int,
        default=50,
        expose_value=False,
        help="Size of batches when calling API.",
        callback=callback,
    )(f)


def glob_option(f, default=None):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.glob = value
        return value

    if default is None:
        default = ["*.vcf", "*.vcf.gz"]

    return click.option(
        "-g",
        "--glob",
        multiple=True,
        type=str,
        default=default,
        expose_value=False,
        help="File pattern (e.g. *.vcf) of files to load",
        callback=callback,
    )(f)


def include_tar_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.include_tar = value
        return value

    return click.option(
        "--include-tar",
        is_flag=True,
        expose_value=False,
        help="Search in tar (tgz, tar.gz, tar) files",
        callback=callback,
    )(f)


def hard_option(f):
    def callback(ctx, _param, value):
        state = ctx.ensure_object(State)
        state.hard_failure = value
        return value

    return click.option(
        "-h",
        "--hard",
        is_flag=True,
        expose_value=False,
        help="Hard stop on failure.",
        callback=callback,
    )(f)


def validate_dob(_ctx, _param, value):
    if value:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as e:
            _logger.error('invalid date format: %s', e)
            raise click.BadParameter("format must be YYYY-MM-DD")
    return value


def common_options(f):
    f = quiet_option(f)
    f = debug_option(f)
    f = hard_option(f)
    return f
