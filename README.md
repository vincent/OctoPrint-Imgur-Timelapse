# OctoPrint-Imgur-Timelapse

Automatically upload rendered timelapses to Imgur. Can also delete after upload to save space on the Raspberry Pi
SD Card.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/jslay88/OctoPrint-Imgur-Timelapse/archive/master.zip

## Configuration

You must provide an API Token to be able to upload rendered timelapses to Imgur.
To do this, [create a Imgur App](https://api.imgur.com/oauth2/addclient)
select `Imgur API` -> `App Folder` -> Provide Folder Name.
Once the app is created, scroll down to the `OAuth 2` section, and click `Generate Token`. Paste the token into the
settings pane.

# Thank you

Shamelessly copied from https://github.com/jslay88/OctoPrint-Dropbox-Timelapse
