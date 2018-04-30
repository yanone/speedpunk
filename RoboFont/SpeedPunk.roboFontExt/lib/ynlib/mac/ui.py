def SetMouseSpeed(speed):

	from ynlib.mac import ExecuteAppleScript
	
	script = u"""\
tell application "System Preferences" to activate

tell application "System Preferences"
	activate
	set current pane to pane "com.apple.preference.keyboard"
end tell
tell application "System Events"
	tell process "System Preferences"
		click menu item "Maus" of menu "Einstellungen" of menu bar 1
		set value of slider "Zeigerbewegung" of window "Maus" to %s
	end tell
end tell

tell application "System Preferences" to quit""" % (speed)

	ExecuteAppleScript(script)


def SetKeyboardLanguage():
	pass

def Growl(message, iconfiletype = None, iconapp = None):
	u"""\
	Display messages using Growl
	"""
	
	from ynlib.system import Execute
	
	if iconfiletype:
		return Execute('/usr/local/bin/growlnotify -m "%s" -i "%s"' % (message, iconfiletype))
	elif iconapp:
		return Execute('/usr/local/bin/growlnotify -m "%s" -a "%s"' % (message, iconapp))
	else:
		return Execute('/usr/local/bin/growlnotify -m "%s"' % (message))

def GrowlError(message):
	u"""\
	Display messages using Growl
	"""
	
	from ynlib.system import Execute
	
	return Execute('/usr/local/bin/growlnotify -m "%s" --image /Users/yanone/Pictures/Tango/tango-icon-theme/32x32/status/dialog-warning.png -s' % (message))
