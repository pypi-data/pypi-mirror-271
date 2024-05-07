from typing import List, Dict


def ordering_to_query_params(ordering: Dict) -> List:
    if isinstance(ordering, dict):
        return [
            f"{k}_{v.lower()}"
            for k, v in ordering.items()
            if v.lower() in ("asc", "desc")
        ]


def tags_to_query_params(tags: Dict) -> List:
    if isinstance(tags, dict):
        return [f"{k}:{v}" for k, v in tags.items()]
