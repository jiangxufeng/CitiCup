# -*- coding:utf-8 -*-

from account.models import LoginUser

Repeat_Factor = 100
Intention_Factor = 4


class ForumCoin(object):

    def __init__(self, user):
        self.user = user

    # 发布新帖子
    def get_interacting_consume_factor(self, tags, types):

        if not tags:
            return None

        types = ["post", "like", "comment"][types]
        u_t = self.user.alltags

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

        self.user.alltags = user_tags
        self.user.save()
        return interacting_consume_factor

    # 发布新帖子
    def new_issues(self, tags, degree):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 0)

        return sum([i*degree*self.user.forumcoin for i in interacting_consume_factor])

    # 点赞
    def likes(self, tags, click_num):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 1)

        intention_degree = Intention_Factor * click_num

        return sum([i * intention_degree * self.user.forumcoin for i in interacting_consume_factor])

    # 评论
    def comment(self, tags, degree):

        interacting_consume_factor = self.get_interacting_consume_factor(tags, 2)

        return sum([i * degree * self.user.forumcoin for i in interacting_consume_factor])