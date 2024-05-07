#!/usr/bin/python3
"""
    Copyright (c) 2024 Penterep Security s.r.o.

    ptmultiviews - Apache Multiviews Detection & Enumeration Tool

    ptmultiviews is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ptmultiviews is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ptmultiviews.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import copy
import re
import sys
import urllib.parse; sys.path.append(__file__.rsplit("/", 1)[0])
import urllib

import requests

from _version import __version__
from ptlibs import ptjsonlib, ptmisclib, ptnethelper, ptprinthelper, ptpathtypedetector
from ptlibs.threads import ptthreads


class PtMultiviews:
    def __init__(self, args):
        self.ptjsonlib            = ptjsonlib.PtJsonLib()
        self.ptthreads            = ptthreads.PtThreads()
        self.ptpathtypedetector   = ptpathtypedetector.PtPathTypeDetector()
        self.without_domain       = args.without_domain
        self.with_requested_url   = args.with_requested_url
        self.use_json             = args.json
        self.timeout              = args.timeout
        self.cache                = args.cache
        self.redirects            = args.redirects
        self.output_file          = args.output
        self.proxies              = {"http": args.proxy, "https": args.proxy}
        self.headers              = ptnethelper.get_request_headers(args)

        # Test type
        self.url_test             = None
        self.file_test            = None
        self.url_file_test        = None
        self.domain_file_test     = None

        self.url_list             = self._get_urls_and_set_test_type(args)
        self.original_url_list    = copy.copy(self.url_list)
        self.result_path_list     = []


    def run(self, args):
        """Main method"""
        if self.url_test:
            # URL only test
            if self._is_vulnerable(self.url_list[0]) and not args.check_only:
                ptprinthelper.ptprint("Enumerated:", "TITLE", not self.use_json, newline_above=True, colortext=True)
                self.ptthreads.threads(self.url_list, self._enumerate_files, 1)

        elif self.url_file_test:
            # URL + Filepaths
            ptprinthelper.ptprint("Enumerated:", "TITLE", not self.use_json, newline_above=True, colortext=True)
            self.ptthreads.threads(self.url_list, self._enumerate_files, args.threads)

        elif self.file_test:
            # URLs from file
            ptprinthelper.ptprint("Enumerated:", "TITLE", not self.use_json, newline_above=True, colortext=True)
            self.ptthreads.threads(self.url_list, self._enumerate_files, args.threads)

        elif self.domain_file_test:
            # Domains from file
            ptprinthelper.ptprint("Vulnerable domains:", "TITLE", not self.use_json, newline_above=True, colortext=True)
            self.ptthreads.threads(self.url_list, self._is_vulnerable, args.threads)

        ptprinthelper.ptprint('\n'.join(sorted(self.result_path_list)), "", not self.use_json)

        if not self.result_path_list:
            ptprinthelper.ptprint("No alternatives to enumerate")

        if self.output_file:
            self._write_output_to_file(args.output)

        self.ptjsonlib.set_status("finished")
        ptprinthelper.ptprint(self.ptjsonlib.get_result_json(), condition=self.use_json)

    def _is_vulnerable(self, url: str) -> bool:
        """Checks whether <url> is vulnerable to multiviews"""
        malformed_url = self._strip_url_extension(url)
        try:
            response, response_dump = ptmisclib.load_url_from_web_or_temp(url=malformed_url, method="GET", headers=self.headers, proxies=self.proxies, timeout=self.timeout, redirects=self.redirects, verify=False, cache=self.cache, dump_response=True)
        except requests.exceptions.RequestException as e:
            if not self.domain_file_test: self.ptjsonlib.end_error(f"Cannot connect to website: {e}", self.use_json)
            return

        ptprinthelper.ptprint(f"Testing URL: {response.url}", "INFO", not self.use_json and not self.domain_file_test)
        ptprinthelper.ptprint(f"Status code: {response.status_code}", "INFO", not self.use_json and not self.domain_file_test)

        # Checks whether multiviews enabled
        if response.status_code in [200, 301, 302] and response.headers.get("Vary") and "negotiate" in response.headers.get("Vary"):
            if self.domain_file_test:
                ptprinthelper.ptprint(urllib.parse.urlparse(response.url).netloc, "", not self.use_json)
            ptprinthelper.ptprint(f"Multiviews: Enabled", "VULN", not self.use_json and not self.domain_file_test)
            self.ptjsonlib.add_vulnerability("PTV-WEB-DISCO-MVIEWS", vuln_request=response_dump["request"], vuln_response=response_dump["response"])
            return True
        else:
            ptprinthelper.ptprint(f"Multiviews: Disabled", "NOTVULN", not self.use_json and not self.domain_file_test)
            return False

    def _enumerate_files(self, url: str) -> None:
        """Enumerate files from URL"""
        original_url = url
        malformed_url = self._strip_url_extension(url)
        headers = dict({"Accept": "foo/foo"}, **self.headers)
        try:
            response = ptmisclib.load_url_from_web_or_temp(url=malformed_url, method="GET", headers=headers, proxies=self.proxies, timeout=self.timeout, redirects=self.redirects, verify=False, cache=self.cache)
        except requests.exceptions.RequestException as e:
            if self.url_test: self.ptjsonlib.end_error(f"Cannot connect to: {original_url}", self.use_json)
            return

        if response.status_code == 406:
            enumerated_files = re.findall('<a href="(.*)">', response.text)
            for found_file in enumerated_files:
                abs_path = f"{url.rsplit('/', 1)[0]}/{found_file}"
                rel_path = f"{url.split('/', 3)[-1]}/{found_file}"
                if abs_path == original_url and not self.with_requested_url:
                    continue
                path = abs_path if not self.without_domain else rel_path
                if path not in self.result_path_list:
                    self.result_path_list.append(path)
                    if self.use_json:
                        self.ptjsonlib.add_node(self.ptjsonlib.create_node_object("webpage", properties={"url": abs_path, "name": found_file, "WebPageType": self.ptpathtypedetector.get_type(path)}))

    def _strip_url_extension(self, url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.rsplit("/", 1)
        if "." in path[-1]:
            new_path = f"{path[0]}/{path[-1].split('.', 1)[0]}"
            parsed = parsed._replace(path=new_path)
        return urllib.parse.urlunparse(parsed)

    def _get_urls_and_set_test_type(self, args: argparse.Namespace) -> list:
        if args.url and not args.file and not args.domain_file:
            self.url_test = True
            return [self._parse_url(args.url)]

        elif (args.url and args.file) and not args.domain_file:
            self.url_file_test = True
            base_url =  args.url + "/" if not urllib.parse.urlparse(args.url).path.endswith("/") else args.url
            try:
                with open(args.file, 'r') as file:
                    url_list = [base_url + path.strip("/").strip() for line in file for path in [self.extract_path(line.strip())] if path.strip("/")]
                    return list(set(url_list))
            except (IOError, FileNotFoundError) as e:
                self.ptjsonlib.end_error(f"Cannot read file - {e}", self.use_json)

        elif args.file and not (args.url and args.domain):
            self.file_test = True
            try:
                with open(args.file, 'r') as file:
                    url_list = [line.strip() for line in file.readlines() if self._is_valid_url(line.strip())]
                    return list(set(url_list))
            except (IOError, FileNotFoundError) as e:
                self.ptjsonlib.end_error(f"Cannot read file - {e}", self.use_json)

        elif args.domain_file:
            if self.use_json: self.ptjsonlib.end_error("Cannot use --json option with -df/--domain-file", self.use_json)
            self.domain_file_test = True
            try:
                with open(args.domain_file, 'r') as file:
                    url_list = [f"https://{line.strip()}/favicon.ico" for line in file if line.strip()]
                    return url_list
            except (FileNotFoundError, IOError):
                self.ptjsonlib.end_error(f"Error reading from file - {args.domain_file}", self.use_json)

        else:
            self.ptjsonlib.end_error("Bad argument combination, see --help", self.use_json)

    def _is_valid_url(self, url):
        parsed = urllib.parse.urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def _adjust_domain(self, domain: str) -> str:
        """Adjusts provided <domain>"""
        parsed = urllib.parse.urlparse(domain)
        self._check_scheme(parsed.scheme)
        return domain + "/" if not parsed.path.endswith("/") else domain

    def _parse_url(self, url: str) -> str:
        """Checks whether the provided url is valid"""
        parsed = urllib.parse.urlparse(url)
        self._check_scheme(parsed.scheme)
        if len(parsed.path) in [0, 1]:
            self.ptjsonlib.end_error(f"URL with PATH to file is required (e.g. https://www.example.com/index.php)", self.use_json)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def _check_scheme(self, scheme: str) -> None:
        """Checks whether provided scheme is valid"""
        if not re.match("http[s]?$", scheme):
            self.ptjsonlib.end_error(f"Missing or invalid scheme, supported schemes are: [HTTP, HTTPS]", self.use_json)

    def extract_path(self, url_or_filepath):
        parsed = urllib.parse.urlparse(url_or_filepath)
        return parsed.path if parsed.scheme else url_or_filepath

    def _write_output_to_file(self, output_file):
        try:
            with open(output_file, 'a') as file:
                if self.result_path_list:
                    file.write('\n'.join(self.result_path_list) + "\n")
                ptprinthelper.ptprint(f"Output saved successfully to: {output_file}", "", not self.use_json, newline_above=True)
        except (FileNotFoundError, IOError) as e:
            ptprinthelper.ptprint(f"Cannot output to file - {e}", "ERROR", condition=not self.use_json)


def get_help():
    return [
        {"description": ["Apache Multiviews Detection & Enumeration Tool"]},
        {"usage": ["ptmultiviews <options>"]},
        {"tip": ["Use this program against existing web resources (eg. https://www.example.com/index.php)"]},
        {"usage_example": [
            "ptmultiviews -u https://www.example.com/",
            "ptmultiviews -u https://www.example.com/ --check-only",
            "ptmultiviews -d https://www.example.com/ -f filepaths.txt",
            "ptmultiviews -f urlList.txt",
            "ptmultiviews -df domainList.txt",
        ]},
        {"options": [
            ["-u",   "--url",                    "<url>",            "Connect to URL"],
            ["-f",   "--file",                   "<file>",           "Load list of URLs / filepaths"],
            ["-df",  "--domain-file",            "<domain-file>",    "Load list of domains to mass scan (defaults to favicon.ico)"],
            ["-co",  "--check-only",             "",                 "Check for multiviews without enumerating"],
            ["-wr",  "--with-requested-url",     "",                 "Include requested source among enumerated results"],
            ["-wd",  "--without-domain",         "",                 "Enumerated files will be printed without domain"],
            ["-t",   "--threads",                "<threads>",        "Set number of threads (default 20)"],
            ["-p",   "--proxy",                  "<proxy>",          "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-T",   "--timeout",                "<timeout>",        "Set timeout (default 10)"],
            ["-a",   "--user-agent",             "<agent>",          "Set User-Agent"],
            ["-c",   "--cookie",                 "<cookie>",         "Set Cookie(s)"],
            ["-H",   "--headers",                "<header:value>",   "Set Header(s)"],
            ["-o",   "--output",                 "<output>",         "Save output to file"],
            ["-r",   "--redirects",              "",                 "Follow redirects (default False)"],
            ["-C",   "--cache",                  "",                 "Cache HTTP communication (load from tmp in future)"],
            ["-v",   "--version",                "",                 "Show script version and exit"],
            ["-h",   "--help",                   "",                 "Show this help message and exit"],
            ["-j",   "--json",                   "",                 "Output in JSON format"],
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-u",  "--url",                  type=str)
    parser.add_argument("-d",  "--domain",               type=str)
    parser.add_argument("-df", "--domain-file",          type=str)
    parser.add_argument("-f",  "--file",                 type=str)
    parser.add_argument("-o",  "--output",               type=str)
    parser.add_argument("-T",  "--timeout",              type=int, default=10)
    parser.add_argument("-t",  "--threads",              type=int, default=20)
    parser.add_argument("-p",  "--proxy",                type=str)
    parser.add_argument("-c",  "--cookie",               type=str)
    parser.add_argument("-a",  "--user-agent",           type=str, default="Penterep Tools")
    parser.add_argument("-H",  "--headers",              type=ptmisclib.pairs)
    parser.add_argument("-co", "--check-only",           action="store_true")
    parser.add_argument("-wd", "--without-domain",       action="store_true")
    parser.add_argument("-wr", "--with-requested-url",   action="store_true")
    parser.add_argument("-r",  "--redirects",            action="store_true")
    parser.add_argument("-C",  "--cache",                action="store_true")
    parser.add_argument("-v",  "--version",              action="version", version=f"{SCRIPTNAME} {__version__}")
    parser.add_argument("-j",  "--json",                 action="store_true")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptprinthelper.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    ptprinthelper.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptmultiviews"
    requests.packages.urllib3.disable_warnings()
    args = parse_args()
    script = PtMultiviews(args)
    script.run(args)


if __name__ == "__main__":
    main()
