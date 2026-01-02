BIM2PNG converts (reverses compression of) BIM (`42 49 4D`) and Divinity (`44 49 56 49 4E 49 54 59`) texture maps (`*.tga`) **found in Doom External community mods** to PNG images for editing.

**It cannot be used to extract original game texture maps!** Game textures are packed differently and require restructuring/reconstructing.

For Oodle-compressed textures, `oo2core.dll` library from Doom Eternal is required. Set the installation path `OO2CORE_LIBRARY_PATH` if you encountered errors. You won't need this if the modded BIM wasn't compressed, but it's not up to you.

Currently, only format 25 and 33 are supported. (I haven't seen mods using other textures formats.) If you encountered another format, check the definition on https://github.com/brongo/eternal-010-templates/blob/50ab5dcce1a04d44afdecb037a8a41503a9638fd/templates/DoomEternalTGA.bt#L161. Either put it in the same case as 25/33, or write a new case and call another decoding function from `texture2ddecoder`. Once you decode and load the texture map into a PIL `Image`, the rest of the loop should continue the same.
