How to save developpers lives with KVM
######################################
:date: 2011-09-02 09:12
:tags: kvm, virtualization, howto
:author: Mathieu Leplatre (credits: Anthony Prades)

This how-to will help you setting-up a very powerful development environment
using Linux kernel-based virtualization system : KVM.

=========
But Why ?
=========

You work on various projects, with specific requirements, with various 
technologies, diverse operating systems or cpu architectures, usually with 
a couple of services like databases or Web servers. 

You would prefer not taking this whole family with you each time you start your machine. 

Probably, you also want to upgrade your workstation to the last unstable eye-candy OS
without compromising your projects dependencies and without reinstalling all this stuff, 
or you may want to restore the environment you had when you were working on this famous project a year ago.

Your sysadmin uses KVM and you would like to push your local instances on 
production servers in a blink ?

The magic medicine exists, and is freely available :)

At the end, you are promised to enjoy : 

* a GUI to manage your Virtual Machines (VM)
* a local domain to access your VMs by their name
* a fully integrated set of machines, accessible from each others


================
A Strict Minimum
================

KVM is maintained along with the Linux kernel, and is thus fully integrated
in your system, taking advantage of optimizations available. 

A strict minimum is to install ``kvm`` and a set of commands to control it : ``libvirt``.
As a human being, you may want a GUI : ``virt-manager``.

::

    sudo apt-get install kvm libvirt-bin virt-manager


Managing your Virtual Machines
==============================

* Setup your VM network interface as auto DHCP

Cloning
* u-dev/00 persistent on debian


======================
A Local Network Domain
======================

* DNS daemon

=====================
Dynamic Configuration
=====================

In order to make sure your VM always obtain the same IP adress when it
boots, we setup a DHCP daemon on your host, that will match Mac adresses.

Note:
* at boot, restart it

==================
Host Configuration
==================

* DNS
* search domain

=====================
Adding a new instance
=====================

* Get its Mac address (virt-manager : `Device` > `Hardware` > ...)
* Add it to your DHCP configuration (``dhcpd.conf``)
* Add an IP for this entry in your DNS zone (``yourzone.loc``)
* Add it in the reverse DNS (``XX.0.0.1.db``)

If you do that all day, you'll quickly find it relevant to write a script...
