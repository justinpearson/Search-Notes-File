# Search-Notes-File

- [Summary](#summary)
- [Installation](#installation)
- [Description](#description)
- [Usage](#usage)
- [Additional notes](#additional-notes)

## Summary

This simple program lets me search my personal notes file.

My notes file (notes.txt) has a lot of entries. Each entry has a date, a title line, and several body lines:

```
2018-03-11
USB type C troubles on the 2017 macbook laptop with anker USB hub & USB cable

It turns out that USB Type C ports and devices are really confusing:
there are tons of data-transfer protocols that can be implemented over...
...
```

Using this searching program, I can search the entries' title text and body text, and open the desired entry in Sublime Text:

```
% which ns

ns: aliased to python3 ~/Notes/Search-Notes-File/main.py


% ns usb mac

Hi from "/Users/justin/Notes/Search-Notes-File/main.py" !
pwd = /Users/justin
Found subl = /Applications/Sublime Text.app/Contents/SharedSupport/bin/subl
Found notes file = /Users/justin/Notes/notes.txt
26 ms - Read notes file: 111808 lines.
43 ms - Split into 2197 entries.
4 ms - Parsed 2197 entries.
11 ms - 4 results matching:
        title=['usb', 'mac']
        body=[]
        match_ANY_title=False
        match_ANY_body=False
        match_title_OR_body=False

[0] 12126: 2015-01-04 - Virtualbox error: macbook host / ubuntu guest virtual machine. "pci#0: New device in slot 0x58, usb-ehci"
[1] 58064: 2018-01-23 - Mac: Burning ubuntu linux iso to usb thumb drive
[2] 59776: 2018-03-11 - USB type C troubles on the 2017 macbook laptop with anker USB hub & USB cable
[3] 67140: 2018-07-21 - tiny usb wireless network 802.11n adapter for raspberry pi

Which entry? (leave blank to quit): 2

Opening notes file in Sublime Text at line 59776...

Bye from "/Users/justin/Notes/Search-Notes-File/main.py" !
```

## Installation

1. Download:


    ```
    % git clone git@github.com:justinpearson/Search-Notes-File.git
    ```

2. Install dependencies (`more_itertools`):

    ```
    % cd Search-Notes-File
    % python3 -m pip install -r requirements.txt
    ```

3. (Optional) Run tests:

    ```
    % pytest
    ```

4. Run, pointing to your own notes file and your own text editor:

    ```
    % python3 main.py --sublime-exe /your/own/text-editor-exe --notes-file /your/own/notes-file.txt foo bar
    ```

5. (Optional) Alias ^-- this command in your shell for convenience:

    ```
    % cat 'alias ns="python3 /your/downloads/Search-Notes-File/main.py --sublime-exe /your/own/text-editor-exe --notes-file /your/own/notes-file.txt"' >> ~/.zshrc
    ```

## Description

You can search the entries' titles and bodies. Title searches are most common, so they are given as the first positional args, eg,

```
main.py usb mac
```

finds entries whose titles contain 'usb' AND 'mac' (case-insensitive).

- By default, in order to be considered a match, an entry's title must match ALL the given title search strings.
You can change this behavior to search for ANY title search string with the command-line option `--match-ANY-title`.

Use `--body-search-strs` (or `-b`) to search the body text, eg,

```
main.py -b "type c" hub
```

finds entries whose bodies contain 'type c' AND 'hub'.

- By default, if you specify body search strings, an entry's body must match ALL of them to be considered a matching entry.
You can change this behavior to search for ANY body search string with the command-line option `--match-ANY-body`.


Titles and bodies can be searched together:

```
main.py foo -b bar
```

finds entries whose titles contain 'foo' AND whose bodies contain 'bar'.

- By default, an entry only matches if its title matches the given title terms AND its body matches the given body terms.
You can change this behavior to search title terms OR body terms with the  command-line option `--match-title-OR-body`.


**Syntax Summary**

The command

    python3 main.py p1 p2 p3 --body-search-strs q1 q2 q3

searches the notes file for entries whose title matches the title search terms (`p1`, `p2`, AND `p3`)
AND whose body matches the body search terms (`q1`, `q2`, AND `q3`).
Those three ANDs can be turned to ORs using three command-line flags; specifically:

```
title:
    matches pattern p1
    AND matches pattern p2   <- AND by default;
    AND matches pattern p3      use OR with --match-ANY-title
    ...

AND                          <- AND by default; use OR with --match-title-OR-body

body:
    matches pattern q1
    AND matches pattern q2   <- AND by default;
    AND matches pattern q3      use OR with --match-ANY-body
    ...
```


## Usage

Display this with `main.py -h`:

```
usage: main.py [-h] [-b [S1 [S2 ...]]] [-v] [--sublime-exe PATH] [--notes-file PATH] [--match-ANY-title]
               [--match-ANY-body] [--match-title-OR-body]
               [title_search_strs ...]

Search my notes file and prompt to open a matching entry in Sublime Text.

positional arguments:

  title_search_strs     Strings to search the entries' titles for.

optional arguments:

  -h, --help            show this help message and exit

  -b [S1 [S2 ...]], --body-search-strs [S1 [S2 ...]]

                        Strings to search the entries bodies for. (Not req'd.)

  -v, --verbose         Print helpful debugging info.

  --sublime-exe PATH    Path to Sublime Text executable.

  --notes-file PATH     Path to my notes file.

  --match-ANY-title     Matching entries' titles must have AT LEAST 1 given title str present.
                        (Default is ALL.)

  --match-ANY-body      Matching entries' bodies must have AT LEAST 1 given body str present.
                        (Default is ALL.)

  --match-title-OR-body
                        Entry matches if its title OR body matches the given search terms.
                        (Default is title AND body must match.)
```




## Additional notes

Search strings can be regexs if you escape them, eg, `MPE\?G` to match `MPEG` or `MPG`.
