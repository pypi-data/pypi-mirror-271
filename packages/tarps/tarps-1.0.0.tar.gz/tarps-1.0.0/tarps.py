#!/usr/bin/env python3


# Made By Rayan Haddad

import os
import subprocess
import colorama
import click
import time
import requests

from rich import print
from colorama import Fore
from rich.tree import Tree

__version__ = '0.1.0'
__author__ = 'Rayan Haddad'

@click.group()
def cli():
    pass


def memoize(f): 
    fast = {}  
    def partner(l): 
        if l not in fast: 
            fast[l] = f(l) 
        return fast[l]  
    return partner 


@memoize
@cli.command()
@click.argument("package_name")
def install(package_name):
    try:
        print(f"Cached [ [bright_cyan]{package_name}[/bright_cyan] ]")

        start_time = time.time()

        # Check if the package exists in PyPI
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        
        if response.status_code == 200:
            print("Package Verified [ [green]OK[/green] ]")
            print(f"Version Fetched [bold]dev[/bold]")



            # Package exists, proceed with installation
            result = subprocess.run(["pip", "install", package_name], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

            
            if result.stderr:
                print(result.stderr)
            
            print(f"[bright_magenta]Installed {package_name}[/bright_magenta]")

        else:
            print("Package Verified [ [red]ERROR[/red] ]")
            print("[bold]Package does not exist[/bold]")

            quit()

        print("✨ %s ms" % (time.time() - start_time))

    except Exception as e:
        print(e)
        print(f"Error Installing {package_name}")
        

@memoize
@cli.command()
@click.argument("package_name")
def uninstall(package_name):
    try:
        print(f"Captured [ [bright_cyan]{package_name}[/bright_cyan] ]")
        start_time = time.time()

        result = subprocess.run(["pip", "uninstall", package_name, "-y"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

        if result.returncode == 0:
            print(f"Uninstalled {package_name}\n")
        else:
            print(f"Error Uninstalling {package_name} [Exit Code: {result.returncode}]\n")
        

        print(f"[bright_magenta]Uninstalled {package_name}[/bright_magenta]\n")
        print("✨ %s " % (time.time() - start_time))

    except Exception as e:
        print(e)
        print(f"[red]Error[/red] Uninstalling {package_name}")
        quit()


@memoize
@cli.command()
def update():
    try:
        print("Updating [[bold]tarps.0.1.0[/bold]]")
        start_time = time.time()

        subprocess.call(["pip", "install", "--upgrade", "pip"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

        print(f"[bright_magenta]Tarps has been updated successfully[/bright_magenta]\n")

        print("✨ %s ms" % (time.time() - start_time))

    except Exception as e:
        print(f"[red]Error[/red] Updating tarps.")
        quit()



if __name__ == '__main__':
    cli()