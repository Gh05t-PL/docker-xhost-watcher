import docker

class DockerHostsChecker:
    def __init__(self, client=None):
        self.client = client or docker.from_env()

    def get_running_containers(self):
        """Fetch the list of all running containers."""
        try:
            return self.client.containers.list()
        except docker.errors.APIError as e:
            print(f"Failed to list containers: {str(e)}")
            return []

    def get_container_ip(self, container, network_name=None):
        """Get the IP address of a container."""
        try:
            networks = container.attrs['NetworkSettings']['Networks']
            if network_name:
                return networks[network_name]['IPAddress']
            return next(iter(networks.values()))['IPAddress']
        except (KeyError, StopIteration) as e:
            print(f"Failed to retrieve IP address for container {container.name}: {str(e)}")
            return None

    def get_container_env_value(self, container, env_name):
        """Retrieve the value of a specified environment variable from a container."""
        try:
            env_vars = container.attrs['Config']['Env']
            return next((env.split('=', 1)[1] for env in env_vars if env.startswith(f'{env_name}=')), None)
        except (StopIteration, KeyError) as e:
            print(f"Failed to retrieve {env_name} from container {container.name}: {str(e)}")
            return None

    def get_container_XHOST_value(self, container):
        return self.get_container_env_value(container, 'XHOST')

    def extract_hosts_env(self, container):
        """Extract and format the HOSTS environment variable and the container's IP address."""
        try:
            ip_address = self.get_container_ip(container)
            hosts_env = self.get_container_env_value(container, 'HOSTS')
            if ip_address and hosts_env:
                return f"{ip_address}    {hosts_env}"
            return None
        except Exception as e:
            print(f"Failed to extract HOSTS environment variable from container {container.name}: {str(e)}")
            return None

    def find_xhost_containers(self):
        """Find all containers with the XHOST environment variable."""
        try:
            return [container for container in self.get_running_containers() if self.get_container_env_value(container, 'XHOST')]
        except Exception as e:
            print(f"Failed to find XHOST containers: {str(e)}")
            return []

