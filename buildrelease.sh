# change to this directory in command line and execute this file


VERSION='1.01'
REVERSION='1\.01'
BUILDGLYPHS=true
BUILDROBOFONT=true

# Change version number in lib
find "lib/speedpunk" -type f -exec sed -i "" "s/VERSION = 'beta'/VERSION = '$REVERSION'/g" {} +

# Mirror source folder
rm -Rf "Builds/$VERSION/"
cp -Rf "Builds/Source/" "Builds/$VERSION/"

# Glyphs
#if $BUILDGLYPHS; then
#cd "Glyphs Plugin"
## Change version number
#find . -type f -exec sed -i "" "s/%%VERSION%%/$REVERSION/g" {} +
#rm -Rf build
#rm -Rf dist
#python2.5 setup.py py2app -A --resources toolbar.png
##python2.5 setup.py py2app --semi-standalone --resources toolbar.png
## Change version number back
#sed -i "" "s/$REVERSION/%%VERSION%%/g" setup.py
#sed -i "" "s/$REVERSION/%%VERSION%%/g" SpeedPunk.py
#cd ..
#cp -R "Glyphs Plugin/dist/SpeedPunk.glyphsTool" "Release/$VERSION/Glyphs/"
#fi

# Glyphs
if $BUILDGLYPHS; then
echo "Building SpeedPunk $VERSION for Glyphs"
cp -f "Glyphs/SpeedPunk.py" "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources"
cp -f "Resources/toolbar.png" "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources"
cp -Rf "/Users/yanone/Code/git/Yanone/ynlib.git (trunk)/Lib/ynlib" "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources/"
cp -Rf "lib/speedpunk" "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources/"
cp -Rf "/Users/yanone/Code/svn/typesupply/vanilla.git/trunk/Lib/vanilla" "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources/"
find "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool/Contents/Resources" -name .svn -exec rm -rf {} \;
# Copy
rm -Rf "/Users/yanone/Library/Application Support/Glyphs/Plugins/SpeedPunk.glyphsTool"
cp -Rf "Builds/$VERSION/Glyphs/SpeedPunk.glyphsTool" "/Users/yanone/Library/Application Support/Glyphs/Plugins/"
fi


# RoboFont
if $BUILDROBOFONT; then
echo "Building SpeedPunk $VERSION for RoboFont"
cp -f "RoboFont/SpeedPunkTool.py" "Builds/$VERSION/RoboFont/SpeedPunk.roboFontExt/lib/"
cp -f "Resources/toolbar.png" "Builds/$VERSION/RoboFont/SpeedPunk.roboFontExt/Resources/"
cp -Rf "/Users/yanone/Code/git/Yanone/ynlib.git (trunk)/Lib/ynlib" "Builds/$VERSION/RoboFont/SpeedPunk.roboFontExt/lib/"
cp -Rf "lib/speedpunk" "Builds/$VERSION/RoboFont/SpeedPunk.roboFontExt/lib/"
# Copy
rm -Rf "/Users/yanone/Library/Application Support/RoboFont/plugins/SpeedPunk.roboFontExt"
cp -Rf "Builds/$VERSION/RoboFont/SpeedPunk.roboFontExt" "/Users/yanone/Library/Application Support/RoboFont/plugins/"
fi


# Change version number
find "Release" -type f -exec sed -i "" "s/%%VERSION%%/$REVERSION/g" {} +
# Change version number in lib back
find "lib/speedpunk" -type f -exec sed -i "" "s/VERSION = '$VERSION'/VERSION = 'beta'/g" {} +
