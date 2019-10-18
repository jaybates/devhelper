import click
import devhelper.helpers.wordpress as wp
import devhelper.helpers.apache as apache

@click.command()
@click.option('--subdomain', '-s',  required=True, type=str)

def cli(subdomain):

    """
    Easy cleanup for sites no longer in Developement. Dumps DB into site and creates archive, then removes directory and Apache config.
    """

    click.echo('[:: Removal Start ::]')

    click.echo('Remove Project')

    wp.remove(subdomain)

    click.echo('Remove Project from Apache')

    apache.remove(subdomain)

    click.echo('[:: Removal Complete ::]')
