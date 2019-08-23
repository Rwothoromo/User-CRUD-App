def validate_inputs(args):
    """Return error message if input is invalid"""

    fifty_character_limit = ['first_name', 'last_name', 'username', 'name']
    for key, value in args.items():
        if isinstance(value, int):
            return False

        valid_length = 50 if key in fifty_character_limit else 256
        arg_is_invalid = (len(value) > valid_length or not isinstance(value, str) or not value.strip(),
                          valid_length, key)
        if arg_is_invalid[0]:
            return arg_is_invalid
