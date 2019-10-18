import click
import devhelper.helpers.webhook as webhook

@click.command()
@click.option('--subdomain', '-s',  required=True, type=str)
@click.option('--theme-name', '-t', required=True, type=str)

def cli(subdomain, theme_name):
    """
    Webhook is triggered by a commit Bitbucket, which will pull the latest commit to the Dev server and run Gulp.
    """
    
    click.echo('[:: Webhook Start ::]')

    webhook.theme_repo(subdomain, theme_name)

    click.echo('[:: Webhook Complete ::]')
