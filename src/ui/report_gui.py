#!/usr/bin/env python3
"""Simple Tkinter GUI for reporting bugs and feature requests.

Saves reports to ~/.winpatable/reports/ as JSON and optionally opens the
GitHub new-issue page prefilled with title/body. If the environment
variable `WINPATABLE_GITHUB_TOKEN` is set and the user opts in, the GUI
can POST the issue using the API (user opt-in required).
"""

import os
import json
import time
import webbrowser
import platform
import getpass
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception:
    tk = None

REPO = 'thomasboy2017/Winpatable-'


def ensure_report_dir() -> Path:
    d = Path.home() / '.winpatable' / 'reports'
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_report(rtype: str, title: str, description: str) -> Path:
    d = ensure_report_dir()
    timestamp = int(time.time())
    filename = f"{rtype}_{timestamp}.json"
    path = d / filename

    system_summary = {
        'user': getpass.getuser(),
        'platform': platform.platform(),
        'python': platform.python_version()
    }

    report = {
        'type': rtype,
        'title': title,
        'description': description,
        'system': system_summary,
        'created_at': timestamp
    }

    with open(path, 'w') as fh:
        json.dump(report, fh, indent=2)

    return path


def open_github_issue_page(title: str, body: str):
    url = f"https://github.com/{REPO}/issues/new?title={quote(title)}&body={quote(body)}"
    webbrowser.open(url)


def quote(s: str) -> str:
    from urllib.parse import quote as _q
    return _q(s)


def try_create_github_issue(title: str, body: str) -> bool:
    """Attempt to create a GitHub issue using a token in env var.

    Returns True if created, False otherwise.
    """
    token = os.environ.get('WINPATABLE_GITHUB_TOKEN')
    if not token:
        return False

    import urllib.request
    import urllib.error

    api_url = f"https://api.github.com/repos/{REPO}/issues"
    payload = json.dumps({'title': title, 'body': body}).encode('utf-8')
    req = urllib.request.Request(api_url, data=payload, method='POST')
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            # On success, data contains 'html_url'
            if 'html_url' in data:
                webbrowser.open(data['html_url'])
                return True
    except Exception:
        return False

    return False


def launch_gui():
    if tk is None:
        print("GUI not available: tkinter could not be imported on this system.")
        return

    root = tk.Tk()
    root.title('Winpatable - Report Bug / Feature')
    root.geometry('700x520')

    frm = ttk.Frame(root, padding=12)
    frm.pack(fill='both', expand=True)

    ttk.Label(frm, text='Report Type:').grid(column=0, row=0, sticky='w')
    rtype = tk.StringVar(value='bug')
    ttk.Radiobutton(frm, text='Bug', variable=rtype, value='bug').grid(column=1, row=0, sticky='w')
    ttk.Radiobutton(frm, text='Feature', variable=rtype, value='feature').grid(column=2, row=0, sticky='w')

    ttk.Label(frm, text='Title:').grid(column=0, row=1, sticky='w', pady=(8,0))
    title_entry = ttk.Entry(frm, width=80)
    title_entry.grid(column=0, row=2, columnspan=6, sticky='we')

    ttk.Label(frm, text='Description:').grid(column=0, row=3, sticky='w', pady=(8,0))
    desc = tk.Text(frm, height=18, wrap='word')
    desc.grid(column=0, row=4, columnspan=6, sticky='nsew')

    # GitHub options
    # Token can be provided via env var or saved token file
    token_path = Path.home() / '.winpatable' / 'github_token'
    env_token = os.environ.get('WINPATABLE_GITHUB_TOKEN')
    file_token = None
    if token_path.exists():
        try:
            file_token = token_path.read_text().strip()
        except Exception:
            file_token = None

    has_token = bool(env_token or file_token)
    create_issue_var = tk.BooleanVar(value=False)
    create_issue_chk = ttk.Checkbutton(frm, text='Create GitHub issue (requires WINPATABLE_GITHUB_TOKEN in environment)', variable=create_issue_var)
    create_issue_chk.grid(column=0, row=5, columnspan=4, sticky='w', pady=(8,0))
    if not has_token:
        create_issue_chk.state(['disabled'])

    open_page_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(frm, text='Open GitHub new-issue page in browser (prefill only)', variable=open_page_var).grid(column=0, row=6, columnspan=4, sticky='w')

    status_lbl = ttk.Label(frm, text='')
    status_lbl.grid(column=0, row=8, columnspan=6, sticky='w', pady=(8,0))

    def on_submit():
        title = title_entry.get().strip()
        body = desc.get('1.0', 'end').strip()
        if not title or not body:
            messagebox.showwarning('Missing fields', 'Please provide both title and description.')
            return

        path = save_report(rtype.get(), title, body)
        status_lbl.config(text=f'Report saved: {path}')

        # If token present and user wants to create via API
        if create_issue_var.get() and has_token:
                # prefer env token, otherwise file token
                if env_token:
                    os.environ['WINPATABLE_GITHUB_TOKEN'] = env_token
                elif file_token:
                    os.environ['WINPATABLE_GITHUB_TOKEN'] = file_token
                ok = try_create_github_issue(title, body)
            if ok:
                messagebox.showinfo('Issue Created', 'Created issue on GitHub and opened it in your browser.')
            else:
                messagebox.showwarning('API Failed', 'Could not create issue via API. Opening prefilled page instead.')
                open_github_issue_page(title, body)
        else:
            if open_page_var.get():
                open_github_issue_page(title, body)

        # keep window open for convenience

    submit_btn = ttk.Button(frm, text='Submit Report', command=on_submit)
    submit_btn.grid(column=0, row=7, sticky='w', pady=(8,0))

    # layout expand
    frm.rowconfigure(4, weight=1)
    frm.columnconfigure(5, weight=1)

    root.mainloop()


if __name__ == '__main__':
    launch_gui()
