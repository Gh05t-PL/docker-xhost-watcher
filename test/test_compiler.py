from unittest import TestCase
import compiler

class TestHostsFileCompiler(TestCase):
    def test_get_hosts_file_string(self):
        hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='./test_files/hosts_1')
        hostfile_compiler.read_hosts_file()


        hostfile_compiler.update_hosts_data(['123.123.123.123  foo.bar.local'])
        print('#################')
        print('#################')
        print('#################')
        compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
        print(compiled_hosts_file)



    def test_get_hosts_file_string__hosts_multiple_complete_xhosts_tags(self):
        hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='./test_files/hosts_multiple_complete_xhosts_tags')
        hostfile_compiler.read_hosts_file()


        hostfile_compiler.update_hosts_data(['123.123.123.123  foo.bar.local'])
        print('#################')
        print('#################')
        print('#################')
        compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
        print(compiled_hosts_file)


    def test_get_hosts_file_string__hosts_data_and_end_of_xhosts_token(self):
        hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='./test_files/hosts_data_and_end_of_xhosts_token')
        hostfile_compiler.read_hosts_file()


        hostfile_compiler.update_hosts_data(['123.123.123.123  foo.bar.local'])
        print('#################')
        print('#################')
        print('#################')
        compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
        print(compiled_hosts_file)


    def test_get_hosts_file_string__hosts_only_begining_of_xhosts_token(self):
        hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='./test_files/hosts_only_begining_of_xhosts_token')
        hostfile_compiler.read_hosts_file()


        hostfile_compiler.update_hosts_data(['123.123.123.123  foo.bar.local'])
        print('#################')
        print('#################')
        print('#################')
        compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
        print(compiled_hosts_file)


    def test_get_hosts_file_string__hosts_only_end_of_xhosts_token(self):
        hostfile_compiler = compiler.HostsFileCompiler(hosts_file_path='./test_files/hosts_only_end_of_xhosts_token')
        hostfile_compiler.read_hosts_file()


        hostfile_compiler.update_hosts_data(['123.123.123.123  foo.bar.local'])
        print('#################')
        print('#################')
        print('#################')
        compiled_hosts_file = hostfile_compiler.get_hosts_file_string()
        print(compiled_hosts_file)