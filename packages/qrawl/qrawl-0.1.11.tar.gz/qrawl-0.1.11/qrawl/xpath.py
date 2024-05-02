"""
This file is for all xpath-related functions that are relevant to all means of web crawling.
"""


def lowercase(text: str):
    """
    Returns the xpath needed to translate a string to lowercase
    """
    return f"translate('{text}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"


def contains_keywords(
    keywords: list[str],
    container: str = "text()",
    case_sensitive: bool = False,
):
    """
    Returns the xpath needed to search a container for keywords. Final xpath will look like:
    contains(text(), 'keyword1') and contains(text(), 'keyword2') and etc...
    Also, ensures keywords are searched for case-insensitively.
    """
    # This is to prevent user from having to add those quotes manually.
    # INCORRECT: contains(..., keyword), CORRECT: contains(..., 'keyword')
    ctn = container if container == "text()" else f"'{container}'"

    xpaths = []
    for kw in keywords:
        container_text = lowercase(ctn) if case_sensitive else ctn
        keyword_text = lowercase(kw) if case_sensitive else kw
        # Add quotes around keyword for same reason as above.
        keyword_text = f"'{keyword_text}'"
        xpath = f"contains({container_text}, {keyword_text})"
        xpaths.append(xpath)

    return " and ".join(xpaths)
