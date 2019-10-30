Bash auto completion for swanctl
================================

Auto completion for all options. If access to the VICI socket is not possible,
no suggestions are shown.
The URI to the VICI socket can be configured via the SWANCTL_COMPLETION_VICI_URI
environmental variable. If not set, it connects to the default of the VICI Python egg.

Requirements:
* Python3
* VICI python egg in library search path
* urllib for Python3

Features:
* Auto completion for all options and arguments
* fails with traceback output to user if unseen circumstances occur
* Does not suggest already used arguments
* Automatically stops suggesting on using -h or --help
* User configurable URI to VICI socket
* Easily changeable for users due to clear Python syntax

How to install:
1) Copy it in some dir you have access to
2) source it from your shell

Optional:
* Hook it up in your \~/.bashrc so it's loaded automatically
* Copy it in /usr/share/bash-completion/completions/ so it's loaded
  automatically like any other auto completion

Current problems:
* Short args (e.g. -v) aren't auto completed with a trailing space
* No data fetching or strongswan.conf parsing yet
* No integration to take prefix and sysconfdir at install time into account
* No description for all methods and classes

How to report bugs:
Just open an issue on the GH repo for this script.

FAQ
===
*Q* Is this script affiliated with the strongSwan project?
*A* No.