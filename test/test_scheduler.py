from unittest import TestCase

from app.scheduler import Scheduler


def simple_function():
    print(5)


def fun_with_args(x):
    print(x)


class TestScheduler(TestCase):
    @classmethod
    def setUpClass(cls):
        scheduler = Scheduler()
        scheduler.start()
        cls.scheduler = scheduler.apscheduler

    def test_simple_function(self):
        self.scheduler.add_job(simple_function)

    def test_fun_with_args(self):
        self.scheduler.add_job(lambda: fun_with_args(15))