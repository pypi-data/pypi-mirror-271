# libsrg_apps

This library provides three python applications

* DiskInfo - displays disks, aliases, formatting and ZFS pool membership
* ztool - zfs toolset to copy volumes within and between nodes
* ReZFS - this application is used for the re-installation of zfs when something goes bump after a new Fedora Kernel update
  * It can edit the repo file from the previous Fedora release to try and get it working on the current release
  * It can stomp on the dkms files to force a recompilation
  * It has limited ability to run on RHEL, but RHEL doesn't do rapid kernel updates
* Stage0 - this application nfs mounts my Ansible environment to a newly installed node
  * installs files for nfs mounting and local operation of ansible
  * mounts my ansible scripts and roles from an intranet shared drive
  * prompts with the command to execute ansible locally to setup ssh and ssh keys

DiskInfo and ztool are probably the only things here of general usefulness outside of my homelab environment.

These applications make extensive use of libsrg, and were originally packaged as part of that library.
I'm thinning libsrg out to just the reusable components, and using libsrg_apps to package the apps mainly for
my own ease of installation.

