from ticket_data import TICKETS

VALID_STATUSES = {"open", "closed"}
VALID_CATEGORIES = {"software", "network", "access"}
VALID_PRIORITIES = {"low", "normal", "high"}


def validate_ticket(ticket):
    """Validate a ticket record and return (is_valid, message)."""

    required_fields = ["id", "status", "category", "age_days", "priority"]

    for field in required_fields:
        if field not in ticket:
            ticket_id = ticket.get("id", "Unknown")
            return False, f"{ticket_id}: missing required field '{field}'"

    if not isinstance(ticket["id"], str) or not ticket["id"].strip():
        return False, "Invalid ticket id"

    if ticket["status"] not in VALID_STATUSES:
        return False, f"{ticket['id']}: invalid status"

    if ticket["category"] not in VALID_CATEGORIES:
        return False, f"{ticket['id']}: invalid category"

    if ticket["priority"] not in VALID_PRIORITIES:
        return False, f"{ticket['id']}: invalid priority"

    age = ticket["age_days"]

    if not isinstance(age, int) or isinstance(age, bool) or age < 0:
        return False, f"{ticket['id']}: invalid age_days"

    return True, ""


def select_open_tickets(records):
    """
    Return valid open tickets and any validation issues.
    Returns (selected, issues).
    """

    selected = []
    issues = []

    for ticket in records:
        valid, message = validate_ticket(ticket)

        if not valid:
            issues.append(message)
            continue

        if ticket["status"] == "open":
            selected.append(ticket)

    return selected, issues


def meets_follow_up_age(age_days):
    """
    Tuesday repaired version.
    Follow-up requires age_days >= 2.
    """

    return age_days >= 2


def select_follow_up(records):
    """
    Tuesday Follow-Up v1:
    - valid
    - open
    - age_days >= 2

    Returns (selected, issues).
    """

    selected = []
    issues = []

    for ticket in records:
        valid, message = validate_ticket(ticket)

        if not valid:
            issues.append(message)
            continue

        if (
            ticket["status"] == "open"
            and meets_follow_up_age(ticket["age_days"])
        ):
            selected.append(ticket)

    return selected, issues


def display_results(title, tickets, issues):
    """Display selected tickets and issues."""

    print(f"\n{title}")
    print("-" * len(title))

    if tickets:
        for ticket in tickets:
            print(
                f"ID: {ticket['id']} | "
                f"Status: {ticket['status']} | "
                f"Category: {ticket['category']} | "
                f"Age: {ticket['age_days']} | "
                f"Priority: {ticket['priority']}"
            )

        print(f"\nCount: {len(tickets)}")

    else:
        print("No tickets match the current rule.")

    if issues:
        print("\nRecords Needing Checking:")

        for issue in issues:
            print(f"- {issue}")


def main():
    print("Ticket Rules Application")
    print("Current Follow-Up Policy:")
    print("Valid, open, and at least 2 days old.\n")

    open_tickets, open_issues = select_open_tickets(TICKETS)

    follow_up_tickets, follow_up_issues = select_follow_up(TICKETS)

    display_results(
        "OPEN TICKETS",
        open_tickets,
        open_issues
    )

    display_results(
        "FOLLOW-UP TICKETS (V1)",
        follow_up_tickets,
        follow_up_issues
    )


if __name__ == "__main__":
    main()