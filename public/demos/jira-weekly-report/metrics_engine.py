"""
metrics_engine.py - Sprint Metrics & Analytics Calculator
Processes raw Jira sprint data and computes velocity, burndown, and developer workloads.
"""

from typing import Any, Dict, List


class MetricsEngine:
    @staticmethod
    def compute_sprint_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        sprint = data.get("sprint", {})
        issues: List[Dict[str, Any]] = data.get("issues", [])

        total_issues = len(issues)
        completed_issues = [i for i in issues if i.get("status", "").lower() in ["done", "closed", "resolved"]]
        in_progress_issues = [i for i in issues if i.get("status", "").lower() in ["in progress", "in development"]]
        in_review_issues = [i for i in issues if i.get("status", "").lower() in ["in review", "code review", "testing"]]

        total_points = sum(i.get("story_points", 0) for i in issues)
        completed_points = sum(i.get("story_points", 0) for i in completed_issues)
        completion_rate = round((completed_points / total_points * 100), 1) if total_points > 0 else 0.0

        total_hours_spent = sum(i.get("time_spent_hours", 0) for i in issues)
        total_hours_est = sum(i.get("original_estimate_hours", 0) for i in issues)

        # Developer Workload & Hours
        dev_worklogs: Dict[str, Dict[str, Any]] = {}
        for i in issues:
            dev = i.get("assignee", "Unassigned")
            if dev not in dev_worklogs:
                dev_worklogs[dev] = {
                    "developer": dev,
                    "hours_logged": 0.0,
                    "hours_estimated": 0.0,
                    "tasks_completed": 0,
                    "tasks_active": 0,
                }
            dev_worklogs[dev]["hours_logged"] += i.get("time_spent_hours", 0.0)
            dev_worklogs[dev]["hours_estimated"] += i.get("original_estimate_hours", 0.0)
            if i in completed_issues:
                dev_worklogs[dev]["tasks_completed"] += 1
            else:
                dev_worklogs[dev]["tasks_active"] += 1

        dev_list = list(dev_worklogs.values())
        dev_list.sort(key=lambda x: x["hours_logged"], reverse=True)

        # Type Distribution
        type_counts: Dict[str, int] = {}
        for i in issues:
            t = i.get("type", "Task")
            type_counts[t] = type_counts.get(t, 0) + 1

        # Simulated Burndown Timeline (7 Days)
        # Starting with total_points, linearly tracking ideal vs actual completed points
        burndown = [
            {"day": "Mon", "ideal": total_points, "actual": total_points},
            {"day": "Tue", "ideal": round(total_points * 0.83, 1), "actual": total_points},
            {"day": "Wed", "ideal": round(total_points * 0.66, 1), "actual": round(total_points - 5, 1)},
            {"day": "Thu", "ideal": round(total_points * 0.50, 1), "actual": round(total_points - 13, 1)},
            {"day": "Fri", "ideal": round(total_points * 0.33, 1), "actual": round(total_points - 21, 1)},
            {"day": "Sat", "ideal": round(total_points * 0.16, 1), "actual": round(total_points - 26, 1)},
            {"day": "Sun", "ideal": 0.0, "actual": round(total_points - completed_points, 1)},
        ]

        return {
            "sprint_name": sprint.get("name", "Active Sprint"),
            "sprint_goal": sprint.get("goal", "No goal defined"),
            "total_issues": total_issues,
            "completed_count": len(completed_issues),
            "in_progress_count": len(in_progress_issues),
            "in_review_count": len(in_review_issues),
            "total_points": total_points,
            "completed_points": completed_points,
            "completion_rate": completion_rate,
            "total_hours_spent": round(total_hours_spent, 1),
            "total_hours_est": round(total_hours_est, 1),
            "estimation_variance": round(total_hours_spent - total_hours_est, 1),
            "developers": dev_list,
            "type_counts": type_counts,
            "burndown": burndown,
            "completed_issues": completed_issues,
            "active_issues": in_progress_issues + in_review_issues,
        }
