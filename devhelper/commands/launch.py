import click
import devhelper.helpers.wordpress as wp

@click.command()
@click.option('--subdomain', '-s',  required=True, type=str)

def cli(subdomain):

    """
    Creates an archive with the site and database, with proper permissions ready for production. This will NOT Remove the site from the development server.
    """

    click.echo('[:: Launch Start ::]')

    click.echo('Creating Launch Archive')

    wp.launch(subdomain)

    click.echo('[:: Launch Complete ::]')
