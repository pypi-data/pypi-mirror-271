from jira.resources import Issue

from dzira.betterdict import D


# def make_issue_to_worklogs_mapping(issue: Issue, worklogs: list) -> D:
#     issue_to_worklogs = D(counter=0)

#     return issue_to_worklogs


def worklogs_to_daily_report(worklogs: D):
    """
    >>> worklogs_to_daily_report(worklogs)
    >>> {"issue_id":
          {"key": key, "summary": summary, "total_time": N,
           "worklogs": [
             {"w_id": N, "started": dt, "spent_time": TT, "spent_seconds": SS, "comment": comment}
           ]
          }
        }
    """
    ...


# todo
def sprint_report():
    ...

def show_issues_as_table():
    sprint = sprint_and_issues["sprint"]
    json_dict = {
        "sprint": {
            "name": sprint.name,
            "id": sprint.id,
            "start": sprint.startDate,
            "end": sprint.endDate,
        },
        "issues": [dict(zip(headers, issue)) for issue in processed_issues]
    }
    print(json.dumps(json_dict))


def show_issues_as_json():
    ...


def show_issues_as_csv(sprint: Sprint, issues: list):
    ...
