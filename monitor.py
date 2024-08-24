import os
import shutil
import schedule


import compiler
from docker_host_checker import DockerHostsChecker


def _transform_hosts_file():
    checker = DockerHostsChecker()
    containers = checker.find_xhost_containers()
    containers = [
        {
            "name": c.name,
            "ip": checker.get_container_ip(c),
            "xhost": checker.get_container_XHOST_value(c)
        }
        for c in containers
    ]
    containers = [
        f"# {c['name']}\n{c['ip']}    {c['xhost']}"
        for c in containers
    ]

    hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='/etc/hosts')
    hostfile_compiler.read_hosts_file()


    hostfile_compiler.update_hosts_data(containers)
    print('#################')
    print('#################')
    print('#################')
    compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
    print(compiled_hosts_file)
    return compiled_hosts_file

def _write_to_hosts_file(new_content):
    with open("/etc/hosts", 'w') as f:
        lines = f.write(new_content)

def _backup_hosts_file():
        shutil.copy("/etc/hosts", "/etc/hosts.bp.dxw")


def monitor():
    new_hosts_file_content = _transform_hosts_file()

    if not os.path.isfile("/etc/hosts.bp.dxw"):
        _backup_hosts_file()

    _write_to_hosts_file(new_hosts_file_content)
