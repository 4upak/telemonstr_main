import json
def get_account_info(account):
    try:
        f = open(f"accounts/sessions/import/{account}.json", "r")
        with f as read_file:
            return json.load(read_file)
    except Exception as ex:
        return False