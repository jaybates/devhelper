import os, shutil, subprocess

# PHP-FPM runs as www-data which has no shell, so no PATH ENVs are set

os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

def theme_repo(subdomain, theme_name):

    # Go to Repo directory

    repo_path = "/var/www/projects/" + subdomain + "/wp-content/themes/" + theme_name

    os.chdir(repo_path)

    # Stash & Pull latest updates from Repo

    git_stash = subprocess.Popen('git stash --include-untracked', shell=True)
    git_stash.communicate()

    git_pull = subprocess.Popen('git pull origin master', shell=True)
    git_pull.communicate()

    # Run Gulp

    gulp_webhook = subprocess.Popen('gulp webhook', shell=True)
    gulp_webhook.communicate()