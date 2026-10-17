from main import (
    validate_ticket,
    meets_follow_up_age,
    select_open_tickets,
    select_follow_up,
)


def test_meets_follow_up_age_below_boundary():
    assert meets_follow_up_age(1) is False


def test_meets_follow_up_age_at_boundary():
    assert meets_follow_up_age(2) is True


def test_meets_follow_up_age_above_boundary():
    assert meets_follow_up_age(3) is True


def test_boolean_age_is_invalid():
    ticket = {
        "id": "TEST1",
        "status": "open",
        "category": "software",
        "age_days": True,
        "priority": "high",
    }

    valid, _ = validate_ticket(ticket)

    assert valid is False


def test_missing_field_is_invalid():
    ticket = {
        "id": "TEST2",
        "status": "open",
        "category": "software",
        "priority": "high",
    }

    valid, _ = validate_ticket(ticket)

    assert valid is False


def test_open_ticket_selected():
    records = [
        {
            "id": "TEST3",
            "status": "open",
            "category": "software",
            "age_days": 1,
            "priority": "normal",
        }
    ]

    selected, _ = select_open_tickets(records)

    assert len(selected) == 1


def test_follow_up_ticket_selected():
    records = [
        {
            "id": "TEST4",
            "status": "open",
            "category": "software",
            "age_days": 2,
            "priority": "normal",
        }
    ]

    selected, _ = select_follow_up(records)

    assert len(selected) == 1


def test_follow_up_ticket_not_selected_when_too_young():
    records = [
        {
            "id": "TEST5",
            "status": "open",
            "category": "software",
            "age_days": 1,
            "priority": "normal",
        }
    ]

    selected, _ = select_follow_up(records)

    assert len(selected) == 0


def test_closed_ticket_not_selected_for_follow_up():
    records = [
        {
            "id": "TEST6",
            "status": "closed",
            "category": "software",
            "age_days": 10,
            "priority": "high",
        }
    ]

    selected, _ = select_follow_up(records)

    assert len(selected) == 0


def test_empty_input():
    selected, issues = select_follow_up([])

    assert selected == []
    assert issues == []
if __name__ == "__main__":
    test_meets_follow_up_age_below_boundary()
    test_meets_follow_up_age_at_boundary()
    test_meets_follow_up_age_above_boundary()
    test_boolean_age_is_invalid()
    test_missing_field_is_invalid()
    test_open_ticket_selected()
    test_follow_up_ticket_selected()
    test_follow_up_ticket_not_selected_when_too_young()
    test_closed_ticket_not_selected_for_follow_up()
    test_empty_input()

    print("All tests passed!")
