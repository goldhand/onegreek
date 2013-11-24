def split_addresses(email_string_list):
    """
    Converts a string containing comma separated email addresses
    into a list of email addresses.
    """
    return filter(None, [s.strip() for s in email_string_list.split(",")])