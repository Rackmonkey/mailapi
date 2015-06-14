# UWSGI Installation of mailapi

## Archlinux

### Requirements

* uwsgi
* uwsgi-plugin-python

### Configuration

Create following file in **/etc/uwsgi/mailapi.ini**
```
[uwsgi]
#application's base folder
venv = <Rootpath of Directory with VirtualEnvironment>
module = <Name of mainmodule> eg. main

plugins = python
pythonpath = <Rootpath of Application>
callable = app
master = True
chmod-socket = 777
socket = /var/run/%n.sock
logto = /var/log/%n.log
```

### Start Mailapi
Run as User with systemd access:

```
systemctl start uwsgi@mailapi
```

For Autostart run:

```
systemctl enable uwsgi@supertool
```
