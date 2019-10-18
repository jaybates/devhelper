import os, shutil, slugify, subprocess

def add(subdomain):

    # Format and set variables

    subdomain = slugify.slugify(subdomain)

    # Go to Apaches Sites dir

    os.chdir('/etc/apache2/sites-available')

    # Copy sample apache virtual host for to configure projects virtual hose

    shutil.copyfile('./wordpress.sample', './' + subdomain + '.conf')

    # Set Projects paramas in the projects virtual host and restart Apache

    subprocess.call(['sed', '-i', 's/project_name/' + subdomain + '/g', subdomain + '.conf'])
    subprocess.call(['a2ensite', subdomain])
    subprocess.call(['systemctl', 'reload', 'apache2'])

def remove(subdomain):

    # Format and set variables

    subdomain = slugify.slugify(subdomain)

    # Unset Project from Apache

    subprocess.call(['a2dissite', subdomain])

    os.chdir('/etc/apache2/sites-available')

    subprocess.call(['rm', '-f', subdomain + '.conf'])

    subprocess.call(['systemctl', 'reload', 'apache2'])

