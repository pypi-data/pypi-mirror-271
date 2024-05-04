"""Console script for rstms_testmail."""

import subprocess
import sys
from pprint import pformat
import json

import click
import click.core

from .counter import Counter
from .settings import Settings
from .exception_handler import ExceptionHandler
from .gmail import Gmail
from .sendgrid_server import SendGrid
from .smtp_server import SMTPServer
from .shell import _shell_completion
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"


def _ehandler(ctx, option, debug):
    ctx.obj = dict(ehandler=ExceptionHandler(debug))
    ctx.obj["debug"] = debug
    return debug


def fail(msg):
    click.echo("Failed: " + msg, err=True)
    sys.exit(-1)


@click.command("testmail")
@click.version_option(message=header)
@click.option("-d", "--debug", is_eager=True, is_flag=True, callback=_ehandler, help="debug mode")
@click.option(
    "--shell-completion",
    is_flag=False,
    flag_value="[auto]",
    callback=_shell_completion,
    help="configure shell completion",
)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
@click.option("-f", "--from", "from_addr", envvar="TESTMAIL_FROM")
@click.option("-t", "--to", "to_addr", envvar="TESTMAIL_TO")
@click.option("-s", "--subject", default="test{}")
@click.option("-c", "--set-counter", type=int)
@click.option("-s", "--system", envvar="TESTMAIL_SYSTEM")
@click.option("-e", "--exec", "exec_command", envvar="TESTMAIL_EXEC")
@click.option("-k", "--api-key", envvar="TESTMAIL_API_KEY")
@click.option("-u", "--username", envvar="TESTMAIL_USERNAME")
@click.option("-p", "--password", envvar="TESTMAIL_PASSWORD")
@click.option("-P", "--port", default=465, envvar="TESTMAIL_PORT")
@click.option('--profile', default='default', show_envvar=True, envvar='TESTMAIL_PROFILE')
@click.option("--dryrun", is_flag=True)
@click.argument("message", required=False)
@click.pass_context
def cli(ctx, debug, shell_completion, quiet, verbose, dryrun, to_addr, from_addr, set_counter, subject, message, system, exec_command, username, password, port, api_key, profile):
    """send a test email"""

    if "{}" in subject:
        counter = Counter(label="testmail")
        count = counter.bump(set_counter)
        subject = subject.replace("{}", str(count))

    settings = Settings(profile=f"testmail_{profile}", from_addr=from_addr, to_addr=to_addr, system=system, exec_command=exec_command, username=username, password=password,port=port, api_key=api_key)

    if debug:
        click.echo(json.dumps({'config': settings.dict()}, indent=2))

    if settings.exec_command is not None:
        message = subprocess.check_output(settings.exec_command, shell=True).decode()

    if message == "-":
        message = sys.stdin.read()
    elif message is None:
        message = subject

    if settings.system == "gmail":
        server = Gmail()
    elif settings.system == "sendgrid":
        server = SendGrid(api_key)
    elif settings.system.startswith('smtp:'):
        server = SMTPServer(settings.system, settings.port, settings.username, settings.password)
    else:
        fail("unknown system")

    if dryrun:
        click.echo(pformat(settings.dict()))
        sys.exit(0)
    else:
        error = server.send(settings.from_addr, settings.to_addr, subject, message)

    if error:
        fail(pformat(error))

    if not quiet:
        click.echo(f"sent {subject} to {settings.to_addr}")

    if verbose:
        click.echo(pformat(server.result))

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
