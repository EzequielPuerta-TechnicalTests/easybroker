from __future__ import annotations


class WrappedResource:
    def __init__(self, *path: str, subs: list["WrappedResource"] = []) -> None:
        self.accessor: str = path[-1]
        self.wrapped = lambda parent: parent._resource(*path, subs=subs)

    def __get__(self, parent, parent_type=None):
        return self.wrapped(parent)
