def contains_from(string, words):
    for word in words:
        if word.lower() in string.lower():
            return True
    return False


def contains_words(element, words):
    content = element.get_text()
    for attr in list(element.attrs.values()):
        if isinstance(attr, list):
            content += (' ' + ' '.join(attr))
        else:
            content += (' ' + attr)

    return contains_from(content, words)


def contains_all_words(element, words):
    content = element.get_text()
    for attr in list(element.attrs.values()):
        if isinstance(attr, list):
            content += (' ' + ' '.join(attr))
        else:
            content += (' ' + attr)

    for word in words:
        if word not in content:
            return False

    return True


def search_by_words(elements, words):
    found_elements = []
    for element in elements:
        if contains_from(element.text, words):
            found_elements.append(element)
        else:
            attrs = element.attrs
            for value in attrs.values():
                if isinstance(value, str):
                    if contains_from(value, words):
                        found_elements.append(element)
                if isinstance(value, list):
                    for s in value:
                        if contains_from(s, words):
                            found_elements.append(element)
    return found_elements


def search_by_tags(elements, words):
    found_elements = []
    for element in elements:
        if contains_from(element.name, words):
            found_elements.append(element)
    return found_elements


def find_search(inputs, words):
    search = None
    for input in inputs:
        if contains_words(input, words) and not contains_words(input, ["город"]):
            search = input
            break
    return search


def find_no_filter(element):
    parent = element.parent
    while parent.name != "body":
        if contains_words(parent, ["filter"]):
            return False
        parent = parent.parent
    return True


def find_parent_next(element):
    parent = element.parent
    if parent.name == "li" and contains_words(parent, ["next", "след"]) and not contains_words(parent, ["disabled"]):
        return True
    return False

