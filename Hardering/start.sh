#!/bin/bash

echo "Disabilitando KVM per permettere a VirtualBox di usare VT-x..."
sudo rmmod kvm_intel
sudo rmmod kvm

echo "Avviando la VM con Vagrant/VirtualBox..."
vagrant up

echo "VM avviata!"
