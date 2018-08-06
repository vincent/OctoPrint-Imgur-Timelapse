# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import pyimgur

class ImgurTimelapsePlugin(octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.EventHandlerPlugin,
                           octoprint.plugin.TemplatePlugin,
                           octoprint.plugin.RestartNeedingPlugin):

    def get_settings_defaults(self):
        return dict(
            client_id=None,
            client_secret=None,
            album="Octoprint",
            delete_after_upload=False
        )

    def get_settings_restricted_paths(self):
        return dict(
            admin=[['client_id'], ['client_secret'], ['album'], ]
        )

    def get_template_configs(self):
        return [
            dict(type='settings', custom_bindings=False, template='imgur_timelapse_settings.jinja2')
        ]

    def get_update_information(self):
        return dict(
            imgur_timelapse=dict(
                displayName="Imgur Timelapse Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="vincent",
                repo="OctoPrint-Imgur-Timelapse",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/vincent/OctoPrint-Imgur-Timelapse/archive/{target_version}.zip"
            )
        )

    @property
    def client_id(self):
        return self._settings.get(['client_id'])

    @property
    def client_secret(self):
        return self._settings.get(['client_secret'])

    @property
    def album(self):
        return self._settings.get(['album'])

    @property
    def delete_after_upload(self):
        return self._settings.get_boolean(['delete_after_upload'])

    def on_event(self, event, payload):
        from octoprint.events import Events
        if event == Events.MOVIE_DONE:
            self.upload_timelapse(payload)

    def upload_timelapse(self, payload):
        file_path = payload['movie']
        file_name = payload['movie_basename']
        if self.client_id and self.api_secret:
            im = pyimgur.Imgur(client_id=self.client_id, client_secret=self.client_secret)
        else:
            self._logger.info('No Imgur API Tokens Defined! Cannot Upload Timelapse %s!' % file_name)
            return

        delete = self.delete_after_upload

        self._logger.info('Uploading %s to Imgur...' % file_name)
        try:
            im.upload_image(path=file_path, title=file_name, album=self.album)
            self._logger.info('Uploaded %s to Imgur!' % file_name)
        except Exception as e:
            delete = False
            if e.user_message_text:
                self._logger.info(e.user_message_text)
            else:
                self._logger.info(e)

        if delete:
            import os
            self._logger.info('Deleting %s from local disk...' % file_name)
            os.remove(file_path)
            self._logger.info('Deleted %s from local disk.' % file_name)


__plugin_name__ = "Imgur Timelapse Plugin"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ImgurTimelapsePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

