from unittest.mock import Mock, sentinel

import pytest

from dzira.betterdict import D
from dzira.data import worklogs_to_daily_report
# from dzira.data import make_issue_to_worklogs_mapping


# def test_make_issue_to_worklogs_mapping():
#     mock_issue = Mock(id="issue_id", key=sentinel.key, fields=Mock(summary=sentinel.summary))
#     mock_worklogs = [Mock(), Mock()]

#     result = make_issue_to_worklogs_mapping(mock_issue, mock_worklogs)

#     assert result == D(
#         {
#             "counter": 2,
#             "issue_id": D(key=sentinel.key, summary=sentinel.summary, worklogs=mock_worklogs)
#         }
#     )

@pytest.fixture
def worklogs():
    author = Mock(accountId="123")
    worklog1 = Mock(
        raw={
            "started": "2023-11-26T13:42:16.000+0100",
            "timeSpent": "30m",
            "comment": "task a",
            "timeSpentSeconds": 30 * 60,
        },
        author=author,
        id="1"
    )
    worklog2 = Mock(
        raw={
            "started":"2023-11-26T15:42:00.000+0100",
            "timeSpent": "1h 15m",
            "timeSpentSeconds": (60 * 60) + (15 * 60),
        },
        author=author,
        id="2"
    )
    return [worklog1, worklog2]


def test_worklogs_to_daily_report(worklogs):
    mock_issue_to_worklogs = D({"issue_id": D({"summary": "issue summary", "key": "ABC-123", "worklogs": [worklogs]})})

    result = worklogs_to_daily_report(mock_issue_to_worklogs)

    assert result == {
        "issue_id": {
            "key": "ABC-123", "summary": "issue summary", "total_time": "1h 45m", "total_seconds": 6300,
            "worklogs": [
                {"id": "1", "started": "12:42:16", "time_spent": "30m", "time_seconds": 1800, "comment": "task a"},
                {"id": "2", "started": "14:42:00", "time_spent": "1h 15m", "time_seconds": 4500, "comment": ""},
            ]
        }
    }
