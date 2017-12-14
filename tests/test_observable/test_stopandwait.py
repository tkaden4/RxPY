import unittest

from rx.testing import TestScheduler, ReactiveTest

send = ReactiveTest.send
close = ReactiveTest.close
throw = ReactiveTest.throw
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created


class TestStopAndWait(unittest.TestCase):

    def test_never(self):
        scheduler = TestScheduler()

        xs = scheduler.create_hot_observable(
            send(150, 1)
        )

        def create():
            return xs.controlled(True, scheduler).stop_and_wait()

        results = scheduler.start(create)
        assert results.messages == []
        assert xs.subscriptions == [subscribe(200, 1000)]

    def test_empty(self):
        scheduler = TestScheduler()

        xs = scheduler.create_hot_observable(
            send(150, 1),
            close(250)
        )

        def create():
            return xs.controlled(True, scheduler).stop_and_wait()

        results = scheduler.start(create)

        assert results.messages == [close(250)]
        assert xs.subscriptions == [subscribe(200, 250)]
