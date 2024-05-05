import csv
import json
from urllib.parse import urlparse

from . import pritunl

from pritunl_api.utils.query import org_user
from pritunl_api.utils.keygen import profile_key

import click

from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()


def get(**kwargs):
    table = Table(
        title=f"User Profile and Key Information:",
        title_style="bold green",
        title_justify="left",
        show_lines=True
        )

    table.add_column("Status", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    if kwargs['all_users']:
        org, user = org_user(pritunl=pritunl, org_name=kwargs['org_name'])
        users = list(filter(lambda x: x['type'] == 'client', user))

        if users:
            for user in users:
                key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])

                status = []
                status.append("[red]Disabled[/red]" if user['disabled'] else "[green]Enabled[/green]")
                status.append("[green]With PIN[/green]" if user['pin'] else "[yellow]No PIN[/yellow]")

                table.add_row(f"{status}", f"{user['name']}", f"{org['name']}", f"{key_view_url}", f"{key_uri_url}")

        console.print(table)

    else:
        org, user = org_user(pritunl=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
        if user:
            key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])

            status = []
            status.append("[red]Disabled[/red]" if user['disabled'] else "[green]Enabled[/green]")
            status.append("[green]With PIN[/green]" if user['pin'] else "[yellow]No PIN[/yellow]")

            table.add_row(f"{status}", f"{user['name']}", f"{org['name']}", f"{key_view_url}", f"{key_uri_url}")
            console.print(table)
        else:
            console.print(f"[bold red]No user profile found![/bold red]")

    if kwargs['show_advanced_details']:
        console.print(
            f"Advanced Details:",
            style="blue bold"
        )
        if kwargs['all_users']:
            print_json(json.dumps(users))
        else:
            print_json(json.dumps(user))


def create(**kwargs):
    table = Table(
        title=f"User Profile Created and Key Information:",
        title_style="bold green",
        title_justify="left",
        show_lines=True
        )

    table.add_column("Actions", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("User Email", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    def __create_user(org_id, user_name, user_email):
        user_data = {
            'name': user_name,
            'email': user_email
        }

        if kwargs['pin']:
            user_data["pin"] = kwargs['pin']

        if kwargs['yubikey_id']:
            user_data["auth_type"] = "yubico"
            user_data["yubico_id"] = kwargs['yubikey_id'][:12]

        create_user = pritunl.user.post(org_id=org_id, data=user_data)

        for user in create_user:
            key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])

            actions.append("[green]Created[/green]")

            table.add_row(f"{actions}", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

    if kwargs['org_name'] and kwargs['user_name'] and kwargs['user_email'] and not kwargs['from_csv']:
        org, user = org_user(pritunl=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
        actions = []

        if not user:
            __create_user(org_id=org['id'], user_name=kwargs['user_name'], user_email=kwargs['user_email'])
        else:
            key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])
            actions.append("[yellow]Skipped[/yellow]")
            table.add_row(f"{actions}", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

        console.print(table)

    elif kwargs['from_csv'] and not kwargs['org_name'] and not kwargs['user_name'] and not kwargs['user_email']:
        csv_list = []
        with open(kwargs['from_csv']) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                csv_list.append(row)

        for row in csv_list:
            org, user = org_user(pritunl=pritunl, org_name=row['Organization'], user_name=row['Username'])
            actions = []

            if not user:
                __create_user(org_id=org['id'], user_name=row['Username'], user_email=row['Email'])
            else:
                key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])
                actions.append("[yellow]Skipped[/yellow]")
                table.add_row(f"{actions}", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

        console.print(table)

    else:
        if not kwargs['org_name'] and not kwargs['user_name'] and not kwargs['user_email'] and not kwargs['from_csv']:
            raise click.UsageError('Error: You entered with empty options.')
        else:
            raise click.UsageError('Error: You entered an invalid combination of options.')


def update(**kwargs):
    table = Table(
        title=f"User Profile Update and Key Information:",
        title_style="bold green",
        title_justify="left",
        )

    table.add_column("Actions", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    org, user = org_user(pritunl=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

    if user:
        user_data = {
            'name': user['name'],
            'email': user['email'],
            'disabled': False,
        }

        actions = []

        if kwargs['disable']:
            user_data.update({'disabled': True})
            actions.append("[red]Disabled[/red]")
        else:
            actions.append("[green]Enabled[/green]")

        if kwargs['pin']:
            user_data["pin"] = kwargs['pin']
            actions.append("[green]Set PIN[/green]")
        else:
            actions.append("[green]As is PIN State[/green]")

        response = pritunl.user.put(org_id=org['id'], usr_id=user['id'], data=user_data)

        if response:
            key_uri_url, key_view_url = profile_key(pritunl=pritunl, org_id=org['id'], usr_id=user['id'])
            table.add_row(f"{actions}", f"{user['name']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")
            console.print(table)

    else:
        console.print(f"[bold red]No user profile to update![/bold red]")


def delete(**kwargs):
    table = Table(
        title=f"User Profile Delete:",
        title_style="bold green",
        title_justify="left",
        )

    table.add_column("Actions", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")

    org, user = org_user(pritunl=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

    if user:
        actions = []
        response = pritunl.user.delete(org_id=org['id'], usr_id=user['id'])

        if response:
            actions.append("[red]Deleted[/red]")

            table.add_row(f"{actions}", f"{user['name']}", f"{user['organization_name']}")
            console.print(table)

    else:
        console.print(f"[bold red]No user profile to delete![/bold red]")
