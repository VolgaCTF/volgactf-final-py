# -*- coding: utf-8 -*-
import os

import click

from .flag_api import SubmitResult, GetinfoResult, FlagAPIHelper


def get_api_endpoint():
    return os.getenv('THEMIS_FINALS_API_ENDPOINT')


@click.group()
def cli():
    pass


@cli.group(name='flag')
def flag_cli():
    pass


def print_submit_results(results):
    click.echo('')
    for r in results:
        flag_part = click.style(r['flag'], bold=True)
        status_part = None
        if r['code'] == SubmitResult.SUCCESS:
            status_part = click.style(r['code'].name, fg='green')
        else:
            status_part = click.style(r['code'].name, fg='red')
        click.echo(flag_part + '  ' + status_part)


@flag_cli.command()
@click.argument('flags', nargs=-1)
def submit(flags):
    h = FlagAPIHelper(get_api_endpoint())
    results = h.submit(*flags)
    print_submit_results(results)


def print_getinfo_results(results):
    click.echo('')
    for r in results:
        flag_part = click.style(r['flag'], bold=True)
        status_part = None
        extra_part = ''
        if r['code'] == GetinfoResult.SUCCESS:
            status_part = click.style(r['code'].name, fg='green')
            extra_part += click.style('\n  Team: ', bold=True, fg='yellow')
            extra_part += click.style(r['team'])
            extra_part += click.style('\n  Service: ', bold=True, fg='yellow')
            extra_part += click.style(r['service'])
            extra_part += click.style('\n  Round: ', bold=True, fg='yellow')
            extra_part += click.style('{0:d}'.format(r['round']))
            extra_part += click.style(
                '\n  Not before: ', bold=True, fg='yellow')
            extra_part += click.style(
                '{0:%-m}/{0:%-d} {0:%H}:{0:%M}:{0:%S}'.format(r['nbf']))
            extra_part += click.style('\n  Expires: ', bold=True, fg='yellow')
            extra_part += click.style(
                '{0:%-m}/{0:%-d} {0:%H}:{0:%M}:{0:%S}'.format(r['exp']))
        else:
            status_part = click.style(r['code'].name, fg='red')

        click.echo(flag_part + '  ' + status_part + extra_part)


@flag_cli.command()
@click.argument('flags', nargs=-1)
def getinfo(flags):
    h = FlagAPIHelper(get_api_endpoint())
    results = h.getinfo(*flags)
    print_getinfo_results(results)
