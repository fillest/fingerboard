A CLI tool for musicians, it highlights some notes on a fingerboard

* supports arbitrary custom tuning (any number of strings)
* lists and highlights scale notes (everywhere)
* highlights chord notes (everywhere)
* shows "fret" numbers, string numbers
* currently it's just a single file Python script, just download it anywhere

Usage examples:

* `python3 path/to/fingerboard.py --help`
* `python3 path/to/fingerboard.py --tunings`
* `python3 path/to/fingerboard.py --scales`
* `python3 path/to/fingerboard.py --tuning "guitar" --scale minor --tonic "a"`
* `python3 path/to/fingerboard.py --tuning "ga#c#ega#" --chord am7`

Current limitations:

* (!) does not support flats (b) yet (both for input and output), so use only sharps (#)
* chord support is limited yet, only supports base, 7 and 9 chords (also without #), e.g.: c, cm7, c9
* please use only lowercase for notes everywhere for now

(contribution/reporting) If you want to add or change anything (please don't hesitate to), please ask me first - I've created this project primarily for my own convenience, and our visions potentially can differ too much in some ways. I'm also planning eventually to rewrite this most likely into a web page/app
