import base64, click, json, os, requests, shutil, slugify, subprocess, sys

# Grab Projects Theme from specified Repo

def get_theme(subdomain, theme_name, cmd):

    subdomain = slugify.slugify(subdomain)

    theme_directory = '/var/www/projects/' + subdomain + '/wp-content/themes/'

    os.chdir(theme_directory)

    if cmd == 'custom':
        theme_name = slugify.slugify(theme_name)

        subprocess.call('ssh-agent bash -c "ssh-add /var/www/.ssh/id_rsa; git clone --depth 1 -b master git@bitbucket.org:sociusmarketing/socius-base-underscores-theme-bs4.git ./' + theme_name + '"', shell=True)
    else:
        subprocess.call('ssh-agent bash -c "ssh-add /var/www/.ssh/id_rsa; git clone --depth 1 -b master git@bitbucket.org:sociusmarketing/' + theme_name + '.git ./' + theme_name + '"', shell=True)

    os.chdir(theme_directory + '/' + theme_name)

    subprocess.call(['rm', '-rf', '.git'])

# Go to Project's root dir and initialize Git for Repo and make initial push

def initialize(subdomain, repo, theme_name):

    subdomain = slugify.slugify(subdomain)

    slug = slugify.slugify(repo)

    theme_path = '/var/www/projects/' + subdomain + '/wp-content/themes/' + theme_name

    os.chdir(theme_path)

    subprocess.call('git init', shell=True)
    subprocess.call('git remote add origin git@bitbucket.org:sociusmarketing/' + slug + '.git', shell=True)
    subprocess.call('git add .', shell=True)
    subprocess.call('git commit -m "Initial Commit"', shell=True)
    subprocess.call('ssh-agent bash -c "ssh-add /var/www/.ssh/id_rsa; git push -u origin master"', shell=True)

# Grab Access Token for API Calls

def access_token():

    url = 'https://bitbucket.org/site/oauth2/access_token'

    payload = 'grant_type=client_credentials'

    auth = base64.b64encode(os.getenv('BITBUCKET_USER') + ':' + os.getenv('BITBUCKET_SECRET'))

    headers = {
        'Authorization': "Basic " + auth,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache"
    }

    response = requests.request('POST', url, data=payload, headers=headers)

    oauth_data = json.loads(response.text)

    return oauth_data['access_token']

# Create the Project in side of BitBucket (Send payload as JSON)

def create_project(token, project):

    regex_pattern = r'[^A-Za-z]+'

    key = slugify.slugify(project.upper(), separator='', regex_pattern=regex_pattern, lowercase=False)

    url = 'https://api.bitbucket.org/2.0/teams/' + os.getenv('BITBUCKET_ACCOUNT')  + '/projects/'

    payload = {'name':  project, 'key':  key, 'is_private': True}

    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request('POST', url, json=payload, headers=headers)

    if response.status_code == 201:
        click.secho('Success: A new project has been created', fg='green')
    elif response.status_code == 403:
        click.secho('Failed: The requesting user isn\'t authorized to create the project', fg='red')
        sys.exit()
    elif response.status_code == 404:
        click.secho('Failed: A team doesn\'t exist at this location', fg='red')
        sys.exit()


    return response

# Create the Repo set to Project in side of BitBucket (Send payload as JSON)

def create_repo(token, project, repo):

    regex_pattern = r'[^A-Za-z]+'

    key = slugify.slugify(project.upper(), separator='', regex_pattern=regex_pattern, lowercase=False)

    slug = slugify.slugify(repo)

    url = 'https://api.bitbucket.org/2.0/repositories/' + os.getenv('BITBUCKET_ACCOUNT')  + '/' + slug
    
    payload = {
        'scm': 'git',
	    'name': repo,
        'project': { 'key': key},
        'is_private': True
    }

    headers = {
        'Authorization': "Bearer " + token,
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request('POST', url, json=payload, headers=headers)

    if response.status_code == 200:
        click.secho('Success: A newly created repository', fg='green')
    elif response.status_code == 400:
        click.secho('Failed: document was invalid, or if the caller lacks the privilege to create repositories', fg='red')
        sys.exit()
    elif response.status_code == 401:
        click.secho('Failed: The request was not authenticated', fg='red')
        sys.exit()

    return response

# Create the Webhook for Repo in side of BitBucket (Send payload as JSON)

def create_webhook(token, repo, subdomain, theme_name):
    
    subdomain = slugify.slugify(subdomain)

    theme_name = slugify.slugify(theme_name)

    slug = slugify.slugify(repo)

    base_url = subprocess.check_output(['sed', '-n', 's/referer=//p', '/etc/webmin/config']).strip()

    url = 'https://api.bitbucket.org/2.0/repositories/' + os.getenv('BITBUCKET_ACCOUNT')  + '/' + slug + '/hooks'

    payload = {
        'scm': 'git',
        "description": "Socius Droplet Webhook",
        'url': "https://" + base_url + "/bb-hook.php?key=H9xnL0a4s1w2q9&project=" + subdomain + "&theme=" + theme_name + "&themerepo=1",
        'active': True,
        'events': ["repo:push"]
    }

    headers = {
        'Authorization': "Bearer " + token,
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request('POST', url, json=payload, headers=headers)

    if response.status_code == 201:
        click.secho('Success: A webhook was registered', fg='green')
    elif response.status_code == 403:
        click.secho('Failed: document was invalid, or if the caller lacks the privilege to install webhook', fg='red')
        sys.exit()
    elif response.status_code == 404:
        click.secho('Failed: The repository does not exist', fg='red')
        sys.exit()

    return response