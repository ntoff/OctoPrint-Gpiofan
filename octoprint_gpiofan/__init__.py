# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class GpiofanPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.TemplatePlugin):

	def get_settings_defaults(self):
		return dict(
			pin=0
		)

	def mirror_m106(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and gcode.startswith('M106'):
			fanPwm = re.search("S(\d+\.?\d*)", cmd)
			if fanPwm and fanPwm.group(1):
				fanPwm = fanPwm.group(1)
				if Decimal(fanPwm) < self.minPWM and Decimal(fanPwm) != 0:
					self._logger.info("fan pwm value " + str(fanPwm) + " is below threshold, increasing to " + str(self.minPWM) + " (" + str(self.minSpeed) + "%)")
	 				cmd = "M106 S" + str(self.minPWM)
					return cmd,
				elif Decimal(fanPwm) > self.maxPWM:
					self._logger.info("fan pwm value " + str(fanPwm) + " is above threshold, decreasing to " + str(self.maxPWM) + " (" + str(self.maxSpeed) + "%)")
					cmd = "M106 S" + str(self.maxPWM)
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

__plugin_name__ = "Gpiofan Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GpiofanPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.mirror_m106,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

