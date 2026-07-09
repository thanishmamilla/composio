import json
import os

def build_html():
    print("Building compiled HTML Case Study...")
    
    # Check if data exists
    if not os.path.exists("results_verified.json"):
        print("results_verified.json not found, running verification first...")
        import verify_agent
        verify_agent.run_verification()
        
    with open("results_verified.json", "r") as f:
        verified_data = json.load(f)
        
    with open("verification_metrics.json", "r") as f:
        metrics_data = json.load(f)
        
    # Calculate statistics for charts
    categories = list(set([app["category"] for app in verified_data]))
    
    auth_counts = {}
    access_counts = {"Self-serve": 0, "Gated": 0}
    verdict_counts = {"Buildable": 0, "Gated": 0, "Blocked": 0}
    mcp_counts = {"Yes": 0, "No": 0}
    
    for app in verified_data:
        # Auth Methods
        for auth in app["auth_methods"]:
            auth_counts[auth] = auth_counts.get(auth, 0) + 1
        # Access Type
        access_counts[app["access_type"]] = access_counts.get(app["access_type"], 0) + 1
        # Verdict
        verdict_counts[app["buildability_verdict"]] = verdict_counts.get(app["buildability_verdict"], 0) + 1
        # MCP
        mcp_key = "Yes" if app["mcp_exists"] else "No"
        mcp_counts[mcp_key] = mcp_counts.get(mcp_key, 0) + 1

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Composio Integration Intelligence | 100 Apps Case Study</title>
    <meta name="description" content="AI Product Ops Intern case study researching API surfaces, auth protocols, and buildability patterns across 100 major platforms using an autonomous agent pipeline.">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {{
            --bg: #060913;
            --surface: #0c1020;
            --surface-elevated: #131930;
            --border: rgba(255, 255, 255, 0.05);
            --border-hover: rgba(255, 255, 255, 0.12);
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.15);
            --warning: #f59e0b;
            --warning-glow: rgba(245, 158, 11, 0.15);
            --danger: #ef4444;
            --danger-glow: rgba(239, 68, 68, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
            scroll-behavior: smooth;
        }}

        body {{
            background: radial-gradient(circle at 50% 0%, #0f172e 0%, #060913 100%);
            background-color: var(--bg);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.6;
            padding-bottom: 5rem;
        }}

        /* Subtle grid background overlay */
        body::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: radial-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 24px 24px;
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            max-width: 1300px;
            margin: 0 auto;
            padding: 0 2.5rem;
            position: relative;
            z-index: 1;
        }}

        /* Header / Brand */
        header {{
            padding: 4.5rem 0 2rem 0;
        }}

        .header-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.85rem;
            font-weight: 800;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
        }}

        .header-brand .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-gradient);
            box-shadow: 0 0 10px #3b82f6;
        }}

        header h1 {{
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.15;
            background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
        }}

        header p.subtitle {{
            font-size: 1.15rem;
            color: var(--text-secondary);
            max-width: 750px;
            font-weight: 400;
        }}

        /* Bento Box Grid */
        .bento-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
            margin-top: 2.5rem;
        }}

        @media (max-width: 1024px) {{
            .bento-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 640px) {{
            .bento-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .bento-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .bento-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: transparent;
            transition: all 0.3s ease;
        }}

        .bento-card:hover {{
            transform: translateY(-4px);
            border-color: var(--border-hover);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        }}

        .bento-card:hover::before {{
            background: var(--accent-gradient);
        }}

        .bento-card .label {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1.25rem;
        }}

        .bento-card .value-container {{
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }}

        .bento-card .value {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }}

        .bento-card .sub-value {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .progress-bar-container {{
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.05);
            border-radius: 999px;
            margin-top: 1rem;
            overflow: hidden;
        }}

        .progress-bar {{
            height: 100%;
            border-radius: 999px;
            background: var(--accent-gradient);
        }}

        .pulsing-indicator {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.75rem;
            font-size: 0.85rem;
            color: var(--success);
            font-weight: 600;
        }}

        .pulsing-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
            animation: pulse 1.8s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}

        /* Dynamic Navigation Bar */
        .nav-sticky {{
            position: sticky;
            top: 0;
            background: rgba(6, 9, 19, 0.75);
            backdrop-filter: blur(12px);
            z-index: 100;
            border-bottom: 1px solid var(--border);
            margin: 3rem 0 2.5rem 0;
        }}

        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 4rem;
        }}

        .tabs-nav {{
            display: flex;
            gap: 0.5rem;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.6rem 1.2rem;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.03);
        }}

        .tab-btn.active {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Section Cards / Containers */
        .glass-panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.25rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }}

        .glass-panel h3 {{
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.01em;
            margin-bottom: 1.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text-primary);
        }}

        .glass-panel h3 svg {{
            color: var(--accent-blue);
        }}

        /* Insights Tab Style */
        .insight-layout {{
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }}

        @media (max-width: 1024px) {{
            .insight-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        .insight-cards-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
        }}

        @media (max-width: 640px) {{
            .insight-cards-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .insight-mini-card {{
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.25s ease;
        }}

        .insight-mini-card:hover {{
            background: rgba(255, 255, 255, 0.02);
            border-color: var(--border-hover);
        }}

        .insight-mini-card .card-icon {{
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: rgba(59, 130, 246, 0.08);
            color: var(--accent-blue);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }}

        .insight-mini-card h4 {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }}

        .insight-mini-card p {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Executive Charts Panel */
        .charts-box-layout {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
        }}

        @media (max-width: 768px) {{
            .charts-box-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-card {{
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            min-height: 300px;
        }}

        .chart-card h4 {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }}

        .chart-render-wrapper {{
            flex-grow: 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Interactive Matrix Filter Board */
        .filter-board {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border);
            padding: 1.25rem;
            border-radius: 14px;
            align-items: center;
        }}

        .search-field {{
            flex-grow: 2;
            min-width: 280px;
            position: relative;
        }}

        .search-field input {{
            width: 100%;
            background: rgba(6, 9, 19, 0.5);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1rem 0.75rem 2.75rem;
            border-radius: 10px;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.25s ease;
        }}

        .search-field input:focus {{
            border-color: var(--accent-blue);
            background: rgba(6, 9, 19, 0.8);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }}

        .search-magnifier {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }}

        .custom-select {{
            background: rgba(6, 9, 19, 0.5);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 500;
            outline: none;
            cursor: pointer;
            min-width: 160px;
            transition: all 0.25s ease;
        }}

        .custom-select:focus {{
            border-color: var(--accent-blue);
            background: rgba(6, 9, 19, 0.8);
        }}

        .count-tag {{
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.04);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            margin-left: auto;
        }}

        /* Table Design */
        .table-view-box {{
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: var(--surface);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        }}

        table.matrix-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            text-align: left;
            font-size: 0.95rem;
        }}

        table.matrix-table th {{
            background: rgba(255, 255, 255, 0.015);
            padding: 1.1rem 1.5rem;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border);
        }}

        table.matrix-table td {{
            padding: 1.1rem 1.5rem;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
            color: #d1d5db;
        }}

        table.matrix-table tbody tr {{
            transition: all 0.2s ease;
        }}

        table.matrix-table tbody tr:hover {{
            background: rgba(255, 255, 255, 0.015);
            cursor: pointer;
            transform: scale(0.998);
        }}

        table.matrix-table tbody tr:last-child td {{
            border-bottom: none;
        }}

        .name-txt {{
            font-weight: 700;
            color: var(--text-primary);
        }}

        .sub-cat-txt {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        /* Badges & Pills */
        .pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .pill-blue {{
            background: rgba(59, 130, 246, 0.08);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.15);
        }}

        .pill-green {{
            background: rgba(16, 185, 129, 0.08);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.15);
        }}

        .pill-yellow {{
            background: rgba(245, 158, 11, 0.08);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.15);
        }}

        .pill-red {{
            background: rgba(239, 68, 68, 0.08);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.15);
        }}

        .pill-purple {{
            background: rgba(139, 92, 246, 0.08);
            color: #a78bfa;
            border: 1px solid rgba(139, 92, 246, 0.15);
        }}

        .mcp-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .mcp-active {{ color: var(--success); }}
        .mcp-inactive {{ color: var(--text-muted); }}

        .mcp-circle {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }}

        .bg-mcp-active {{ background: var(--success); box-shadow: 0 0 6px var(--success); }}
        .bg-mcp-inactive {{ background: var(--text-muted); }}

        .table-action-btn {{
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 0.45rem 0.9rem;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .table-action-btn:hover {{
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--text-secondary);
            color: var(--text-primary);
        }}

        /* Sliding Detail Drawer */
        .drawer-overlay {{
            position: fixed;
            top: 0; right: 0; bottom: 0; left: 0;
            background: rgba(4, 6, 12, 0.7);
            backdrop-filter: blur(8px);
            z-index: 999;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .drawer-overlay.active {{
            opacity: 1;
            visibility: visible;
        }}

        .drawer {{
            position: fixed;
            top: 0; right: -580px; bottom: 0;
            width: 100%;
            max-width: 550px;
            background: var(--surface);
            border-left: 1px solid var(--border);
            box-shadow: -15px 0 40px rgba(0,0,0,0.6);
            z-index: 1000;
            padding: 3rem;
            overflow-y: auto;
            transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .drawer.active {{
            right: 0;
        }}

        .drawer-close {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            color: var(--text-primary);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 1.75rem;
            right: 1.75rem;
            transition: all 0.2s ease;
        }}

        .drawer-close:hover {{
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
            color: var(--danger);
        }}

        .drawer-header {{
            margin-top: 1.5rem;
            margin-bottom: 2rem;
        }}

        .drawer-header h2 {{
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.2;
            color: var(--text-primary);
            margin-top: 0.5rem;
        }}

        .drawer-header .sub-info {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }}

        .drawer-block {{
            border-top: 1px solid var(--border);
            padding: 1.5rem 0;
        }}

        .drawer-block h4 {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
        }}

        .drawer-block p, .drawer-block div {{
            font-size: 0.95rem;
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .drawer-evidence {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--accent-blue);
            text-decoration: none;
            font-weight: 600;
            margin-top: 0.5rem;
            transition: color 0.2s ease;
            font-size: 0.95rem;
        }}

        .drawer-evidence:hover {{
            color: var(--accent-purple);
            text-decoration: underline;
        }}

        /* Flowchart styling for Research Agent tab */
        .flow-board {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 2rem 0;
        }}

        .flow-card {{
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.25rem;
            position: relative;
        }}

        .flow-num {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--accent-gradient);
            color: white;
            font-weight: 800;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }}

        .flow-info h5 {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }}

        .flow-info p {{
            font-size: 0.88rem;
            color: var(--text-secondary);
        }}

        /* Coding Terminal mockup */
        .terminal {{
            background: #05070f;
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-top: 1.5rem;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}

        .terminal-header {{
            background: rgba(255, 255, 255, 0.02);
            padding: 0.75rem 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .terminal-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }}

        .terminal-red {{ background: #ff5f56; }}
        .terminal-yellow {{ background: #ffbd2e; }}
        .terminal-green {{ background: #27c93f; }}

        .terminal-title {{
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            margin-left: auto;
        }}

        .terminal-body {{
            padding: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            color: #34d399;
            line-height: 1.6;
            overflow-x: auto;
        }}

        .terminal-prompt {{
            color: var(--accent-blue);
        }}

        /* Verification Table styling */
        .verify-log-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            margin-top: 1.5rem;
        }}

        .verify-log-table th, .verify-log-table td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
            text-align: left;
        }}

        .verify-log-table th {{
            color: var(--text-secondary);
            font-weight: 700;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: rgba(255, 255, 255, 0.01);
        }}

        .verify-grid {{
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 2rem;
        }}

        @media (max-width: 1024px) {{
            .verify-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* General SVGs */
        .svg-asset {{
            width: 20px;
            height: 20px;
            fill: currentColor;
            vertical-align: middle;
        }}

        footer {{
            text-align: center;
            padding: 4rem 0;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
            margin-top: 6rem;
        }}
    </style>
</head>
<body>

    <header>
        <div class="container">
            <div class="header-brand">
                <span class="dot"></span>
                Composio Case Study
            </div>
            <h1>Integration Intelligence Matrix</h1>
            <p class="subtitle">An analysis of authorization APIs, developer access models, and MCP compatibility across 100 platforms, powered by an agentic audit and verification pipeline.</p>
        </div>
    </header>

    <div class="nav-sticky">
        <div class="container nav-container">
            <div class="tabs-nav">
                <button class="tab-btn active" onclick="switchTab('insights')">Executive Summary & Patterns</button>
                <button class="tab-btn" onclick="switchTab('directory')">Interactive Findings Matrix</button>
                <button class="tab-btn" onclick="switchTab('agent')">The Research Agent & Verification</button>
            </div>
        </div>
    </div>

    <main class="container">
        <!-- Section 1: Executive Summary & Patterns -->
        <section id="insights" class="tab-content active">
            <div class="insight-layout">
                <div class="glass-panel" style="margin-bottom:0;">
                    <h3>
                        <svg class="svg-asset" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
                        Headline Insights & Market Patterns
                    </h3>
                    <div class="insight-cards-grid">
                        <div class="insight-mini-card">
                            <div class="card-icon">
                                <svg class="svg-asset" viewBox="0 0 24 24"><path d="M12.65 11.65l2.79-2.79-2.29-2.29-2.79 2.79-.88-.88 2.79-2.79-2.29-2.29-2.79 2.79-.88-.88 3.67-3.67 6.84 6.84zM12 22c5.52 0 10-4.48 10-10H2c0 5.52 4.48 10 10 10z"/></svg>
                            </div>
                            <h4>Auth Consolidation</h4>
                            <p>Modern cloud APIs are highly standardized around <strong>OAuth2</strong> (52%) and <strong>API Keys</strong> (41%). Traditional basic credentials (10%) are legacy patterns mostly restricted to enterprise environments.</p>
                        </div>
                        <div class="insight-mini-card">
                            <div class="card-icon">
                                <svg class="svg-asset" viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
                            </div>
                            <h4>Self-Serve Access</h4>
                            <p><strong>70%</strong> of target applications are self-serve, enabling free trials or testing immediately. <strong>30%</strong> are gated under custom sales pipelines, enterprise pricing tiers, or corporate approvals.</p>
                        </div>
                        <div class="insight-mini-card">
                            <div class="card-icon">
                                <svg class="svg-asset" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                            </div>
                            <h4>Strategic Blockers</h4>
                            <p>The primary blocker for tool integrations is the complete absence of a public developer API surface (**9%** of apps, including consumer-facing tools like NotebookLM and closed suites like fanbasis).</p>
                        </div>
                        <div class="insight-mini-card">
                            <div class="card-icon">
                                <svg class="svg-asset" viewBox="0 0 24 24"><path d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z"/></svg>
                            </div>
                            <h4>MCP Acceleration</h4>
                            <p>An encouraging **30%** of requesting platforms (Notion, Slack, Stripe, Vercel, Supabase) already offer active Model Context Protocol (MCP) server configurations for rapid tool integration.</p>
                        </div>
                    </div>
                </div>

                <div class="glass-panel" style="margin-bottom:0; display:flex; flex-direction:column; justify-content:space-between;">
                    <h3>
                        <svg class="svg-asset" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15H9v-2h2v2zm0-4H9V7h2v6zm4 4h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                        Roadmap Feasibility
                    </h3>
                    <div class="chart-card" style="min-height:190px; padding:1.25rem; margin-bottom:1rem;">
                        <h4 style="margin-bottom:0.75rem;">Buildability Verdicts</h4>
                        <div class="chart-render-wrapper">
                            <canvas id="verdictChart"></canvas>
                        </div>
                    </div>
                    <div class="chart-card" style="min-height:190px; padding:1.25rem;">
                        <h4 style="margin-bottom:0.75rem;">Developer Access Models</h4>
                        <div class="chart-render-wrapper">
                            <canvas id="accessChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <div class="glass-panel">
                <h3>
                    <svg class="svg-asset" viewBox="0 0 24 24"><path d="M12 22c5.52 0 10-4.48 10-10S17.52 2 12 2 2 6.48 2 12s4.48 10 10 10zm1-15h-2v2h2V7zm0 4h-2v6h2v-6z"/></svg>
                    Authentication & Protocol Distribution
                </h3>
                <div class="charts-box-layout">
                    <div class="chart-card">
                        <h4>Auth Protocol Frequencies</h4>
                        <div class="chart-render-wrapper">
                            <canvas id="authChart"></canvas>
                        </div>
                    </div>
                    <div class="chart-card">
                        <h4>Active MCP Support</h4>
                        <div class="chart-render-wrapper">
                            <canvas id="mcpChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section 2: Interactive Findings Matrix -->
        <section id="directory" class="tab-content">
            <div class="filter-board">
                <div class="search-field">
                    <svg class="search-magnifier svg-asset" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                    <input type="text" id="searchBar" onkeyup="filterData()" placeholder="Filter by platform, description, auth mechanism, or documentation link...">
                </div>
                
                <select id="categoryFilter" onchange="filterData()" class="custom-select">
                    <option value="">All Categories</option>
                    {"".join([f'<option value="{c}">{c}</option>' for c in categories])}
                </select>

                <select id="authFilter" onchange="filterData()" class="custom-select">
                    <option value="">All Auth Methods</option>
                    <option value="OAuth2">OAuth2</option>
                    <option value="API Key">API Key</option>
                    <option value="Basic">Basic</option>
                    <option value="token">Token</option>
                    <option value="other">Other/None</option>
                </select>

                <select id="accessFilter" onchange="filterData()" class="custom-select">
                    <option value="">All Access Types</option>
                    <option value="Self-serve">Self-serve</option>
                    <option value="Gated">Gated</option>
                </select>

                <select id="verdictFilter" onchange="filterData()" class="custom-select">
                    <option value="">All Feasibility</option>
                    <option value="Buildable">Buildable</option>
                    <option value="Gated">Gated Blocker</option>
                    <option value="Blocked">Blocked</option>
                </select>

                <div class="count-tag" id="resultsCount">Showing 100 of 100 apps</div>
            </div>

            <div class="table-view-box">
                <table class="matrix-table" id="appsTable">
                    <thead>
                        <tr>
                            <th>Platform Name</th>
                            <th>Category</th>
                            <th>Auth Mechanisms</th>
                            <th>Developer Access</th>
                            <th>Feasibility</th>
                            <th>MCP Configuration</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Section 3: The Research Agent & Verification -->
        <section id="agent" class="tab-content">
            <div class="verify-grid">
                <div class="glass-panel" style="margin-bottom:0;">
                    <h3>
                        <svg class="svg-asset" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                        Research Agent Architecture
                    </h3>
                    <p class="insight-text" style="font-size:0.95rem; margin-bottom:1.5rem; color:var(--text-secondary);">An automated Python framework was constructed utilizing the <strong>Composio SDK</strong> and <strong>Gemini 1.5 Flash</strong> to scrape and parse documentation page-by-page.</p>
                    
                    <div class="flow-board">
                        <div class="flow-card">
                            <div class="flow-num">1</div>
                            <div class="flow-info">
                                <h5>Input Config Seeding</h5>
                                <p>Loads `apps_list.json` containing targets and web address hints.</p>
                            </div>
                        </div>
                        <div class="flow-card">
                            <div class="flow-num">2</div>
                            <div class="flow-info">
                                <h5>Composio Tool Search & Scrape</h5>
                                <p>Launches crawler search and scraping sessions to fetch dev API landing pages.</p>
                            </div>
                        </div>
                        <div class="flow-card">
                            <div class="flow-num">3</div>
                            <div class="flow-info">
                                <h5>Structured Extraction Loop</h5>
                                <p>Feeds markdown search payloads to Gemini, validating extraction schema via Pydantic mapping.</p>
                            </div>
                        </div>
                        <div class="flow-card">
                            <div class="flow-num">4</div>
                            <div class="flow-info">
                                <h5>Verification & Human-in-the-Loop Overlay</h5>
                                <p>Audits anomalies programmatically, cross-checking gated enterprise platforms and applying manual correction logic.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="glass-panel" style="margin-bottom:0; display:flex; flex-direction:column;">
                    <div class="verification-header">
                        <h3 style="margin-bottom:0;">
                            <svg class="svg-asset" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                            Accuracy & Verification Loop
                        </h3>
                        <div class="accuracy-box">
                            <div class="accuracy-value">{metrics_data["final_accuracy"]}%</div>
                            <div class="accuracy-lbl">Final Accuracy</div>
                        </div>
                    </div>
                    
                    <p class="insight-text" style="font-size:0.95rem; margin-top:1.5rem; margin-bottom:1.25rem; color:var(--text-secondary);">
                        To prove the reliability of the findings, a **15-app random sample (15%)** was manually audited. 
                    </p>
                    <p class="insight-text" style="font-size:0.95rem; margin-bottom:1.5rem; color:var(--text-secondary);">
                        **Iterative Accuracy Performance:**
                        The unverified first-pass agent run achieved **{metrics_data["first_pass_accuracy"]}%** accuracy. The agent misclassified complex platforms like **DealCloud** and **Otter AI** due to the presence of public documentation portals that mask underlying commercial client walls. 
                        Applying our verification rules and human overlay successfully caught these cases, adjusting accuracy to **{metrics_data["final_accuracy"]}%** (with **fanbasis** remaining as a noted honest miss).
                    </p>

                    <h5 style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:0.5rem;">Sample Audit Report Log</h5>
                    <div style="flex-grow:1; overflow-y:auto; max-height:260px; border: 1px solid var(--border); border-radius:10px;">
                        <table class="verify-log-table">
                            <thead>
                                <tr>
                                    <th>App Name</th>
                                    <th>First Pass Result</th>
                                    <th>Verification Action</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {"".join([f'<tr><td><span style="font-weight:700;">{res["name"]}</span></td><td>{"❌ Faulty Extraction" if res["status"] == "Corrected" else "✅ Verified"}</td><td>{"Corrected via Manual Rules" if res["status"] == "Corrected" else "Passed Check"}</td><td><span class="pill pill-{"green" if res["status"] == "Pass" else "yellow"}" style="padding:0.15rem 0.5rem; font-size:0.65rem; margin:0;">{"Pass" if res["status"] == "Pass" else "Corrected"}</span></td></tr>' for res in metrics_data["sampled_results"]])}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="glass-panel" style="margin-top:2rem;">
                <h3>
                    <svg class="svg-asset" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
                    Source Code Instructions
                </h3>
                <p class="insight-text" style="font-size:0.95rem; color:var(--text-secondary);">The agent pipeline is designed to execute locally with minimal configuration:</p>
                
                <div class="terminal">
                    <div class="terminal-header">
                        <span class="terminal-dot terminal-red"></span>
                        <span class="terminal-dot terminal-yellow"></span>
                        <span class="terminal-dot terminal-green"></span>
                        <span class="terminal-title">bash - research_agent</span>
                    </div>
                    <div class="terminal-body">
<span class="terminal-prompt">$</span> pip install composio google-generativeai duckduckgo-search python-dotenv beautifulsoup4
<br><span class="terminal-prompt">$</span> echo "GEMINI_API_KEY=your_key_here" > .env
<br><span class="terminal-prompt">$</span> python research_agent.py --refresh
<br><span class="terminal-prompt">$</span> python verify_agent.py
<br><span class="terminal-prompt">$</span> python build_index.py
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Details View Drawer Overlay -->
    <div class="drawer-overlay" id="drawerOverlay" onclick="closeDrawer()"></div>
    <div class="drawer" id="detailDrawer">
        <button class="drawer-close" onclick="closeDrawer()">✕</button>
        <div class="drawer-header">
            <span class="pill" id="drawerVerdictBadge">Buildable</span>
            <h2 id="drawerAppName">Salesforce</h2>
            <div class="sub-info" id="drawerCategory">CRM and Sales</div>
        </div>
        
        <div class="drawer-block">
            <h4>Application Purpose</h4>
            <p id="drawerDescription">Customer relationship management suite.</p>
        </div>

        <div class="drawer-block">
            <h4>API Credentials & Auth Protocol</h4>
            <div id="drawerAuthMethods">OAuth2, API Key</div>
        </div>

        <div class="drawer-block">
            <h4>Developer Access Policies</h4>
            <p id="drawerAccessType" style="font-weight:700; margin-bottom:0.25rem;">Self-serve</p>
            <p id="drawerAccessDetail" style="color:var(--text-secondary);">Credentials require a business account.</p>
        </div>

        <div class="drawer-block">
            <h4>API Surface Analysis</h4>
            <p id="drawerApiSurface" style="color:var(--text-secondary);">REST, SOAP endpoints.</p>
        </div>

        <div class="drawer-block">
            <h4>Model Context Protocol (MCP)</h4>
            <p id="drawerMcp">No standard MCP available.</p>
        </div>

        <div class="drawer-block" id="drawerBlockerSection">
            <h4>Main Blocker</h4>
            <p id="drawerBlocker" style="color:var(--danger); font-weight:600;">None</p>
        </div>

        <div class="drawer-block">
            <h4>Evidence Reference</h4>
            <a href="#" id="drawerEvidenceUrl" class="drawer-evidence" target="_blank">
                Open Developer API Reference
                <svg class="svg-asset" viewBox="0 0 24 24" style="width:14px; height:14px;"><path d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-8z"/></svg>
            </a>
        </div>
    </div>

    <footer>
        <p>© 2026 Composio Integration Matrix. Hand-crafted by Product Ops Candidate. Powered by Agentic Pipelines.</p>
    </footer>

    <script>
        // Compiled database mapping
        const appData = {json.dumps(verified_data)};

        // Tab selection logic
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        // Matrix rendering engine
        function renderTable(data) {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            if(data.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:3rem; color:var(--text-muted); font-weight:500;">No applications matched the requested query filters.</td></tr>';
                return;
            }}

            data.forEach(app => {{
                const authBadges = app.auth_methods.map(a => `<span class="pill pill-purple" style="margin-right:0.35rem; margin-bottom:0.25rem; font-size:0.68rem; text-transform:none;">${{a}}</span>`).join('');
                
                let accessBadge = '';
                if(app.access_type === 'Self-serve') {{
                    accessBadge = '<span class="pill pill-green">Self-serve</span>';
                }} else {{
                    accessBadge = '<span class="pill pill-yellow">Gated</span>';
                }}

                let verdictBadge = '';
                if(app.buildability_verdict === 'Buildable') {{
                    verdictBadge = '<span class="pill pill-green">Buildable</span>';
                }} else if (app.buildability_verdict === 'Gated') {{
                    verdictBadge = '<span class="pill pill-yellow">Gated</span>';
                }} else {{
                    verdictBadge = '<span class="pill pill-red">Blocked</span>';
                }}

                const mcpBadge = app.mcp_exists ? 
                    `<span class="mcp-indicator mcp-active"><span class="mcp-circle bg-mcp-active"></span>Active MCP</span>` : 
                    `<span class="mcp-indicator mcp-inactive"><span class="mcp-circle bg-mcp-inactive"></span>Not Configured</span>`;

                const tr = document.createElement('tr');
                tr.onclick = () => openDrawer(app.name);
                tr.innerHTML = `
                    <td>
                        <div class="name-txt">${{app.name}}</div>
                        <div class="sub-cat-txt">${{app.hint}}</div>
                    </td>
                    <td class="sub-cat-txt" style="font-weight:600; color:var(--text-secondary);">${{app.category}}</td>
                    <td>${{authBadges}}</td>
                    <td>${{accessBadge}}</td>
                    <td>${{verdictBadge}}</td>
                    <td>${{mcpBadge}}</td>
                    <td><button class="table-action-btn" onclick="event.stopPropagation(); openDrawer('${{app.name}}')">Details</button></td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Dynamic multi-filtering algorithm
        function filterData() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            const category = document.getElementById('categoryFilter').value;
            const auth = document.getElementById('authFilter').value;
            const access = document.getElementById('accessFilter').value;
            const verdict = document.getElementById('verdictFilter').value;

            const filtered = appData.filter(app => {{
                const matchesSearch = app.name.toLowerCase().includes(query) || 
                                      app.description.toLowerCase().includes(query) ||
                                      app.blocker.toLowerCase().includes(query) ||
                                      app.evidence_url.toLowerCase().includes(query);
                
                const matchesCategory = category === '' || app.category === category;
                const matchesAuth = auth === '' || app.auth_methods.includes(auth) || (auth === 'other' && app.auth_methods.includes('other'));
                const matchesAccess = access === '' || app.access_type === access;
                const matchesVerdict = verdict === '' || app.buildability_verdict === verdict;

                return matchesSearch && matchesCategory && matchesAuth && matchesAccess && matchesVerdict;
            }});

            renderTable(filtered);
            document.getElementById('resultsCount').innerText = `Showing ${{filtered.length}} of ${{appData.length}} apps`;
        }}

        // Sidebar Sliding Drawer Engine
        function openDrawer(appName) {{
            const app = appData.find(a => a.name === appName);
            if(!app) return;

            document.getElementById('drawerAppName').innerText = app.name;
            document.getElementById('drawerCategory').innerText = app.category;
            document.getElementById('drawerDescription').innerText = app.description;
            
            // Auth badges
            const authContainer = document.getElementById('drawerAuthMethods');
            authContainer.innerHTML = app.auth_methods.map(a => `<span class="pill pill-purple" style="text-transform:none; margin-right:0.35rem; margin-bottom:0.25rem;">${{a}}</span>`).join('');
            
            // Access details
            document.getElementById('drawerAccessType').innerText = app.access_type;
            document.getElementById('drawerAccessDetail').innerText = app.access_detail;
            
            // API surface details
            document.getElementById('drawerApiSurface').innerText = app.api_surface;
            
            // MCP URL
            const mcpContainer = document.getElementById('drawerMcp');
            if(app.mcp_exists) {{
                mcpContainer.innerHTML = `✅ Existing MCP Server: <a href="https://${{app.mcp_url}}" target="_blank" style="color:var(--accent-blue); font-weight:600; text-decoration:none;">${{app.mcp_url}}</a>`;
            }} else {{
                mcpContainer.innerHTML = '❌ No standard MCP server exists for this platform today.';
            }}

            // Blocker details
            const blockerSection = document.getElementById('drawerBlockerSection');
            const blockerText = document.getElementById('drawerBlocker');
            if(app.buildability_verdict === 'Buildable') {{
                blockerSection.style.display = 'none';
            }} else {{
                blockerSection.style.display = 'block';
                blockerText.innerText = app.blocker;
            }}

            // Evidence URL
            document.getElementById('drawerEvidenceUrl').href = app.evidence_url;

            // Verdict badge class styling
            const badge = document.getElementById('drawerVerdictBadge');
            badge.className = 'pill';
            if(app.buildability_verdict === 'Buildable') {{
                badge.classList.add('pill-green');
                badge.innerText = 'Buildable';
            }} else if (app.buildability_verdict === 'Gated') {{
                badge.classList.add('pill-yellow');
                badge.innerText = 'Gated';
            }} else {{
                badge.classList.add('pill-red');
                badge.innerText = 'Blocked';
            }}

            document.getElementById('drawerOverlay').classList.add('active');
            document.getElementById('detailDrawer').classList.add('active');
        }}

        function closeDrawer() {{
            document.getElementById('drawerOverlay').classList.remove('active');
            document.getElementById('detailDrawer').classList.remove('active');
        }}

        // Render Custom Charts on initialization
        window.onload = function() {{
            renderTable(appData);

            // Chart global defaults configuration
            Chart.defaults.color = '#94a3b8';
            Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

            // 1. Verdict Chart
            new Chart(document.getElementById('verdictChart'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Buildable', 'Gated', 'Blocked'],
                    datasets: [{{
                        data: [{verdict_counts["Buildable"]}, {verdict_counts["Gated"]}, {verdict_counts["Blocked"]}],
                        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{ boxWidth: 12, font: {{ size: 10, weight: 600 }} }}
                        }}
                    }}
                }}
            }});

            // 2. Access Chart
            new Chart(document.getElementById('accessChart'), {{
                type: 'pie',
                data: {{
                    labels: ['Self-serve', 'Gated'],
                    datasets: [{{
                        data: [{access_counts["Self-serve"]}, {access_counts["Gated"]}],
                        backgroundColor: ['#3b82f6', '#8b5cf6'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{ boxWidth: 12, font: {{ size: 10, weight: 600 }} }}
                        }}
                    }}
                }}
            }});

            // 3. Auth Chart (Horizontal Bar Chart)
            const sortedAuths = Object.entries({json.dumps(auth_counts)})
                .sort((a,b) => b[1] - a[1]);
            
            new Chart(document.getElementById('authChart'), {{
                type: 'bar',
                data: {{
                    labels: sortedAuths.map(x => x[0]),
                    datasets: [{{
                        data: sortedAuths.map(x => x[1]),
                        backgroundColor: '#8b5cf6',
                        borderRadius: 5,
                        barThickness: 15
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(255,255,255,0.03)' }}, ticks: {{ font: {{ size: 10 }} }} }},
                        y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10, weight: 600 }} }} }}
                    }}
                }}
            }});

            // 4. MCP Support Chart
            new Chart(document.getElementById('mcpChart'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Active MCP', 'No MCP Configuration'],
                    datasets: [{{
                        data: [{mcp_counts["Yes"]}, {mcp_counts["No"]}],
                        backgroundColor: ['#10b981', 'rgba(255,255,255,0.04)'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ boxWidth: 12, font: {{ size: 10, weight: 600 }} }}
                        }}
                    }}
                }}
            }});
        }};
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Compiled HTML file created: index.html.")

if __name__ == "__main__":
    build_html()
