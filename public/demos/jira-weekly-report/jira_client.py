"""
jira_client.py - Dual-Mode Jira Connector
Fetches Jira Agile Sprint data and Worklogs via REST API or falls back to synthetic fixture.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.parse
import base64

logger = logging.getLogger("jira_client")

FIXTURE_PATH = Path(__file__).parent / "mock_jira_data.json"


class JiraClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        offline: bool = False,
    ):
        self.base_url = (base_url or os.getenv("JIRA_BASE_URL", "")).rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL", "")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN", "")
        self.offline = offline or not (self.base_url and self.email and self.api_token)

    def _get_auth_headers(self) -> Dict[str, str]:
        auth_str = f"{self.email}:{self.api_token}"
        encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        return {
            "Authorization": f"Basic {encoded_auth}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "JiraWeeklyReporter/1.0",
        }

    def fetch_sprint_data(self, board_id: Optional[int] = None, sprint_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieves sprint information, issues, and worklog hours.
        Falls back to local mock data if running in offline mode.
        """
        if self.offline:
            logger.info("Operating in Offline/Mock mode. Loading synthetic Sprint data...")
            with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)

        logger.info(f"Connecting to live Jira instance at {self.base_url}...")
        try:
            # 1. Fetch active sprint if not specified
            if not sprint_id and board_id:
                sprint_url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint?state=active"
                req = urllib.request.Request(sprint_url, headers=self._get_auth_headers())
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    values = data.get("values", [])
                    if values:
                        sprint_id = values[0]["id"]

            if not sprint_id:
                raise ValueError("Active sprint ID could not be resolved.")

            # 2. Fetch issues in sprint
            issues_url = f"{self.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue?maxResults=100"
            req = urllib.request.Request(issues_url, headers=self._get_auth_headers())
            with urllib.request.urlopen(req, timeout=15) as resp:
                issues_data = json.loads(resp.read().decode("utf-8"))

            parsed_issues = []
            for item in issues_data.get("issues", []):
                fields = item.get("fields", {})
                time_spent_sec = fields.get("timespent") or 0
                original_est_sec = fields.get("timeoriginalestimate") or 0
                assignee_obj = fields.get("assignee") or {}
                
                parsed_issues.append({
                    "key": item.get("key"),
                    "summary": fields.get("summary", ""),
                    "type": fields.get("issuetype", {}).get("name", "Task"),
                    "status": fields.get("status", {}).get("name", "To Do"),
                    "assignee": assignee_obj.get("displayName", "Unassigned"),
                    "story_points": fields.get("customfield_10016") or 0,
                    "original_estimate_hours": round(original_est_sec / 3600, 1),
                    "time_spent_hours": round(time_spent_sec / 3600, 1),
                    "completed_at": fields.get("resolutiondate"),
                })

            return {
                "sprint": {
                    "id": sprint_id,
                    "name": f"Sprint #{sprint_id}",
                    "state": "active",
                },
                "issues": parsed_issues,
            }
        except Exception as e:
            logger.warning(f"Failed to fetch live Jira data: {e}. Falling back to fixture.")
            with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
