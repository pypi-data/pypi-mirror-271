"""
Vulnerabilities Integration
"""

import json
import logging
import os
from datetime import timedelta, datetime
from typing import List, Dict, Optional

from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import get_current_datetime, check_file_path
from regscale.integrations.commercial.wiz.constants import VULNERABILITY_QUERY, CONTENT_TYPE, VULNERABILITY_FILE_PATH
from regscale.models.regscale_models import Vulnerability, Asset, SecurityPlan, ScanHistory
from regscale.utils import PaginatedGraphQLClient

logger = logging.getLogger(__name__)


class VulnerabilitiesIntegration:
    """
    Fetches vulnerabilities from Wiz
    """

    def __init__(
        self,
        wiz_project_id: str,
        parent_id: int,
        scan_tool: str,
        parent_module: str = SecurityPlan.get_module_slug(),
        filter_by_override: str = None,
    ):
        self.parent_id = parent_id
        self.parent_module = parent_module
        self.app = Application()
        self.scan_tool = scan_tool
        self.name = "Vulnerabilities"
        self.query = VULNERABILITY_QUERY
        self.findings: List[Vulnerability] = []
        self.assets: List[Asset] = []
        self.asset_dict = {}
        self.scan_history: Optional[ScanHistory] = None
        self.low = 0
        self.medium = 0
        self.high = 0
        self.critical = 0
        self.filter_by = {"projectId": wiz_project_id.split(",")}
        if filter_by_override:
            self.filter_by = json.loads(filter_by_override)
        self.variables = {
            "first": 1000,
            "filterBy": self.filter_by,
            "fetchTotalCount": False,
        }

    def run(self):
        """
        Fetches vulnerabilities from Wiz and creates them in the application
        """
        self.fetch_assets()
        self.create_scan_history()
        fetched_findings = self.fetch_vulnerabilities()
        self.update_counts()
        logger.info(f"Found total of {len(fetched_findings)} vulnerabilities from Wiz.")
        vulnerabilities = Vulnerability.batch_create(items=fetched_findings)
        logger.info(f"Created total of {len(vulnerabilities)} vulnerabilities from Wiz.")

    def fetch_assets(self):
        """
        Fetches assets from the application
        """
        self.assets = Asset.get_all_by_parent(parent_id=self.parent_id, parent_module=self.parent_module)
        self.asset_dict = {asset.wizId: asset for asset in self.assets} if self.assets else {}

    def set_severity_count(self, severity: str):
        """
        Increments the count of the severity
        :param str severity: Severity of the vulnerability
        """
        if severity == "LOW":
            self.low += 1
        elif severity == "MEDIUM":
            self.medium += 1
        elif severity == "HIGH":
            self.high += 1
        elif severity == "CRITICAL":
            self.critical += 1

    def update_counts(self):
        """
        Updates the counts of the vulnerabilities in the scan history
        """
        if not self.scan_history:
            return
        self.scan_history.vLow = self.low
        self.scan_history.vMedium = self.medium
        self.scan_history.vHigh = self.high
        self.scan_history.vCritical = self.critical
        self.scan_history.save()

    def fetch_vulnerabilities(self) -> List[Vulnerability]:
        """
        Fetches vulnerabilities from Wiz
        :returns: List of Vulnerabilities
        :rtype: List[Vulnerability]
        """
        return self.fetch_data_if_needed()

    def fetch_data_if_needed(self) -> List[Vulnerability]:
        """
        Fetches data if the file is not present or is older than the fetch interval
        :returns: List of Vulnerabilities
        :rtype: List[Vulnerability]
        """
        fetch_interval = timedelta(hours=1)  # Interval to fetch new data
        current_time = datetime.now()

        # Check if the file exists and its last modified time
        if os.path.exists(VULNERABILITY_FILE_PATH):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(VULNERABILITY_FILE_PATH))
            if current_time - file_mod_time < fetch_interval:
                return self.load_file()
        nodes = self.fetch_wiz_data()
        self.write_to_file(nodes)
        for node in nodes:
            self.map_node_to_vulnerability(node)
        return self.findings

    @staticmethod
    def write_to_file(nodes: List[Dict]):
        """
        Writes the nodes to a file
        :param List[Dict] nodes: List of nodes to write
        """
        check_file_path("artifacts")
        with open(VULNERABILITY_FILE_PATH, "w") as file:
            json.dump(nodes, file)

    def load_file(self) -> List[Vulnerability]:
        """
        Loads the file and maps the nodes to Vulnerability objects
        Returns: List of Vulnerabilities
        :rtype: List[Vulnerability]
        """
        check_file_path("artifacts")
        with open(VULNERABILITY_FILE_PATH, "r") as file:
            nodes = json.load(file)
            for node in nodes:
                self.map_node_to_vulnerability(node)
            return self.findings

    def map_node_to_vulnerability(self, node: Dict):
        """
        Maps the node to a Vulnerability object
        :param Dict node: Node from the Wiz API
        """
        asset = self.asset_dict.get(node.get("vulnerableAsset", {}).get("id"))
        self.set_severity_count(node.get("severity", "").upper())
        self.findings.append(
            Vulnerability(
                uuid=node.get("id"),
                title=node.get("name"),
                description=node.get("description"),
                severity=node.get("severity"),
                cve=node.get("cve"),
                cvsSv3BaseScore=node.get("score"),
                firstSeen=node.get("firstDetectedAt"),
                lastSeen=node.get("lastDetectedAt"),
                exploitAvailable=node.get("hasExploit", False),
                parentId=asset.id if asset else self.scan_history.id,
                parentModule="assets" if asset else "scanhistory",
                dns=node.get("name"),
                ipAddress="unknown",
                mitigated=False,
                port="",
                plugInId=0,
                scanId=self.scan_history.id,
            )
        )

    def fetch_wiz_data(self) -> List[Dict]:
        """
        Fetches data from Wiz
        :returns: List of nodes
        :rtype: List[Dict]
        """
        client = None
        api_endpoint_url = self.app.config.get("wizUrl")
        if token := self.app.config.get("wizAccessToken"):
            client = PaginatedGraphQLClient(
                endpoint=api_endpoint_url,
                query=self.query,
                headers={
                    "Content-Type": CONTENT_TYPE,
                    "Authorization": "Bearer " + token,
                },
            )
        # Fetch all results using the client's pagination logic
        data = client.fetch_all(variables=self.variables, topic_key="vulnerabilityFindings") if client else []
        return data

    def create_scan_history(self):
        """
        Creates scan history record
        """
        self.scan_history = ScanHistory(
            scanningTool=self.scan_tool,
            parentId=self.parent_id,
            parentModule=self.parent_module,
            scanDate=get_current_datetime(),
        ).create()
