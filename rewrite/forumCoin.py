# -*- coding:utf-8 -*-

from account.models import LoginUser
from decimal import Decimal

Repeat_Factor = 80


def new_issues(user, tags, degree):

    if not tags:
        return None

    if not degree:
        return None

    tags = tags.split(";")
    if isinstance(user.posttags, dict):
        user_tags = user.posttags
    else:
        user_tags = eval(user.posttags)

    length = len(tags)

    interacting_consume_factor = []

    for i in range(length):
        if tags[i] in user_tags:
            user_tags[tags[i]] += 1
        else:
            user_tags[tags[i]] = 1

        interacting_consume_factor.append(Repeat_Factor ** (-user_tags[tags[i]]))

    user.posttags = user_tags
    user.save()

    print(interacting_consume_factor)
    return sum([Decimal(i)*Decimal(degree)*user.wealth for i in interacting_consume_factor])


if __name__ == "__main__":
    user = LoginUser.objects.get(username='qwer1234')
    user.wealth = 1000
    user.tags = {'1': 3}
    user.save()