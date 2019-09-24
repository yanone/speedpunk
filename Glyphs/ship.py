import os, sys

from subprocess import Popen,PIPE,STDOUT

# Notarize workflow: https://developer.apple.com/documentation/xcode/notarizing_your_app_before_distribution/customizing_the_notarization_workflow?language=objc

# Check notarization: xcrun altool --notarization-history 0 -u "post@yanone.de" -p "@keychain:AppleDev_AppSpecificPassword de.Yanone.GlyphsAppSpeedPunkReporter"

flavour = sys.argv[-1]


_list = [
['Remove shipping folder', 'rm -r ship', None, '', True],

['Validate notarization', 'spctl -a -vvv -t install SpeedPunk.glyphsReporter', None, ''],
['Staple notarization to plugin', 'xcrun stapler staple SpeedPunk.glyphsReporter', None, ''],
['Validate stapling', 'stapler validate SpeedPunk.glyphsReporter', None, ''],

['Create shipping folder', 'mkdir ship', None, ''],
['Copy files', 'cp -R SpeedPunk.glyphsReporter ship', None, ''],
['Copy files', 'cp Install.txt ship', None, ''],
['Copy files', 'cp Update.txt ship', None, ''],

['ZIP it again', 'ditto -c -k --rsrc ship SpeedPunk.glyphsReporter.ship.zip', None, ''],
['Remove shipping folder', 'rm -r ship', None, ''],
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
