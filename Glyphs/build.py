import os, sys

from subprocess import Popen,PIPE,STDOUT

# Notarize workflow: https://developer.apple.com/documentation/xcode/notarizing_your_app_before_distribution/customizing_the_notarization_workflow?language=objc

# Check notarization: xcrun altool --notarization-history 0 -u "post@yanone.de" -p "@keychain:AppleDev_AppSpecificPassword de.Yanone.GlyphsAppSpeedPunkReporter"

flavour = sys.argv[-1]


_list = [
['Remove all resource forks', 'xattr -cr SpeedPunk.glyphsReporter', None, ''],
['Remove code signatues', 'rm -r SpeedPunk.glyphsReporter/Contents/_CodeSignature', None, '', True],
['Remove code signatues', 'rm -r SpeedPunk.glyphsReporter/Contents/CodeResources', None, '', True],
['Remove zip file', 'rm SpeedPunk.glyphsReporter.notarize.zip', None, '', True],
['Remove zip file', 'rm SpeedPunk.glyphsReporter.ship.zip', None, '', True],
# ['Sign main script', 'codesign -s "Jan Gerner" -f SpeedPunk.glyphsReporter/Contents/MacOS/main.py', None, ''],
# ['Sign Python scripts', 'codesign -s "Jan Gerner" -f SpeedPunk.glyphsReporter/Contents/Resources/plugin.py', None, ''],
# ['Sign Python scripts', 'codesign -s "Jan Gerner" -f SpeedPunk.glyphsReporter/Contents/Resources/speedpunk/__init__.py', None, ''],
# ['Sign Python scripts', 'codesign -s "Jan Gerner" -f SpeedPunk.glyphsReporter/Contents/Resources/speedpunk/speedpunklib.py', None, ''],
# ['Sign Python scripts', 'codesign -s "Jan Gerner" -f SpeedPunk.glyphsReporter/Contents/Resources/speedpunk/speedpunkWindow.py', None, ''],
['Sign outer package', 'codesign --deep -s "Jan Gerner" -f SpeedPunk.glyphsReporter', None, ''],
['Verify signature', 'codesign -dv --verbose=4 SpeedPunk.glyphsReporter', None, ''],
['Verify signature', 'codesign --verify --deep --strict --verbose=2 SpeedPunk.glyphsReporter', None, ''],

['ZIP it', 'ditto -c -k --keepParent --rsrc SpeedPunk.glyphsReporter SpeedPunk.glyphsReporter.notarize.zip', None, ''],

['Notarize', 'xcrun altool --notarize-app --primary-bundle-id "de.Yanone.GlyphsAppSpeedPunkReporter" --username "post@yanone.de" --password "@keychain:AppleDev_AppSpecificPassword de.Yanone.GlyphsAppSpeedPunkReporter" --file SpeedPunk.glyphsReporter.notarize.zip', None, ''],
]

for l in _list:

	mayFail = False
	alt = None
	excludeCondition = None
	if len(l) == 2:
		desc, cmd = l
	if len(l) == 3:
		desc, cmd, alt = l
	if len(l) == 4:
		desc, cmd, alt, excludeCondition = l
	if len(l) == 5:
		desc, cmd, alt, excludeCondition, mayFail = l


	if not excludeCondition or excludeCondition != flavour:

		print(desc, '...')

		out = Popen(cmd, stderr=STDOUT,stdout=PIPE, shell=True)
		output, exitcode = out.communicate()[0].decode(), out.returncode

		if exitcode != 0 and not mayFail:
			print(output)
			print()
			print(cmd)
			print()
			print('%s failed! See above.' % desc)
			print()
			if alt:
				print('Debugging output:')
				os.system(alt)
			sys.exit(1)

print('Done.')
print()
