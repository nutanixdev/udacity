#!/usr/bin/env bash
set -ex

if [[ -n '@@{name}@@' ]]; then
  _hostname='@@{name}@@'
else
  _hostname='web@@{calm_array_index}@@'
  _hostname='HAProxy' # system_release.txt?
fi
cat "${_hostname}" | sudo tee /etc/hostname
