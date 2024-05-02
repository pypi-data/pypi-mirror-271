import os
import magic
import shutil
import hashlib
import logging
import requests
import subprocess
from bs4 import BeautifulSoup
from .base_handler import BaseHandler
from urllib.parse import urlparse, parse_qs
from ..common import PackageManager, temp_directory
from ..utils import download_file, temp_directory, extract_tar


class GolangHandler(BaseHandler):
    def fetch(self):
        self.base_url = "https://github.com/"
        repo_url = self.construct_repo_url()
        with temp_directory() as temp_dir:
            self.temp_dir = temp_dir
            if self.purl_details['subpath']:
                self.fetch_file(repo_url)
                logging.info(f"File downloaded in {self.temp_dir}")
                self.unpack()
            else:
                self.clone_repo(repo_url)
                logging.info(f"Repo cloned to {self.temp_dir}")
            self.scan()

    def find_github_links(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            github_links = [
                link['href'] for link in links if 'github.com' in link['href']
            ]
            if github_links:
                gh_link = github_links[0]
                parts = gh_link.split('/')
                if 'tree' in parts:
                    index = parts.index('tree')
                    parts = parts[:index]
                    return '/'.join(parts)
                else:
                    return gh_link
            else:
                return ''
        except requests.RequestException as e:
            logging.error(f"An error occurred while accessing the URL: {e}")
            exit()

    def construct_repo_url(self):
        GOLANG_REPOS = {
            "go.mongodb.org": self.base_url + "mongodb/",
            "google.golang.org": self.base_url + "golang/",
            "github.com": (
                self.base_url + self.purl_details['fullparts'][2] + "/"
            )
        }
        namespace = self.purl_details['namespace']
        if namespace in GOLANG_REPOS:
            base_url = GOLANG_REPOS[namespace]
            full_url = base_url + self.purl_details['name']
        else:
            full_url = f"https://{namespace}/{self.purl_details['name']}"
            full_url = self.find_github_links(full_url)
        # Default to main if no version is provided
        version = self.purl_details.get('version', 'main')
        return f"{full_url}.git", version

    def unpack(self):
        if self.temp_dir:
            package_file_path = os.path.join(
                self.temp_dir,
                "downloaded_file"
            )
            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(package_file_path)
            if 'gzip' in mimetype:
                extract_tar(package_file_path, self.temp_dir)
                logging.info(f"Unpacked package in {self.temp_dir}")
            else:
                logging.error(f"MimeType not supported {mimetype}")
                logging.error(f"Error unpacking file in {self.temp_dir}")
                exit()

    def scan(self):
        results = {}
        logging.info("Scanning package contents...")
        files = PackageManager.scan_for_files(
            self.temp_dir, ['COPYRIGHT', 'NOTICES', 'LICENSE', 'COPYING']
        )
        results['license_files'] = files
        copyhits = PackageManager.scan_for_copyright(self.temp_dir)
        results['copyrights'] = copyhits
        self.results = results

    def generate_report(self):
        logging.info("Generating report based on the scanned data...")
        return self.results

    def fetch_file(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_data = response.content
            package_file_path = os.path.join(
                self.temp_dir,
                "downloaded_file"
            )
            with open(package_file_path, "wb") as file:
                file.write(file_data)
            logging.info("File downloaded successfully.")
        else:
            raise ConnectionError("Failed to download the file.")

    def clone_repo(self, repo_url):
        repo = repo_url[0]
        try:
            subprocess.run(
                ["git", "clone", repo, self.temp_dir],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if self.purl_details['version']:
                version = self.purl_details['version']
                subprocess.run(
                    ["git", "-C", self.temp_dir, "checkout", version],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            logging.info(f"Repository cloned successfully to {self.temp_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e}")
            # shutil.rmtree(self.temp_dir)
            raise
