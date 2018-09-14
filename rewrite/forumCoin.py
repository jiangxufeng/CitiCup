# -*- coding:utf-8 -*-

from decimal import Decimal

Repeat_Factor = 30
Intention_Factor = 50


class ForumCoin(object):

    def __init__(self, user):
        self.user = user

    # 发布新帖子
    def get_interacting_consume_factor(self, tags, types):

        if not tags:
            return None

        types = ["post", "like", "comment"][types]
        u_t = self.user.tags

        tags = tags.split(";")
        if isinstance(u_t, dict):
            user_tags = u_t
        else:
            user_tags = eval(u_t)

        length = len(tags)

        interacting_consume_factor = []

        for i in range(length):
            if tags[i] in user_tags:
                user_tags[types][tags[i]] += 1
            else:
                user_tags[types][tags[i]] = 1

            interacting_consume_factor.append(Repeat_Factor ** (-user_tags[types][tags[i]]))

        self.user.tags = user_tags
        self.user.save()
        return interacting_consume_factor

    # 发布新帖子
    def new_issues(self, tags, degree):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 0)

        return sum([Decimal(i)*Decimal(degree)*self.user.wealth for i in interacting_consume_factor])

    # 点赞
    def likes(self, tags, click_num):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 1)

        intention_degree = Intention_Factor * click_num

        return sum([Decimal(i) * Decimal(intention_degree) * self.user.wealth for i in interacting_consume_factor])

    # 评论
    def comment(self, tags, degree):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 2)

        return sum([Decimal(i) * Decimal(degree) * self.user.wealth for i in interacting_consume_factor])