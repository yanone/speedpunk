def ExecuteAppleScript(text):
	u"""Execute AppleScript code through osascript"""

	import os
	lines = text.split("\n")
	
	call = """osascript -e '%s' """ % ("' -e '".join(lines))
	os.system(call)
