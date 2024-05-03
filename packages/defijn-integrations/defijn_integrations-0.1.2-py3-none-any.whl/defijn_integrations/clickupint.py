from pathlib import Path

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from json.decoder import JSONDecodeError
from rich.console import Console
import questionary

from rich.pretty import pprint

console = Console()

API_CLICKUP_KEY_FILE = Path.home() / ".clickup_api_key"


def load_clickup_api_key():
    if API_CLICKUP_KEY_FILE.exists():
        return API_CLICKUP_KEY_FILE.read_text().strip()
    else:
        return None


def save_clickup_api_key(api_key):
    API_CLICKUP_KEY_FILE.write_text(api_key)


"""
import requests

url = "https://api.clickup.com/api/v2/user"

headers = {"Authorization": "123"}

response = requests.get(url, headers=headers)

data = response.json()
print(data)
"""


def get_clickup_user_id(api_key):
    try:
        with console.status("[bold magenta]Getting user ID..", spinner="dots"):
            url = "https://api.clickup.com/api/v2/user"
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["user"]["id"]

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


"""
import requests

url = "https://api.clickup.com/api/v2/team"

headers = {"Authorization": "123"}

response = requests.get(url, headers=headers)

data = response.json()
print(data)
"""


def get_clickup_teams(api_key):
    try:
        with console.status("[bold magenta]Getting teams..", spinner="dots"):
            url = "https://api.clickup.com/api/v2/team"
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


"""
import requests

team_id = "123"
url = "https://api.clickup.com/api/v2/team/" + team_id + "/space"

query = {
  "archived": "false"
}

headers = {"Authorization": "123"}

response = requests.get(url, headers=headers, params=query)

data = response.json()
print(data)
"""


def get_clickup_spaces(team_id, api_key):
    try:
        with console.status("[bold magenta]Getting spaces..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/team/{team_id}/space"
            query = {
                "archived": "false"
            }
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


def get_clickup_folders(space_id, api_key):
    """
    import requests

    space_id = "123"
    url = "https://api.clickup.com/api/v2/space/" + space_id + "/folder"

    query = {
      "archived": "false"
    }

    headers = {"Authorization": "123"}

    response = requests.get(url, headers=headers, params=query)

    data = response.json()
    print(data)
    """
    try:
        with console.status("[bold magenta]Getting folders..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
            query = {
                "archived": "false"
            }
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


def get_clickup_lists(folder_id, api_key):
    """
    import requests

    folder_id = "123"
    url = "https://api.clickup.com/api/v2/folder/" + folder_id + "/list"

    query = {
      "archived": "false"
    }

    headers = {"Authorization": "123"}

    response = requests.get(url, headers=headers, params=query)

    data = response.json()
    print(data)
    """
    try:
        with console.status("[bold magenta]Getting lists..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
            query = {
                "archived": "false"
            }
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


def get_clickup_list(list_id, api_key):
    """
    import requests

    list_id = "123"
    url = "https://api.clickup.com/api/v2/list/" + list_id

    headers = {"Authorization": "123"}

    response = requests.get(url, headers=headers)

    data = response.json()
    print(data)
    """
    try:
        with console.status("[bold magenta]Getting list..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/list/{list_id}"
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


def get_clickup_tasks(list_id, api_key, statuses=['ongoing', 'open', 'backlog', 'doing']):
    """
    Retrieves tasks from ClickUp API.

    Args:
        list_id (str): The ID of the list from which to retrieve tasks.
        api_key (str): The API key used for authentication.
        statuses (List[str], optional): The task statuses to include (default is ['ongoing', 'open', 'backlog', 'doing']).

    Returns:
        Optional[Dict]: The JSON response containing the retrieved tasks, or None if an error occurred.
    """
    try:
        with console.status("[bold magenta]Getting tasks..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
            query = {
                "archived": "false",
                # "include_markdown_description": "true",
                # "page": "0",
                # "order_by": "string",
                # "reverse": "true",
                # "subtasks": "true",
                "statuses": statuses,
                # "include_closed": "true",
                # "assignees": "string",
                # "watchers": "string",
                # "tags": "string",
                # "due_date_gt": "0",
                # "due_date_lt": "0",
                # "date_created_gt": "0",
                # "date_created_lt": "0",
                # "date_updated_gt": "0",
                # "date_updated_lt": "0",
                # "date_done_gt": "0",
                # "date_done_lt": "0",
                # "custom_fields": "string",
                # "custom_items": "0"
            }
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


"""
    import requests

    list_id = "123"
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    query = {
      "custom_task_ids": "true",
      "team_id": "123"
    }

    payload = {
      "name": "New Task Name",
      "description": "New Task Description",
      "markdown_description": "New Task Description",
      "assignees": [
        183
      ],
      "tags": [
        "tag name 1"
      ],
      "status": "Open",
      "priority": 3,
      "due_date": 1508369194377,
      "due_date_time": False,
      "time_estimate": 8640000,
      "start_date": 1567780450202,
      "start_date_time": False,
      "notify_all": True,
      "parent": None,
      "links_to": None,
      "check_required_custom_fields": True,
      "custom_fields": [
        {
          "id": "0a52c486-5f05-403b-b4fd-c512ff05131c",
          "value": "This is a string of text added to a Custom Field."
        }
      ]
    }

    headers = {
      "Content-Type": "application/json",
      "Authorization": "123"
    }

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    print(data)
    """


def create_clickup_task(api_key, list_id, task_name, task_description, assignees, tags=None, status="doing", priority=3,
                        due_date=None,
                        time_estimate=0, start_date=None):
    """
    Create ClickUp Task

    Creates a new task in ClickUp.

    Args:
        list_id (str): The ID of the list to which the task belongs.
        api_key (str): The ClickUp API key for authorization.
        task_name (str): The name of the task.
        task_description (str): The description of the task.
        assignees (list): A list of assignee IDs for the task.
        tags (list, optional): A list of tag names for the task. Defaults to None.
        status (str, optional): The status of the task. Defaults to "doing".
        priority (int, optional): The priority of the task. Defaults to 3.
        due_date (str, optional): The due date of the task. Defaults to None.
        time_estimate (int, optional): The time estimate for the task in minutes. Defaults to 0.
        start_date (str, optional): The start date of the task. Defaults to None.

    Returns:
        dict: The response JSON object containing task details.

    Raises:
        HTTPError: If an HTTP error occurs.
        ConnectionError: If a connection error occurs.
        Timeout: If a timeout error occurs.
        JSONDecodeError: If a JSON decoding error occurs.
        RequestException: If an error occurs during the request.
        Exception: If an unexpected error occurs.

    """
    if tags is None:
        tags = []
    try:
        with console.status("[bold magenta]Creating task..", spinner="dots"):
            url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
            query = {
                "custom_task_ids": "true",
                "team_id": "123"
            }
            payload = {
                "name": task_name,
                "description": task_description,
                "markdown_description": task_description,
                "assignees": assignees,
                "tags": tags,
                "status": status,
                "priority": priority,
                "due_date": due_date,
                "due_date_time": False,
                "time_estimate": time_estimate,
                "start_date": start_date,
                "start_date_time": False,
                "notify_all": True,
                "parent": None,
                "links_to": None,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": api_key
            }
            response = requests.post(url, json=payload, headers=headers, params=query)
            response.raise_for_status()
            return response.json()

    except HTTPError as http_err:
        console.print(f"[bold red]HTTP error occurred: {http_err}[/]")
    except ConnectionError as conn_err:
        console.print(f"[bold red]Connection error occurred: {conn_err}[/]")
    except Timeout as timeout_err:
        console.print(f"[bold red]Timeout error occurred: {timeout_err}[/]")
    except JSONDecodeError as json_err:
        console.print(f"[bold red]JSON decode error: {json_err}[/]")
    except RequestException as req_err:
        console.print(f"[bold red]An error occurred during the request: {req_err}[/]")
    except Exception as err:
        console.print(f"[bold red]An unexpected error occurred: {err}[/]")

    return None


def main():
    clickup_api_key = load_clickup_api_key()
    if not clickup_api_key:
        clickup_api_key = console.input("[bold magenta]Enter your ClickUp API Key: [/]").strip()
        if not clickup_api_key:
            console.print("[bold red]No API Key provided. Exiting...[/]")
            exit()
        save_clickup_api_key(clickup_api_key)

    user_id = get_clickup_user_id(clickup_api_key)
    console.print(f"[bold magenta]User ID: [/]{user_id}")
    teams = get_clickup_teams(clickup_api_key)
    console.print(f"[bold magenta]Total Teams: [/]{len(teams['teams'])}")
    # get only team id and name
    teams = {
        "teams": [
            {
                "id": team["id"],
                "name": team["name"]
            } for team in teams["teams"]
        ]
    }
    console.print(f"[bold magenta]Teams:[/]")
    pprint(teams)
    team_id = teams["teams"][0]["id"]
    spaces = get_clickup_spaces(team_id, clickup_api_key)
    console.print(f"[bold magenta]Total Spaces: [/]{len(spaces['spaces'])}")
    # get only space id and name
    spaces = {
        "spaces": [
            {
                "id": space["id"],
                "name": space["name"]
            } for space in spaces["spaces"]
        ]
    }
    console.print(f"[bold magenta]Spaces:[/]")
    pprint(spaces)
    space_id = spaces["spaces"][0]["id"]
    folders = get_clickup_folders(space_id, clickup_api_key)
    console.print(f"[bold magenta]Total Folders: [/]{len(folders['folders'])}")
    # get only folder id and name
    folders = {
        "folders": [
            {
                "id": folder["id"],
                "name": folder["name"]
            } for folder in folders["folders"]
        ]
    }
    console.print(f"[bold magenta]Folders:[/]")
    pprint(folders)
    # load folders into questionary
    folder_choices = [folder["name"] for folder in folders["folders"]]
    print(folder_choices)
    folder_name = questionary.select("Select a folder:", choices=folder_choices).ask()
    folder_id = [folder["id"] for folder in folders["folders"] if folder["name"] == folder_name][0]
    lists = get_clickup_lists(folder_id, clickup_api_key)
    console.print(f"[bold magenta]Total Lists: [/]{len(lists['lists'])}")
    # get only list id and name
    lists = {
        "lists": [
            {
                "id": lst["id"],
                "name": lst["name"]
            } for lst in lists["lists"]
        ]
    }
    console.print(f"[bold magenta]Lists:[/]")
    pprint(lists)
    # load lists into questionary
    list_choices = [lst["name"] for lst in lists["lists"]]
    print(list_choices)
    list_name = questionary.select("Select a list:", choices=list_choices).ask()
    list_id = [lst["id"] for lst in lists["lists"] if lst["name"] == list_name][0]
    tasks = get_clickup_tasks(list_id, clickup_api_key)
    console.print(f"[bold magenta]Total Tasks: [/]{len(tasks['tasks'])}")
    # get only task id and name
    tasks = {
        "tasks": [
            {
                "id": task["id"],
                "status": task["status"]["status"],
                "name": task["name"]
            } for task in tasks["tasks"]
        ]
    }
    console.print(f"[bold magenta]Tasks:[/]")
    pprint(tasks)


if __name__ == "__main__":
    main()
