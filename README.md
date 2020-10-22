# local_vars Ansible plugin

**local_vars** is an [Ansible](https://www.ansible.com) [Vars plugin](https://docs.ansible.com/ansible/latest/plugins/vars.html) that allows different variables per controller host. This is useful if you run the same playbooks on different controllers, and like to set some variables that are different for each controller.

## Requirements

There are no requirements other than Ansible.

The plugin has been tested on Ansible 2.6 to 2.10, but likely may be used on earlier and later versions.

## Installation

Copy the file `vars_plugin/local_vars.py` into a `vars_plugins` directory adjacent to your play, or by putting it in one of the directory sources configured in `ansible.cfg`.

## Usage

Create a folder `<location of your Ansible folder>/local_vars/`, and in that folder, place a file `<hostname>.yml` for each controller host, where `<hostname>` is the hostname of the controller as returned by `socket.gethostname()`. This is usually the short name, without domain name, but this is not guaranteed in Python. Run `hostname` in your terminal to find your controllers hostname.

## Example

For example, you have an Ansible playbook that creates some local files on the controller and may want to run Ansible from either your macOS laptop or your Linux server.

You may want to sets a variable `local_cache_folder` which is different for each controller:

In `local_vars/tux.yml` (assuming `tux` is the name of your Linux server):

    ---
    local_cache_folder: /var/tmp/my_ansible_cache

In `local_vars/golden-delicious.yml` (assuming `golden-delicious` is the name of your mac laptop, and `steve` your username):

    ---
    local_cache_folder: /Users/steve/Library/Caches/my_ansible_cache

## Limitations

The hostname of the controller is always taken from `socket.gethostname()` as-is.

This is *usually* the hostname without the domain name, but *might* be the fully qualified domain name (FQDN), depending on your operating system.

It is not possible to override this local hostname using extra_vars (`-e` on the command line)
and/or environment variables. The reason is technical. An Ansible plugin does not have access to other variables (some may not be defined). It may be possible to parse `ansible.context.CLIARGS['extra_vars']` or `os.environ`, but that is very error-prone, and is not implemented.

## License

This plugin was written in 2019 by Freek Dijkstra and published on Github in 2020.

This plugin is released under the MIT license. You can use it in any way you like, as long as you preserve the copyright notice. I'm fine with redistributions under other licenses (including the GPL, what is used as the Ansible license), as long as proper attribution is given, and it is clear that the original version is available under a permissive open source license. A link to the most recent Git repository is appreciated, but not required.

## Further Information

This software is published on https://github.com/macfreek/ansible_local_vars/.
Feel free to leave comments and feedback at this URL.
