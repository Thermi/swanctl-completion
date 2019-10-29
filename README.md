Bash auto completion for swanctl
================================

auto completion for all options, except
the names of IKE_SAs and CHILD_SAs or generally any
variable data due to no nice API to get that via VICI.

Current problems:
* Short args (e.g. -v) aren't auto completed with a trailing space
* good and working URI handler
* No data fetching or strongswan.conf parsing yet
* No integration to take prefix and sysconfdir at install time into account
* No automation for integrating python script into completion script
* description for all methods and classes
