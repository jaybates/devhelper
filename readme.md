###############
 DevHelper
###############

 
DevHelper is a small cli (Command Line) utility for automating the process of installing and configuring you Wordpress projects. This utility will create a wordpress installation, with predefined plugins, theme downloaded via the BitBucket API from a private repo, configure database, and setup an Apache conf.

DevHelper Relies on BitBucket to keep custom project tracking, and utilizes the BitBucket to project's Wehbook to keep server up-to-date wit the latest repo PUSHES.

============
 Installing
============

This script relies on the `WP-Cli <https://wp-cli.org/>`. This should be installed a system PATH, and accessible as wp-cli.

For easy update via git, it suggested to install DevHelper locally using pip::

    cd ./devhelper
    pip install -e ./

=================
 Using DevHelper
=================

Installing Custom Theme, project tracks via BitBucket and configured with Webhook::

    devhelper custom -s <subdomain> -p <BitBucket Project Name> -r <BitBucket Repo Name> -t <Theme Name>

Installing Themes::

    devhelper theme -s <subdomain> -t <Theme Name>

Packaging Project for Launch::

    devhelper launch -s <subdomain>

Project Removal::

    devhelper remove -s <subdomain>

Webhook::

    devhelper webhook -s <subdomain> -t <Theme Name>