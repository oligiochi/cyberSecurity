#!/bin/bash

echo "Spegnendo la VM..."
vagrant halt

echo "Riattivando KVM..."
sudo modprobe kvm
sudo modprobe kvm_intel

echo "VM spenta e KVM riattivato!"
