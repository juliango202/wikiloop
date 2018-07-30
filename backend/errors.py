class FollowerError(Exception):
    def __init__(self, error, visited):
        self.error = error
        self.visited = visited

    def serialize(self):
        return {"error": self.error, "journey": list(self.visited.values())}


class LinkLoopError(FollowerError):
    def __init__(self, url, visited):
        super().__init__(
            f"Cannot continue because we are looping towards {url}.", visited
        )


class PageMissingError(FollowerError):
    def __init__(self, url, visited):
        super().__init__(f"Cannot continue because the page {url} is missing.", visited)


class PageWithoutLinkError(FollowerError):
    def __init__(self, url, visited):
        super().__init__(
            f"Cannot continue because the page {url} has no link.", visited
        )
