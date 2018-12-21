# coding=utf-8
from __future__ import absolute_import

import pigpio
from decimal import *
import re
import octoprint.plugin

class GpiofanPlugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.ShutdownPlugin,
					octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.RestartNeedingPlugin,
                    octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self._pigpio = pigpio.pi()
		self._pin=0
		
	def on_after_startup(self):
		self.get_settings_updates()
		#self._pin = self._settings.getInt(["pin"])
		self._pigpio.set_PWM_dutycycle(self._pin,0)
		self._logger.info("BCM pin " + str(self._pin) + " is being used to mirror the fan pwm signal.")

	def on_shutdown(self):
		self._pigpio.set_PWM_dutycycle(self._pin,0)

	def get_settings_defaults(self):
		return dict(
			pin=0
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def on_settings_save(self, data):
		s = self._settings
		if "pin" in data.keys():
			s.setInt(["pin"], data["pin"])
		s.save()
		self.get_settings_updates()
		
	def get_settings_updates(self):
		self._pin=self._settings.getInt(["pin"])

	def mirror_m106(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and gcode.startswith('M106'):
			fanPwm = re.search("S(\d+\.?\d*)", cmd)
			if fanPwm and fanPwm.group(1):
				fanPwm = fanPwm.group(1)
				self._logger.info("Mirroring pwm "+ fanPwm + " to BCM " + str(self._pin))
				self._pigpio.set_PWM_dutycycle(self._pin,Decimal(fanPwm))
				return cmd,

	def get_update_information(self):
		return dict(
			gpiofan=dict(
				displayName="Gpiofan Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="ntoff",
				repo="OctoPrint-Gpiofan",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/ntoff/OctoPrint-Gpiofan/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "GPIO fan mirror"
__plugin_description__ = " Takes the PWM value from M106 Snnn and mirrors it to the configured GPIO pin of a raspberry pi."

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GpiofanPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.mirror_m106,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

