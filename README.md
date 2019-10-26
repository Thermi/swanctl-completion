Bash auto completion for swanctl
================================

auto completion for all options, except
the names of IKE_SAs and CHILD_SAs or generally any
variable data due to no nice API to get that via VICI.

Current problems:
* Always autocompletes starting with a dash (-), although that's not intended
* Does not stop completing when variable data has to be provided, e.g. conn names or IDs