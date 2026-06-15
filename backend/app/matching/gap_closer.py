RESOURCES = {
    "python": ["https://docs.python.org/3/tutorial/", "https://www.freecodecamp.org/news/learn-python-free-python-courses-for-beginners/"],
    "react": ["https://react.dev/learn", "https://www.freecodecamp.org/learn/front-end-development-libraries/"],
    "postgres": ["https://www.postgresql.org/docs/current/tutorial.html"],
    "fastapi": ["https://fastapi.tiangolo.com/tutorial/"],
}


def recommend_resources(missing_keywords: list[str]) -> dict[str, list[str]]:
    return {keyword: RESOURCES.get(keyword.lower(), []) for keyword in missing_keywords}

