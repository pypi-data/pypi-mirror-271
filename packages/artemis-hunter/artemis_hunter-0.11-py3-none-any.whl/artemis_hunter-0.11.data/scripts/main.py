#!python
import os
import re
import shlex
import argparse
from subprocess import Popen, PIPE
from typing import List, Dict, Union
from threading import Thread, Lock, current_thread


import toml
from bs4 import BeautifulSoup


class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'


class Utils:
    class ArtemisException(Exception):
        pass

    @staticmethod
    def make_directories(*args: str) -> None:
        """
        Makes a directory for each directory
        :param args:
        :return:
        """
        for directory in args:
            if os.path.isdir(directory):
                continue
            os.makedirs(directory)

    @staticmethod
    def clear_file(_file: str) -> None:
        """
        Clear file by writing an empty string into it
        :param _file:
        :return:
        """
        with open(_file, 'w') as f:
            f.write('')

    @staticmethod
    def determine_output_file(command: str, options_associated_with_output_file: List[str]) -> Union[str, None]:
        """
        Parses command for output file and returns...
            (1) the output file if determined
                        or
            (2) None, if output file can not determined
        :param command:
        :param options_associated_with_output_file:
        :return:
        """
        fragments = shlex.split(command)
        filepath = None

        for index, fragment in enumerate(fragments):
            if fragment.lower() in options_associated_with_output_file:
                if index + 1 >= len(fragments):
                    continue

                filepath = fragments[index + 1]
                return filepath
        return filepath

    @staticmethod
    def should_run_command(command_output_file: str) -> bool:
        """
        Should run command if:
            (1) the output file is None
                            or
            (2) the command's output file doesn't exist
        :param command_output_file:
        :return: a boolean value
        """
        if command_output_file is None:
            return True

        return not os.path.isfile(command_output_file)

    @staticmethod
    def extract_matching_string(regex: str, text: str) -> Union[str, None]:
        """
        Extracts the string which matches regex within a text
        :param regex:
        :param text:
        :return:
        """
        match = re.search(regex, text.lower())
        if match:
            return match.string
        else:
            return None

    @staticmethod
    def alpha_to_int(text):
        """
        Casts alpha numeric to an integer
        :param text:
        :return:
        """
        if text.isdigit():
            return int(text)
        return text

    @staticmethod
    def natural_keys(text):
        """
        Splits text into fragments and
        attempts to convert each text fragment into an integer
        example... natural_keys('["hello2world"') = ['hello', '2', 'world']
        :param text:
        :return:
        """
        return [Utils.alpha_to_int(c) for c in re.split('(\d+)', text)]


utils = Utils()


class Artemis:
    def __init__(
            self, ip_address, output_directory=None, config_directory=None,
            port_scan_type=None, nmap_extra=None, ports=None) -> None:
        self.thread_lock = Lock()
        self.address = ip_address
        self.port_scan_type = port_scan_type
        self.nmap_extra = nmap_extra
        self.ports = ports
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

        output_directory = output_directory or os.path.join(self.current_directory, 'results', self.address)
        config_directory = self.get_config(config_directory)
        port_scan_config_file = os.path.join(config_directory, 'port-scans.toml')
        services_scan_config_file = os.path.join(config_directory, 'service-scans.toml')
        universal_pattern_config_file = os.path.join(config_directory, 'universal-patterns.toml')

        if not os.path.isfile(port_scan_config_file):
            raise utils.ArtemisException(f'Can Not Find Port Scan Config File inside: {config_directory} Directory')
        if not os.path.isfile(services_scan_config_file):
            raise utils.ArtemisException(f'Can Not Find Services Scan Config File: {config_directory} Directory')
        if not os.path.isfile(universal_pattern_config_file):
            raise utils.ArtemisException(f'Can Not Find Universal Pattern Config File: {config_directory} Directory')

        self.port_scan_config = toml.load(port_scan_config_file)
        self.services_scan_config = toml.load(services_scan_config_file)
        self.universal_patterns = [value for value in toml.load(universal_pattern_config_file).values()]

        self.scan_directory = os.path.join(output_directory, 'scans')
        xml_directory = os.path.join(self.scan_directory, 'xml')
        log_directory = os.path.join(self.scan_directory, 'logs')
        exploit_directory = os.path.join(output_directory, 'exploit')
        priv_directory = os.path.join(output_directory, 'priv')
        loot_directory = os.path.join(output_directory, 'loot')
        utils.make_directories(
            self.scan_directory, xml_directory, log_directory,
            exploit_directory, priv_directory, loot_directory
        )

        self.detected_services = set()
        self.pattern_matches = dict()
        self.manual_scans = set()
        self.commands_ran = set()
        self.commands_run_log = os.path.join(log_directory, 'commands.log')
        self.detected_services_log = os.path.join(log_directory, 'detected_services.log')
        self.manual_steps_log = os.path.join(log_directory, 'manual_steps.log')
        self.patterns_detected_log = os.path.join(log_directory, 'patterns.log')
        utils.clear_file(self.manual_steps_log)

    def get_config(self, config_directory: str):
        # use user-specified artemis config directory
        if config_directory:
            return config_directory

        # use artemis config directory in home folder (if it exists)
        # checks ~/.config/artemis
        home_directory = os.path.expanduser("~")
        artemis_home_config_directory = os.path.join(home_directory, '.config', 'artemis')
        if os.path.exists(artemis_home_config_directory):
            return artemis_home_config_directory

        # use artemis config directory in current directory
        return os.path.join(self.current_directory, 'config')

    def print(self, _str: str) -> None:
        """
        Locks thread, prints, and releases thread
        so that printing output appears in the correct order
        :param _str:
        :return:
        """
        self.thread_lock.acquire()
        print(_str)
        self.thread_lock.release()

    def thread_print(self, _str: str) -> None:
        """
        Prints while prepending the thread id
        so it's more obvious where message came from
        :param _str:
        :return:
        """
        thread_id = current_thread().native_id
        _str = f"{Colors.CYAN}{Colors.BOLD}Thread {thread_id}:{Colors.END} {_str}"
        self.print(_str)

    def log_command(self, command: str) -> None:
        """
        Writes command to a log file
        :param command:
        :return:
        """
        thread_id = current_thread().native_id
        command = f"[*] (Thread {thread_id}) {command}\n\n"
        self.thread_lock.acquire()
        with open(self.commands_run_log, 'a') as f:
            f.write(command)
        self.thread_lock.release()

    def log_detected_services(self) -> None:
        """
        Write the detected services to a log file
        :return:
        """
        detected_services_list = list(self.detected_services)
        detected_services_list.sort(key=utils.natural_keys)

        with open(self.detected_services_log, 'w') as f:
            self.thread_lock.acquire()
            for detected_service in detected_services_list:
                f.write(f"{detected_service}\n")
            self.thread_lock.release()

    def log_manual_steps(self, manual_scans: List[Dict], service_scan_data: Dict) -> None:
        """
        Writes manual scans to a log file
        :param manual_scans:
        :param service_scan_data:
        :return:
        """
        with open(self.manual_steps_log, 'a') as f:
            self.thread_lock.acquire()
            for sub_scan in manual_scans:
                message = f"[*] {sub_scan['description']}\n"
                wrote_command = False

                for command in sub_scan['commands']:
                    command = command.format(**service_scan_data)
                    if command in self.manual_scans:
                        continue
                    wrote_command = True
                    self.manual_scans.add(command)
                    message += f"\t{command}\n"
                if wrote_command:
                    f.write(f"{message}\n\n")
            self.thread_lock.release()

    def record_pattern_matches(self, output_file: str, patterns: List[dict], service_data: dict) -> None:
        """
        Checks output file for patterns
        and then saves pattern description
        :param output_file:
        :param patterns:
        :param service_data:
        :return:
        """
        if 'port' in service_data:
            # since port scans don't specify a port, don't look at universal
            # patterns for port scans
            patterns_to_search = patterns + self.universal_patterns
        else:
            patterns_to_search = patterns

        if len(patterns_to_search) == 0:
            return

        with open(output_file, 'r') as f:
            for line in f:
                for pattern in patterns_to_search:
                    description = pattern['description']
                    pattern_regex = pattern['pattern'].lower()
                    match = utils.extract_matching_string(pattern_regex, line)
                    if match:
                        description = description.format(**service_data, match=match)
                        if output_file in self.pattern_matches:
                            self.pattern_matches[output_file].add(description)
                        else:
                            self.pattern_matches[output_file] = {description}
        self.log_recorded_patterns()

    def log_recorded_patterns(self) -> None:
        """
        Records patterns which were saved
        :return:
        """
        if len(self.pattern_matches) == 0:
            return

        pattern_description_shown = set()

        self.thread_lock.acquire()
        with open(self.patterns_detected_log, 'w') as f:
            for output_file in self.pattern_matches:
                unrepeated_pattern_present = False
                message = f"[*] Pattern/s detected in: '{output_file}'\n"
                for description in self.pattern_matches[output_file]:
                    if description in pattern_description_shown:
                        continue
                    pattern_description_shown.add(description)
                    message += f"\t[-] {description}\n"
                    unrepeated_pattern_present = True
                message += "\n"

                if unrepeated_pattern_present:
                    f.write(message)
        self.thread_lock.release()

    def run_command(self, command: str) -> None:
        """
        Executes a command
        :param command:
        :return:
        """
        self.log_command(command)
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        _, __ = process.communicate()

    def process_enumeration_command(
            self, command: str, service_data: dict, patterns: List[dict], _type: str = 'primary') -> None:
        """
        Executes command for primary or secondary enumeration
        :param command:
        :param service_data:
        :param patterns:
        :param _type:
        :return:
        """
        command = command.format(**service_data)
        if command in self.commands_ran:
            return

        output_file_flags = {
            'primary': ['-ox'],                 # flag associated with xml files
            'secondary': ['-on', 'tee', '-o', '--simple-report']   # flag associated with text files
        }
        output_file = utils.determine_output_file(command, output_file_flags[_type])
        if utils.should_run_command(output_file):
            self.commands_ran.add(command)
            command = 'sudo ' + command
            command_printed = f"{Colors.GREEN}{command}{Colors.END}"
            self.thread_print(command_printed)
            self.run_command(command)
            self.thread_print(f"{Colors.MAGENTA}{Colors.BOLD}Command Completed{Colors.END}")

        if output_file is None:
            return

        self.record_pattern_matches(output_file, patterns, service_data)
        if _type == 'primary':
            self.secondary_enumerate(output_file)

    def secondary_enumerate(self, xml_output_file: str) -> None:
        """
        Does secondary enumeration based on scans in the service-scans.toml in config folder.
        :param xml_output_file::
        :return:
        """
        if xml_output_file is None:
            return

        infile = open(xml_output_file, "r")
        contents = infile.read()
        soup = BeautifulSoup(contents, 'xml')
        ports = soup.find_all('port')

        for port in ports:
            state = port.find('state')
            if state['state'] == 'closed':
                continue

            service = port.find('service')
            service_scan_data = {
                'nmap_extra': self.nmap_extra,
                'scandir': self.scan_directory,
                'address': self.address,
                'port': port['portid'],
                'protocol': port['protocol'],
                'name': service['name'],
                'username_wordlist': self.services_scan_config['username_wordlist'],
                'password_wordlist': self.services_scan_config['password_wordlist'],
                'secure': True if 'ssl' in service or 'tls' in service else False,
                'scheme': 'https' if 'https' in service or 'ssl' in service or 'tls' in service else 'http'
            }

            self.detected_services.add(
                f"[*] {port['portid']}/{port['protocol']}: {service['name']}    ({state['state']})"
            )
            for service_name, scan in self.services_scan_config.items():
                if type(scan) != dict:
                    continue
                scan_regex_combined = "(" + ")|(".join(scan['service-names']) + ")"
                match = utils.extract_matching_string(scan_regex_combined, service['name'])
                if match is None:
                    continue

                if 'manual' in scan:
                    self.log_manual_steps(scan['manual'], service_scan_data)

                if 'scan' not in scan:
                    continue

                for sub_scan in scan['scan']:
                    command = sub_scan['command']
                    patterns = sub_scan.get('pattern', [])
                    th = Thread(
                        target=self.process_enumeration_command,
                        args=(command, service_scan_data, patterns, 'secondary')
                    )
                    th.start()
            self.log_detected_services()

    def enumerate(self) -> None:
        """
        Kicks off the primary enumeration process based on scans in the port-scans.toml file in the config folder.
        Note, once the primary scans are complete, secondary scans occur based on...
            (1) xml output of primary scans
                        and
            (2) information in the service-scans.toml file in the config folder.
        :return:
        """
        port_scan_data = {
            'nmap_extra': self.nmap_extra,
            'scandir': self.scan_directory,
            'address': self.address,
            'ports': self.ports,
        }
        for scan_name, scan in self.port_scan_config[self.port_scan_type].items():
            for sub_scan in scan.values():
                command = sub_scan['command']
                th = Thread(
                    target=self.process_enumeration_command,
                    args=(command, port_scan_data, [], 'primary')
                )
                th.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Does Enumeration')
    parser.add_argument('-i', '--ip_address', action='store', type=str,
                        dest='ip_address', help='IP Address', required=True)
    parser.add_argument('-c', '--config', action='store', type=str, dest='config_folder', help='Config Folder')
    parser.add_argument('-o', '--output', action='store', type=str, dest='output_folder', help='Output Folder')
    parser.add_argument(
        '--port_scan_type', action='store', type=str,
        default="default", choices=["default", "quick", "udp"],
        dest='port_scan_type', help='Select The Type of Port Scan'
    )
    parser.add_argument(
        '-ne', '--nmap_extra', action='store', type=str,
        dest='nmap_extra', help='Additional Nmap Args', default='-Pn'
    )
    parser.add_argument(
        '-p', '--ports', action='store', type=str,
        dest='ports', help='Ports to Scan', default='80'
    )
    args = parser.parse_args()
    artemis = Artemis(
        args.ip_address, args.output_folder, args.config_folder,
        args.port_scan_type, args.nmap_extra, args.ports
    )
    artemis.enumerate()
