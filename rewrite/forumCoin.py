# -*- coding:utf-8 -*-

from account.models import LoginUser
from decimal import Decimal

Repeat_Factor = 80


def new_issues(user, tags, degree):
    """
    :param user:  用户对象
    :param tags:   前段传入的tag
    :param degree:  程度
    :return: 小号的论坛币
    """
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

    Interacting_Consume_Factor = []

    for i in range(length):
        if tags[i] in user_tags:
            user_tags[tags[i]] += 1
        else:
            user_tags[tags[i]] = 1

        Interacting_Consume_Factor.append(Repeat_Factor ** (-user_tags[tags[i]]))

    user.posttags = user_tags
    user.save()

    #print(Interacting_Consume_Factor)
    return sum([Decimal(i)*Decimal(degree)*user.wealth for i in Interacting_Consume_Factor])


if __name__ == "__main__":
    user = LoginUser.objects.get(username='qwer1234')
    user.wealth = 1000
    user.tags = {'1': 3}
    user.save()