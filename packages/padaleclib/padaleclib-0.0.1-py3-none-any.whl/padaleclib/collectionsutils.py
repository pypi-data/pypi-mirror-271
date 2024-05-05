def list_elements_hierarchy(list_of_elements: list, compacted_form: bool = True) -> str:
    """
            Returns elements of a list in a hierarchical form

            :param compacted_form: This parameter is used to control whether the output string will be compacted or not,
            whether elements in the innermost list will be displayed in a single line or not (default: True)
            :param list_of_elements: The list of elements which you want returned in a hierarchical form
            :return: The list's elements displayed according to hierarchy as a string
        """
    hierarchy_string = " ["
    if compacted_form:
        is_innermost = True
        for i in range(len(list_of_elements)):
            if isinstance(list_of_elements[i], list):
                is_innermost = False
                if i == 0:
                    hierarchy_string += "\n"
                hierarchy_string += " ⁞ " + " [ "
                hierarchy_string = _list_elements_hierarchy_inner(list_of_elements[i], 2, hierarchy_string,
                                                             compacted_form)
                hierarchy_string += " ]"
                if i != len(list_of_elements) - 1:
                    hierarchy_string += ", "
                if i != len(list_of_elements) - 1:
                    hierarchy_string += "\n"
            else:
                try:
                    if isinstance(list_of_elements[i - 1], list):
                        hierarchy_string += " ⁞ " + " "
                except IndexError:
                    pass
                hierarchy_string += str(list_of_elements[i])
                if i != len(list_of_elements) - 1:
                    hierarchy_string += ", "
                    if isinstance(list_of_elements[i + 1], list):
                        hierarchy_string += "\n"
        if not is_innermost:
            hierarchy_string += "\n"
    else:
        hierarchy_string += "\n"
        for index, element in enumerate(list_of_elements):
            if isinstance(element, list):
                hierarchy_string += " ⁞ " + " [" + "\n"
                hierarchy_string = _list_elements_hierarchy_inner(element, 2, hierarchy_string, compacted_form)
                hierarchy_string += " ⁞ " + " ]"
            else:
                hierarchy_string += " " + str(element)
            if index != len(list_of_elements) - 1:
                hierarchy_string += ","
            hierarchy_string += "\n"
    hierarchy_string += " ]"
    return hierarchy_string


def _list_elements_hierarchy_inner(list_of_elements: list, dimension: int, hierarchy_string: str, compacted_form: bool) -> str:
    """
            Inner function of list_elements_hierarchy()

            This is the inner function of list_elements_hierarchy(). It takes the string from list_elements_hierarchy() and adds all the deeper dimensions to it. The function either
            adds the list of elements passed as a parameter to the return string (if it is one dimensional) or
            if it is still multidimensional it recursively calls on itself, passing the elements of type list into itself

            :param compacted_form: If true the returned string will have all the elements in the innermost list compacted to one line, otherwise, it will have one element per line
            :param list_of_elements: The list of elements which you want returned in a hierarchical form
            :param dimension: A variable to count how many dimensions deep the function is
            :param hierarchy_string: The returned string to which the function should add all the deeper dimensions of the main list
            :return: The list's elements displayed according to hierarchy as a string
        """
    if compacted_form:
        is_innermost = True
        for i in range(len(list_of_elements)):
            if isinstance(list_of_elements[i], list):
                is_innermost = False
                if i == 0:
                    hierarchy_string += "\n"
                hierarchy_string += " ⁞ " * dimension + " [ "
                hierarchy_string = _list_elements_hierarchy_inner(list_of_elements[i], dimension+1, hierarchy_string, compacted_form)
                hierarchy_string += " ]"
                if i != len(list_of_elements) - 1:
                    hierarchy_string += ", "
                if i != len(list_of_elements)-1:
                    hierarchy_string += "\n"
            else:
                try:
                    if isinstance(list_of_elements[i-1], list):
                        hierarchy_string += " ⁞ " * dimension + " "
                except IndexError:
                    pass
                hierarchy_string += str(list_of_elements[i])
                if i != len(list_of_elements) - 1:
                    hierarchy_string += ", "
                    if isinstance(list_of_elements[i+1], list):
                        hierarchy_string += "\n"
        if not is_innermost:
            hierarchy_string += "\n" + " ⁞ " * (dimension-1)
        return hierarchy_string
    else:
        for index, element in enumerate(list_of_elements):
            if isinstance(element, list):
                hierarchy_string += " ⁞ " * dimension + " [" + "\n"
                hierarchy_string = _list_elements_hierarchy_inner(element, dimension + 1, hierarchy_string, compacted_form)
                hierarchy_string += " ⁞ " * dimension + " ]"
            else:
                hierarchy_string += str(" ⁞ " * dimension) + " " + str(element)
            if index != len(list_of_elements) - 1:
                hierarchy_string += ","
            hierarchy_string += "\n"
        return hierarchy_string


def list_convert_types(list_to_convert: list, type_to_cast_to: type) -> list:
    """
    Casts all applicable elements in a list to a new type

    This function iterates over a list and trys to cast all elements in that list to the type passed in the parameter.
    If the cast is successful, the element's type is changed, if it is not, the element's type remains unchanged.

    :param list_to_convert: The list in which you want the element's types to be changed
    :param type_to_cast_to: The type you want the elements to be cast to
    :return: A list with all the applicable elements cast to the new type
    """
    for i in range(len(list_to_convert)):
        try:
            list_to_convert[i] = type_to_cast_to(list_to_convert[i])
        except ValueError:
            continue
    return list_to_convert
