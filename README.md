# Element Detector
This is an INI which can be used to detect the element of the character present on screen. It exposes two global variables which can be used in other mods.

## Usage
Put the INI in your mods folder. Then use it in your other mods as you want. You can access the global variable `$\global\detector\element`. The values are starting from 0 and in the order which regions released in game.
So anemo = 0, geo = 1, electro = 2, etc
The main application is that with merged mods, you can incorporate it into your INI to automatically switch mods based on element.

Bonus: you can do `travelerElement` instead of `element` if you want to use that for something.
### Internal working
The exact logic is: "the element of the character that was last visible on the screen. If the last character was traveler, the element is determined by the skill icon that was last visible on screen". Keep this in mind if you see some weird situation where script doesnt behave in exact way you expected.

## Generating the INI yourself
You must have downloaded or cloned the [GIMI assets repository](https://github.com/SilentNightSound/GI-Model-Importer-Assets). Set the relative path in `generate_ini.py`, and run it using Python 3. Refer to the output for missing stuff.

`hash not found for Character` : This means that the character hash could not be found in the assets repository. Check your assets repository whether it contains the dump for the character and whether `hash.json` has the `position_vb` for blank component name or body component.

`using element other for Character`: This means the element is not known for the character. Update the element lists in `reference.json` accordingly.

Demo: https://imgur.com/a/w11BXxF
