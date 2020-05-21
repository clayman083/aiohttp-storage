import os

import click
from alembic import command  # type: ignore
from alembic.config import Config as AlembicConfig  # type: ignore


@click.group()
@click.pass_context
def storage(ctx):
    """ Manage application database. """

    app_config = ctx.obj["app"]["config"]

    storage_root = ctx.obj["app"]["storage_root"]
    directory = os.path.join(storage_root, "migrations")

    config = AlembicConfig(os.path.join(directory, "alembic.ini"))
    config.set_main_option("script_location", directory)
    config.set_main_option("sqlalchemy.url", app_config.db.uri)

    ctx.obj["migrations"] = config


@storage.command()
@click.option("-m", "--message", default=None)
@click.option(
    "--autogenerate",
    default=False,
    is_flag=True,
    help=(
        "Populate revision script with andidate migration "
        "operations, based on comparison of database to model"
    ),
)
@click.option(
    "--sql",
    default=False,
    is_flag=True,
    help=("Don`t emit SQL to database - dump to standard " "output instead"),
)
@click.option(
    "--head",
    default="head",
    help=(
        "Specify head revision or <branchname>@head to" "base new revision on"
    ),
)
@click.option(
    "--splice",
    default=False,
    is_flag=True,
    help='Allow a non-head revision as the "head" to splice onto',
)
@click.option(
    "--branch-label",
    default=None,
    help="Specify a branch label to apply to the new revision",
)
@click.option(
    "--version-path",
    default=None,
    help="Specify specific path from config for version file",
)
@click.option(
    "--rev-id",
    default=None,
    help="Specify a hardcoded revision id instead of generating one",
)
@click.pass_context
def migrate(
    ctx,
    message=None,
    autogenerate=False,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
):
    """Create new database migration. """
    command.revision(
        ctx.obj["migrations"],
        message,
        sql=sql,
        head=head,
        autogenerate=autogenerate,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
    )


@storage.command()
@click.argument("revision", default="head")
@click.option(
    "--sql",
    default=False,
    help=("Don`t emit SQl to database - dump to standard " "output instead"),
)
@click.option(
    "--tag",
    default=None,
    help="Arbitrary `tag` name - can be used by custom `env.py`",
)
@click.pass_context
def upgrade(ctx, revision="head", sql=False, tag=None):
    """Upgrade to a later version"""
    command.upgrade(ctx.obj["migrations"], revision, sql=sql, tag=tag)


@storage.command()
@click.argument("revision", default="head")
@click.option(
    "--sql",
    default=False,
    help=("Don`t emit SQl to database - dump to standard " "output instead"),
)
@click.option(
    "--tag",
    default=None,
    help="Arbitrary `tag` name - can be used by custom `env.py`",
)
@click.pass_context
def downgrade(ctx, revision="-1", sql=False, tag=None):
    """Revert to a previous version"""
    command.downgrade(ctx.obj["migrations"], revision, sql=sql, tag=tag)
