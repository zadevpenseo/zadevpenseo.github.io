#!/usr/bin/env python3
"""
generate_report_pdf.py
Executive Jira Weekly Report PDF Generator.
Renders responsive HTML5/CSS and vector SVG into an executive-grade A4 PDF via Playwright.
"""

import asyncio
import json
from pathlib import Path
from jira_client import JiraClient
from metrics_engine import MetricsEngine

PROTOTYPE_DIR = Path(__file__).parent
OUTPUT_PDF = PROTOTYPE_DIR / "jira_weekly_executive_report.pdf"
OUTPUT_HTML = PROTOTYPE_DIR / "report_preview.html"


def generate_burndown_svg(burndown: list, total_pts: float) -> str:
    vw, vh = 500, 180
    margin_l, margin_r, margin_t, margin_b = 40, 20, 20, 30
    plot_w = vw - margin_l - margin_r
    plot_h = vh - margin_t - margin_b

    max_val = max(total_pts, 1.0)
    n = len(burndown)

    ideal_points = []
    actual_points = []

    for idx, item in enumerate(burndown):
        x = margin_l + (idx / (n - 1)) * plot_w
        y_ideal = margin_t + plot_h - (item["ideal"] / max_val) * plot_h
        y_actual = margin_t + plot_h - (item["actual"] / max_val) * plot_h
        ideal_points.append(f"{x:.1f},{y_ideal:.1f}")
        actual_points.append(f"{x:.1f},{y_actual:.1f}")

    ideal_line = " ".join(ideal_points)
    actual_line = " ".join(actual_points)

    x_labels = "".join(
        f'<text x="{margin_l + (i / (n - 1)) * plot_w:.1f}" y="{vh - 8}" text-anchor="middle" font-size="10" fill="#64748B">{item["day"]}</text>'
        for i, item in enumerate(burndown)
    )

    y_grid = "".join(
        f'<line x1="{margin_l}" y1="{margin_t + (k / 3) * plot_h:.1f}" x2="{vw - margin_r}" y2="{margin_t + (k / 3) * plot_h:.1f}" stroke="#E2E8F0" stroke-dasharray="3,3"/>'
        f'<text x="{margin_l - 8}" y="{margin_t + (k / 3) * plot_h + 3:.1f}" text-anchor="end" font-size="9" fill="#94A3B8">{round(max_val * (1 - k / 3)):.0f}</text>'
        for k in range(4)
    )

    return f"""
    <svg viewBox="0 0 {vw} {vh}" class="chart-svg" xmlns="http://www.w3.org/2000/svg">
        {y_grid}
        <!-- Ideal Burn line -->
        <polyline points="{ideal_line}" fill="none" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5,4" />
        <!-- Actual Burn line -->
        <polyline points="{actual_line}" fill="none" stroke="#6366F1" stroke-width="3" stroke-linecap="round" />
        {x_labels}
        <!-- Legend -->
        <circle cx="340" cy="12" r="4" fill="#94A3B8" />
        <text x="350" y="15" font-size="10" fill="#64748B">Ideal Burn</text>
        <circle cx="420" cy="12" r="4" fill="#6366F1" />
        <text x="430" y="15" font-size="10" fill="#1E293B" font-weight="600">Actual Remaining</text>
    </svg>
    """


def build_html_report(metrics: dict) -> str:
    burndown_svg = generate_burndown_svg(metrics["burndown"], metrics["total_points"])

    dev_rows = ""
    for d in metrics["developers"]:
        logged = d["hours_logged"]
        est = d["hours_estimated"]
        pct = min(round((logged / est * 100), 0) if est > 0 else 0, 150)
        bar_color = "#10B981" if logged <= est else "#F59E0B"
        dev_rows += f"""
        <tr>
            <td style="font-weight: 600; color: #1E293B;">{d['developer']}</td>
            <td><span class="badge completed">{d['tasks_completed']} Done</span></td>
            <td><span class="badge active">{d['tasks_active']} Active</span></td>
            <td style="font-family: monospace; font-weight: 600;">{logged}h / {est}h</td>
            <td style="width: 140px;">
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {min(pct, 100)}%; background-color: {bar_color};"></div>
                </div>
            </td>
        </tr>
        """

    issue_rows = ""
    for issue in metrics["completed_issues"]:
        issue_rows += f"""
        <tr>
            <td style="font-family: monospace; font-weight: 700; color: #4338CA;">{issue['key']}</td>
            <td style="color: #334155;">{issue['summary']}</td>
            <td><span class="badge type-{issue['type'].lower()}">{issue['type']}</span></td>
            <td style="color: #475569;">{issue['assignee']}</td>
            <td style="font-weight: 600; color: #0F172A;">{issue['story_points']} pts</td>
            <td style="font-family: monospace; color: #10B981; font-weight: 600;">{issue['time_spent_hours']}h</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Jira Weekly Executive Report - {metrics['sprint_name']}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm 14mm 16mm 14mm;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #FFFFFF;
            color: #0F172A;
            line-height: 1.45;
            font-size: 11pt;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .header-title h1 {{
            font-size: 20pt;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.02em;
        }}
        .header-title p {{
            font-size: 9.5pt;
            color: #64748B;
            margin-top: 3px;
        }}
        .header-badge {{
            background: linear-gradient(135deg, #4338CA, #6366F1);
            color: #FFFFFF;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 9pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 16px;
        }}
        .kpi-card {{
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 10px 12px;
        }}
        .kpi-label {{
            font-size: 8pt;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .kpi-value {{
            font-size: 17pt;
            font-weight: 800;
            color: #0F172A;
            margin-top: 2px;
        }}
        .kpi-subtext {{
            font-size: 7.5pt;
            color: #10B981;
            font-weight: 600;
            margin-top: 1px;
        }}
        .section-title {{
            font-size: 11pt;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .section-title::before {{
            content: "";
            display: inline-block;
            width: 4px;
            height: 13px;
            background-color: #6366F1;
            border-radius: 2px;
        }}
        .burndown-container {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 16px;
        }}
        .chart-svg {{
            width: 100%;
            height: 140px;
            display: block;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            margin-bottom: 16px;
        }}
        th {{
            background-color: #F1F5F9;
            color: #475569;
            text-align: left;
            padding: 7px 10px;
            font-weight: 700;
            font-size: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 1px solid #CBD5E1;
        }}
        td {{
            padding: 7px 10px;
            border-bottom: 1px solid #F1F5F9;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 7.5pt;
            font-weight: 700;
        }}
        .badge.completed {{ background-color: #DCFCE7; color: #166534; }}
        .badge.active {{ background-color: #FEF3C7; color: #92400E; }}
        .badge.type-story {{ background-color: #E0E7FF; color: #3730A3; }}
        .badge.type-bug {{ background-color: #FEE2E2; color: #991B1B; }}
        .badge.type-task {{ background-color: #F1F5F9; color: #334155; }}
        .progress-bar-bg {{
            width: 100%;
            height: 7px;
            background-color: #E2E8F0;
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        .footer {{
            margin-top: 14px;
            padding-top: 8px;
            border-top: 1px solid #E2E8F0;
            display: flex;
            justify-content: space-between;
            font-size: 7.5pt;
            color: #94A3B8;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            <h1>Weekly Developer Performance Report</h1>
            <p><strong>{metrics['sprint_name']}</strong> &bull; Goal: {metrics['sprint_goal']}</p>
        </div>
        <div class="header-badge">Executive Delivery</div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Sprint Velocity</div>
            <div class="kpi-value">{metrics['completed_points']} / {metrics['total_points']}</div>
            <div class="kpi-subtext">{metrics['completion_rate']}% Target Accomplished</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Completed Tasks</div>
            <div class="kpi-value">{metrics['completed_count']} <span style="font-size: 10pt; color: #64748B;">/ {metrics['total_issues']}</span></div>
            <div class="kpi-subtext">+{metrics['completed_count']} Issues Closed</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Time Spent</div>
            <div class="kpi-value">{metrics['total_hours_spent']}h</div>
            <div class="kpi-subtext">Est: {metrics['total_hours_est']}h ({'+' if metrics['estimation_variance'] >= 0 else ''}{metrics['estimation_variance']}h variance)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Active / In Review</div>
            <div class="kpi-value">{metrics['in_progress_count'] + metrics['in_review_count']}</div>
            <div class="kpi-subtext" style="color: #6366F1;">On Track for Sprint Close</div>
        </div>
    </div>

    <div class="section-title">Sprint Burndown Progression</div>
    <div class="burndown-container">
        {burndown_svg}
    </div>

    <div class="section-title">Developer Workload & Hours Logged</div>
    <table>
        <thead>
            <tr>
                <th>Developer</th>
                <th>Completed</th>
                <th>In Progress</th>
                <th>Logged vs Estimate</th>
                <th>Capacity Allocation</th>
            </tr>
        </thead>
        <tbody>
            {dev_rows}
        </tbody>
    </table>

    <div class="section-title">Key Completed Deliverables</div>
    <table>
        <thead>
            <tr>
                <th>Issue Key</th>
                <th>Summary</th>
                <th>Type</th>
                <th>Assignee</th>
                <th>Story Points</th>
                <th>Time Spent</th>
            </tr>
        </thead>
        <tbody>
            {issue_rows}
        </tbody>
    </table>

    <div class="footer">
        <div>Automated Jira Executive Pipeline &bull; Grounded in Deterministic Analytics</div>
        <div>Generated for Stakeholder Review &bull; Confidential</div>
    </div>
</body>
</html>
"""


async def main():
    client = JiraClient(offline=True)
    raw_data = client.fetch_sprint_data()
    metrics = MetricsEngine.compute_sprint_metrics(raw_data)

    html_content = build_html_report(metrics)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"[*] HTML Report generated at: {OUTPUT_HTML}")

    # Render PDF via Playwright
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_content, wait_until="networkidle")
            await page.pdf(
                path=str(OUTPUT_PDF),
                format="A4",
                print_background=True,
                margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
            )
            await browser.close()
            print(f"[SUCCESS] Executive PDF Report compiled at: {OUTPUT_PDF}")
    except Exception as e:
        print(f"[!] Playwright compilation error: {e}. HTML report remains available at: {OUTPUT_HTML}")


if __name__ == "__main__":
    asyncio.run(main())
