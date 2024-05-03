from pathlib import Path
from pprint import pprint

import gitlab
import questionary
from rich.console import Console
from rich.markdown import Markdown
from typing import List, Optional

# cat ~/.gitlab_api_key
# nvim ~/.gitlab_api_key
GITLAB_API_KEY_FILE = Path.home() / ".gitlab_api_key"

console = Console(width=180)

"""
https://python-gitlab.readthedocs.io/en/stable/api-usage.html
https://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html
https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
https://python-gitlab.readthedocs.io/en/stable/gl_objects/issues.html
"""


# Read the GitLab API key from the file
def load_gitlab_key():
    if GITLAB_API_KEY_FILE.exists():
        return GITLAB_API_KEY_FILE.read_text().strip()
    else:
        return None


gitlab_api_key = load_gitlab_key()
if not gitlab_api_key:
    console.print("[bold red]GitLab API key not found![/]")
    confirm_key_creation = questionary.confirm("Do you want to create a new GitLab API key?").ask()
    if confirm_key_creation:
        new_gitlab_api_key = questionary.text("Enter your GitLab API key:").ask()
        GITLAB_API_KEY_FILE.write_text(new_gitlab_api_key)
        gitlab_api_key = new_gitlab_api_key
    else:
        console.print("[bold red]Exiting...[/]")
        exit()

gl = gitlab.Gitlab(private_token=load_gitlab_key())


# ==================================================================
# FUNCTIONS
# ==================================================================
def get_current_user(verbose: Optional[bool] = False) -> gitlab.v4.objects.User:
    with console.status("[bold magenta]Gitlab - Getting current user...", spinner="monkey"):
        # console.print(f"[bold yellow]Gitlab - Getting current user...[/]")
        gl.auth()
        user = gl.user
        if verbose:
            # console.print(f"[bold magenta]{user}[/]")
            console.print(user)
            # pprint(dir(user))
        return user.username


def get_groups(verbose: Optional[bool] = False) -> List[gitlab.v4.objects.Group]:
    with console.status("[bold magenta]Gitlab - Getting groups...", spinner="monkey"):
        # console.print(f"[bold yellow]Gitlab - Getting groups...[/]")
        groups = gl.groups.list()
        if verbose:
            for group in groups:
                console.print(f"[bold magenta]{group.name}[/]")
                # pprint(dir(group))
        return groups


def get_group_projects(groups: List[gitlab.v4.objects.Group], verbose: Optional[bool] = False) -> List[int]:
    with console.status("[bold magenta]Gitlab - Getting group projects...", spinner="monkey"):
        project_ids = []
        for group in groups:
            projects = group.projects.list()
            if verbose:
                console.print(f"[bold green]{group.name}[/]")
            for project in projects:
                if verbose:
                    console.print(f"[bold magenta]{project.name}[/]")
                project_ids.append(project.id)  # Store project IDs
        return project_ids


def get_group_issues(groups: List[gitlab.v4.objects.Group], username: Optional[str] = None, verbose: Optional[bool] = False) -> List[gitlab.v4.objects.Issue]:
    with console.status("[bold magenta]Gitlab - Getting group issues...", spinner="monkey"):
        all_issues = []
        for group in groups:
            if username:
                issues = group.issues.list(state='opened', assignee_username=username, get_all=True)
            else:
                issues = group.issues.list(state='opened', get_all=True)
            if verbose and issues:
                console.print(f"[bold green]{group.name}[/]")
            for issue in issues:
                if verbose:
                    console.print(f"[bold blue]{issue.title}[/] - {issue.web_url}")
                all_issues.append(issue)
        console.print(f"[bold yellow]Total Gitlab issues: {len(all_issues)}[/]")
        # console.print(all_issues)
        return all_issues


def get_project_issues(project_ids: List[int], username: Optional[str] = None, verbose: Optional[bool] = False) -> \
        List[
            gitlab.v4.objects.Issue]:
    with console.status("[bold magenta]Gitlab - Getting project issues...", spinner="monkey"):
        all_issues = []
        for project_id in project_ids:
            project = gl.projects.get(project_id)  # Retrieve the full project object
            if username:
                issues = project.issues.list(state='opened', assignee_username=username, get_all=True)
            else:
                issues = project.issues.list(state='opened', get_all=True)
            if verbose and issues:
                console.print(f"[bold green]{project.name}[/]")
            for issue in issues:
                if verbose:
                    console.print(f"[bold blue]{issue.title}[/] - {issue.web_url}")
                all_issues.append(issue)  # Optional: Collect all issues in a list if needed elsewhere
        console.print(f"[bold yellow]Total issues: {len(all_issues)}[/]")
        return all_issues


def get_issues_assigned_to_username(username: str) -> List[gitlab.v4.objects.ProjectIssue]:
    """
    Fetch all issues from all projects that are assigned to a specific username.

    Args:
    gl (gitlab.Gitlab): Initialized GitLab instance.
    username (str): The username of the assignee.

    Returns:
    List[gitlab.v4.objects.ProjectIssue]: A list of issues assigned to the given username.
    """
    with console.status("[bold magenta]Gitlab - Getting issues assigned to username...", spinner="monkey"):
        issues = gl.issues.list(assignee_username=username,
                                all=True)  # 'all=True' retrieves all issues across all pages
        for issue in issues:
            console.print(f"[bold blue]{issue.title}[/] - {issue.web_url}")
        return issues


if __name__ == "__main__":
    # private token or personal token authentication (GitLab.com)
    gl = gitlab.Gitlab(private_token=load_gitlab_key())
    user = get_current_user(verbose=True)
    # get_issues_assigned_to_username(user)
    groups = get_groups(gl)
    project_ids = get_group_projects(groups)
    # group_issues = get_group_issues(groups, verbose=True)
    # group_issues = get_group_issues(groups, username=user, verbose=True)
    # issues = get_project_issues(project_ids, verbose=True)
    issues = get_project_issues(project_ids, username=user, verbose=True)
