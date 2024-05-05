def get_input_of_type(input_prompt_message: str, input_type: type, invalid_input_message: str = "Invalid Input"):
    """
    Get input of specific type

    This function loops until the user enters an input which can be cast into the type passed as parameter

    :param input_prompt_message: Message to display when first asking user for input
    :param input_type: Type of the input you want (input will be cast to this type)
    :param invalid_input_message: Message to be displayed when user enters invalid input (Default = "Invalid Input")
    :return: Returns the user input cast into the type passed as parameter input_type
    """
    correct_input = False
    cast_input = None
    while not correct_input:
        user_input = input(input_prompt_message)
        try:
            cast_input = input_type(user_input)
            correct_input = True
        except ValueError:
            print(invalid_input_message)
    return cast_input
