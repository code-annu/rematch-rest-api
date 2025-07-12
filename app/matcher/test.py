from typing import Optional

from fastapi import Query


def get_users(
    min_age: Optional[int] = Query(None, alias="age_gt"),
    max_age: Optional[int] = Query(None, alias="age_lt"),
    gender: Optional[str] = None
):
    query = {}
    if min_age is not None:
        query.setdefault("age", {})["$gt"] = min_age
    if max_age is not None:
        query.setdefault("age", {})["$lt"] = max_age
    if gender:
        query["gender"] = gender

    print(query)


get_users(gender='Male',min_age=10,max_age=20)
