import click
import devhelper.helpers.wordpress as wp
import devhelper.helpers.bitbucket as bitbucket
import devhelper.helpers.apache as apache

@click.command()
@click.option('--subdomain', '-s', required=True, type=str)
@click.option('--theme-name', '-t', required=True, type=str)

def cli(subdomain, theme_name):

    """
    Create a new Wordpress install for a theme site (Theme sites do not included BitBucke)
    """

    cmd = 'theme'

    click.echo('[:: Setup Start ::]')

    click.echo('Installing Wordpress')

    wp.install(subdomain)

    click.echo('Download Theme from Repository')

    bitbucket.get_theme(subdomain, theme_name, cmd)

    click.echo('Settting Project Permissions')

    wp.droplet_permissions(subdomain)

    click.echo('Configuring Project in Apache')

    apache.add(subdomain)

    click.echo('[:: Setup Complete ::]')
