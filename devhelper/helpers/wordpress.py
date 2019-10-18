import binascii, mysql.connector, os, shutil, slugify, subprocess

def install(subdomain):

    # Create Base URL from webmin Config

    base_url = subprocess.check_output(['sed', '-n', 's/referer=//p', '/etc/webmin/config']).strip()

    # Format and Set variables

    subdomain = slugify.slugify(subdomain)

    db_name = slugify.slugify(subdomain, separator='_')
    db_pass = binascii.hexlify(os.urandom(32)).decode('ascii')

    wp_user = 'sociusadmin'
    wp_pass = binascii.hexlify(os.urandom(16)).decode('ascii')
    wp_url = 'http://' + subdomain + '.' + base_url + '/'

    admin_email = subprocess.check_output(['git', 'config', 'user.email']).strip()

    # Create Projects Directory for Wordpress Install

    project_path = '/var/www/projects/' + subdomain

    os.mkdir(project_path)
    os.chdir(project_path)

    # Connect to MySQL to create Database, User, and Grant User Permissions to Database

    db_connection = mysql.connector.connect(
        host= "localhost",
        user= os.getenv('DB_USER'),
        passwd= os.getenv('DB_PASS')
    )

    db_cursor = db_connection.cursor()

    db_cursor.execute('CREATE DATABASE wp_' + db_name)
    db_cursor.execute('CREATE USER \'' + db_name  + '\'@\'localhost\' IDENTIFIED BY \'' + db_pass  + '\'')
    db_cursor.execute('GRANT ALL PRIVILEGES ON wp_' + db_name  + '.* TO \'' + db_name  + '\'@\'localhost\'')
    db_cursor.execute('FLUSH PRIVILEGES')

    db_cursor.close()

    # Run WP-CLI command to install and configur Wordpress Installation

    subprocess.call(['wp-cli', 'core', 'download', '--allow-root'])
    subprocess.call(['wp-cli', 'core', 'config', '--dbname=wp_' + db_name , '--dbuser=' + db_name, '--dbpass=' + db_pass, '--allow-root'])
    subprocess.call(['wp-cli', 'core', 'install', '--url=' + wp_url, '--title=' + subdomain, '--admin_user=' + wp_user, '--admin_password=' + wp_pass, '--admin_email=' + admin_email, '--allow-root'])
    subprocess.call(['wp-cli', 'option', 'update', 'blog_public', '0', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'delete', 'akismet', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'delete', 'hello', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'custom-post-type-ui', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'better-wp-security', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'wp-migrate-db', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'socius-marketing-page-taxonomy', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'wp-optimize', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'wordpress-seo', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'acf-code-field', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'disable-gutenberg', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'https://github.com/wp-sync-db/wp-sync-db/archive/master.zip', '--allow-root'])
    subprocess.call(['wp-cli', 'plugin', 'install', 'https://dev1.sociusinc.com/acf-pro.zip', '--allow-root'])
    subprocess.call(['wp-cli', 'theme', 'update', '--all', '--allow-root'])
    subprocess.call('wp-cli post delete $(wp-cli post list --format=ids --allow-root) --allow-root', shell=True)
    subprocess.call('wp-cli post delete $(wp-cli post list --post_type=\'page\' --format=ids --allow-root) --allow-root', shell=True)

    # Create and write wordpress credentials to text file

    f = open('wordpress_credentials.txt', 'w')

    f.write('You can log in to the administrator account with the following information:\n')
    f.write('Username: ' + wp_user + '\n')
    f.write('Password: ' + wp_pass + '\n')
    f.write('Login URL : ' + wp_url + '/wp-admin \n')

    f.close()

    # Dump Wordpress's Database to Project's root

    dump = subprocess.Popen('mysqldump -u root --databases wp_' + db_name + '> install_wp_' + db_name + '.sql', shell=True)
    dump.communicate()

    # Create Install Archive

    os.chdir('..')

    archive = subprocess.Popen('zip -r ./install_' + subdomain + '.zip' + ' ./' + subdomain, shell=True)
    archive.communicate()

def custom_theme_task(subdomain, theme_name):

    # Fromat and set variables

    subdomain = slugify.slugify(subdomain)

    theme_name = slugify.slugify(theme_name)

    theme_path = '/var/www/projects/' + subdomain + '/wp-content/themes/' + theme_name

    # Go to Theme dir and Install Dev Packages and Run Gulp

    os.chdir(theme_path)

    subprocess.call(['rm', '-f', '.git'])
    subprocess.call('sed -i \'s/localhost\\/default/localhost\\/\'$subdomain\'/g\' ./gulpfile.js', shell=True)
    subprocess.call(['npm', 'install', '--save-dev'])
    subprocess.call(['npm', 'rebuild', 'node-sass'])
    subprocess.call(['gulp', 'webhook'])


def droplet_permissions(subdomain):

    # Format and set variables

    subdomain = slugify.slugify(subdomain)

    # Build Project's Path

    project_path = '/var/www/projects/' + subdomain

    # Set Proper Permissions for Project (DO droplet specific. Not for Launching sites)

    subprocess.call(['chown', '-R', 'www-data:www-data', project_path])
    subprocess.call(['chmod', '-R', 'g+w', project_path])
    subprocess.call(['chmod', '-R', 'g+s', project_path])

def remove(subdomain):

    subdomain = slugify.slugify(subdomain)

    # Go to Projects Folder

    project_path = '/var/www/projects/' + subdomain

    os.chdir(project_path)

    # Build Database name from subdomain

    db_name = slugify.slugify(subdomain, separator='_')

    # Create a database Backup

    dump = subprocess.Popen('mysqldump -u root --databases wp_' + db_name + '> final_wp_' + db_name + '.sql', shell=True)
    dump.communicate()

    # Remove database from Server

    db_connection = mysql.connector.connect(
        host= "localhost",
        user= os.getenv('DB_USER'),
        passwd= os.getenv('DB_PASS')
    )

    db_cursor = db_connection.cursor()

    db_cursor.execute('DROP DATABASE wp_' + db_name)
    db_cursor.execute('DROP USER \'' + db_name  + '\'@\'localhost\'')
    db_cursor.execute('FLUSH PRIVILEGES')

    db_cursor.close()


    # Create Backup of Project

    os.chdir('..')

    archive = subprocess.Popen('zip -r ./final_' + subdomain + '.zip' + ' ./' + subdomain, shell=True)
    archive.communicate()

    # Remove Projects Install

    subprocess.call(['rm', '-rf', './' + subdomain])

def launch(subdomain):

    # Format and set variables

    subdomain = slugify.slugify(subdomain)

    # Go to Projects Folder

    projects_path = '/var/www/projects/'

    os.chdir(projects_path)

    # Create Temp Project for Launch

    temp_launch = projects_path + 'launch'
    project_path = projects_path + subdomain

    shutil.copytree(project_path, temp_launch)

    # Go to Temp Project Launch Folder

    os.chdir(temp_launch)

    # Build Database name from subdomain

    db_name = slugify.slugify(subdomain, separator='_')

    # Create a database Backup

    dump = subprocess.Popen('mysqldump -u root --databases wp_' + db_name + '> launch_wp_' + db_name + '.sql', shell=True)
    dump.communicate()

    # Reset Permissions for Launch

    os.chdir('..')

    subprocess.call('find ./launch -type d -exec chmod 755 {} +', shell=True)
    subprocess.call('find ./launch -type f -exec chmod 644 {} +', shell=True)

    # Create Backup of Project

    archive = subprocess.Popen('zip -r ./launch_' + subdomain + '.zip' + ' ./launch', shell=True)
    archive.communicate()

    # Remove Temp Launch Folder

    shutil.rmtree(temp_launch)