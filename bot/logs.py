"""
author: Bárbara Boechat
date: 29/04/2021

Main Bot Actions Log Generator
"""


class LogHandler:
    def __init__(self, log_info, date):
        self.log_info = log_info
        self.date = date

    def comment_log(self):
        ...

    def follow_log(self):
        # date, followers_count, is_follow
        print(f"Follow { self.log_info.follow } at { self.date }")

    def daily_follow_log(self):
        ...
