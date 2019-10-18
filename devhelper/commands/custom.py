import click
import devhelper.helpers.wordpress as wp
import devhelper.helpers.bitbucket as bitbucket
import devhelper.helpers.apache as apache

@click.command()
@click.option('--subdomain', '-s',  required=True, type=str)
@click.option('--project', '-p', required=True, type=str)
@click.option('--repo', '-r',  required=True, type=str)
@click.option('--theme-name', '-t', required=True, type=str)

def cli(subdomain, project, repo, theme_name):

    """
    Create a new Wordpress install for a Custom Theme Site (Custom Theme Sites will Create a Bitbucket Project & Repo)
    """

    cmd = 'custom'

    click.echo('[:: Setup Start ::]')

    click.echo('Creating Bitbucket Project')

    bitbucket.create_project(bitbucket.access_token(), project)
  
    click.echo('Creating Bitbucket Repository')

    bitbucket.create_repo(bitbucket.access_token(), project, repo)

    click.echo('Adding Bitbucket Repoository Webhook')

    bitbucket.create_webhook(bitbucket.access_token(), repo, subdomain, theme_name)

    click.echo('Installing Wordpress')

    wp.install(subdomain)

    click.echo('Download Theme from Repository')

    bitbucket.get_theme(subdomain, theme_name, cmd)

    click.echo('Run NPM and Gulp Task')

    wp.custom_theme_task(subdomain, theme_name)

    click.echo('Settting Project Permissions')

    wp.droplet_permissions(subdomain)

    click.echo('Prepare Project and Push Initial Commit')

    bitbucket.initialize(subdomain, repo, theme_name)

    click.echo('Configuring Project in Apache')

    apache.add(subdomain)

    click.echo('[:: Setup Complete ::]')
