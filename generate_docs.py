import os

files_to_include = [
    "app.py",
    "engine/health_score.py",
    "engine/fraud_check.py",
    "engine/goal_tracker.py",
    "data/portfolio.py",
    "data/sebi_registry.py",
    "data/goals.py",
    "data/verified_content.py",
    "static/js/app.js",
    "static/js/i18n.js",
    "static/css/index.css",
    "static/css/components.css",
    "templates/base.html",
    "templates/app_shell.html",
    "templates/dashboard.html",
    "templates/portfolio.html",
    "templates/health_score.html",
    "templates/fraud_shield.html",
    "templates/verified_voices.html",
    "templates/goals.html"
]

output_path = r"C:\Users\LOQ\.gemini\antigravity-ide\brain\18f607b0-a4ce-4089-b6a0-927be04d450a\project_code.md"

with open(output_path, "w", encoding="utf-8") as out:
    out.write("# RiskLens Python Project Code\n\n")
    out.write("This document contains all the primary source code files for the RiskLens Python Flask conversion, organized by directory.\n\n")
    
    for fpath in files_to_include:
        if os.path.exists(fpath):
            ext = os.path.splitext(fpath)[1][1:]
            if ext == 'py':
                lang = 'python'
            elif ext == 'html':
                lang = 'html'
            elif ext == 'js':
                lang = 'javascript'
            elif ext == 'css':
                lang = 'css'
            else:
                lang = ''
                
            out.write(f"## `{fpath}`\n\n")
            out.write(f"```{lang}\n")
            with open(fpath, "r", encoding="utf-8") as infile:
                out.write(infile.read())
            out.write("\n```\n\n")

print("Created artifact!")
