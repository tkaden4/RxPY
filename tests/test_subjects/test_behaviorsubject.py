from nose.tools import raises

from rx.testing import TestScheduler, ReactiveTest
from rx.subjects import BehaviorSubject
from rx.internal.exceptions import DisposedException

send = ReactiveTest.send
close = ReactiveTest.close
throw = ReactiveTest.throw
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created


class RxException(Exception):
    pass


# Helper function for raising exceptions within lambdas
def _raise(ex):
    raise RxException(ex)


def test_infinite():
    scheduler = TestScheduler()

    xs = scheduler.create_hot_observable(
        send(70, 1),
        send(110, 2),
        send(220, 3),
        send(270, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7),
        send(630, 8),
        send(710, 9),
        send(870, 10),
        send(940, 11),
        send(1020, 12)
    )

    subject = [None]
    subscription = [None]
    subscription1 = [None]
    subscription2 = [None]
    subscription3 = [None]

    results1 = scheduler.create_observer()
    results2 = scheduler.create_observer()
    results3 = scheduler.create_observer()

    def action1(scheduler, state=None):
        subject[0] = BehaviorSubject(100)
    scheduler.schedule_absolute(100, action1)

    def action2(scheduler, state=None):
        subscription[0] = xs.subscribe(subject[0])
    scheduler.schedule_absolute(200, action2)

    def action3(scheduler, state=None):
        subscription[0].dispose()
    scheduler.schedule_absolute(1000, action3)

    def action4(scheduler, state=None):
        subscription1[0] = subject[0].subscribe(results1)
    scheduler.schedule_absolute(300, action4)

    def action5(scheduler, state=None):
        subscription2[0] = subject[0].subscribe(results2)
    scheduler.schedule_absolute(400, action5)

    def action6(scheduler, state=None):
        subscription3[0] = subject[0].subscribe(results3)
    scheduler.schedule_absolute(900, action6)

    def action7(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(600, action7)

    def action8(scheduler, state=None):
        subscription2[0].dispose()
    scheduler.schedule_absolute(700, action8)

    def action9(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(800, action9)

    def action10(scheduler, state=None):
        subscription3[0].dispose()
    scheduler.schedule_absolute(950, action10)

    scheduler.start()

    assert results1.messages == [
        send(300, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7)]

    assert results2.messages == [
        send(400, 5),
        send(410, 6),
        send(520, 7),
        send(630, 8)]

    assert results3.messages == [
        send(900, 10),
        send(940, 11)]


def test_finite():
    scheduler = TestScheduler()

    xs = scheduler.create_hot_observable(
        send(70, 1),
        send(110, 2),
        send(220, 3),
        send(270, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7),
        close(630),
        send(640, 9),
        close(650),
        throw(660, RxException())
    )

    subject = [None]
    subscription = [None]
    subscription1 = [None]
    subscription2 = [None]
    subscription3 = [None]

    results1 = scheduler.create_observer()
    results2 = scheduler.create_observer()
    results3 = scheduler.create_observer()

    def action1(scheduler, state=None):
        subject[0] = BehaviorSubject(100)
    scheduler.schedule_absolute(100, action1)

    def action2(scheduler, state=None):
        subscription[0] = xs.subscribe(subject[0])
    scheduler.schedule_absolute(200, action2)

    def action3(scheduler, state=None):
        subscription[0].dispose()
    scheduler.schedule_absolute(1000, action3)

    def action4(scheduler, state=None):
        subscription1[0] = subject[0].subscribe(results1)
    scheduler.schedule_absolute(300, action4)

    def action5(scheduler, state=None):
        subscription2[0] = subject[0].subscribe(results2)
    scheduler.schedule_absolute(400, action5)

    def action6(scheduler, state=None):
        subscription3[0] = subject[0].subscribe(results3)
    scheduler.schedule_absolute(900, action6)

    def action7(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(600, action7)

    def action8(scheduler, state=None):
        subscription2[0].dispose()
    scheduler.schedule_absolute(700, action8)

    def action9(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(800, action9)

    def action10(scheduler, state=None):
        subscription3[0].dispose()
    scheduler.schedule_absolute(950, action10)

    scheduler.start()

    assert results1.messages == [
        send(300, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7)]

    assert results2.messages == [
        send(400, 5),
        send(410, 6),
        send(520, 7),
        close(630)]

    assert results3.messages == [
        close(900)]


def test_error():
    scheduler = TestScheduler()

    ex = RxException()

    xs = scheduler.create_hot_observable(
        send(70, 1),
        send(110, 2),
        send(220, 3),
        send(270, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7),
        throw(630, ex),
        send(640, 9),
        close(650),
        throw(660, RxException())
    )

    subject = [None]
    subscription = [None]
    subscription1 = [None]
    subscription2 = [None]
    subscription3 = [None]

    results1 = scheduler.create_observer()
    results2 = scheduler.create_observer()
    results3 = scheduler.create_observer()

    def action1(scheduler, state=None):
        subject[0] = BehaviorSubject(100)
    scheduler.schedule_absolute(100, action1)

    def action2(scheduler, state=None):
        subscription[0] = xs.subscribe(subject[0])
    scheduler.schedule_absolute(200, action2)

    def action3(scheduler, state=None):
        subscription[0].dispose()
    scheduler.schedule_absolute(1000, action3)

    def action4(scheduler, state=None):
        subscription1[0] = subject[0].subscribe(results1)
    scheduler.schedule_absolute(300, action4)

    def action5(scheduler, state=None):
        subscription2[0] = subject[0].subscribe(results2)
    scheduler.schedule_absolute(400, action5)

    def action6(scheduler, state=None):
        subscription3[0] = subject[0].subscribe(results3)
    scheduler.schedule_absolute(900, action6)

    def action7(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(600, action7)

    def action8(scheduler, state=None):
        subscription2[0].dispose()
    scheduler.schedule_absolute(700, action8)

    def action9(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(800, action9)

    def action10(scheduler, state=None):
        subscription3[0].dispose()
    scheduler.schedule_absolute(950, action10)

    scheduler.start()

    assert results1.messages == [
        send(300, 4),
        send(340, 5),
        send(410, 6),
        send(520, 7)]

    assert results2.messages == [
        send(400, 5),
        send(410, 6),
        send(520, 7),
        throw(630, ex)]

    assert results3.messages == [
        throw(900, ex)]

def test_canceled():
    scheduler = TestScheduler()

    xs = scheduler.create_hot_observable(
        close(630),
        send(640, 9),
        close(650),
        throw(660, RxException())
    )

    subject = [None]
    subscription = [None]
    subscription1 = [None]
    subscription2 = [None]
    subscription3 = [None]

    results1 = scheduler.create_observer()
    results2 = scheduler.create_observer()
    results3 = scheduler.create_observer()

    def action1(scheduler, state=None):
        subject[0] = BehaviorSubject(100)
    scheduler.schedule_absolute(100, action1)

    def action2(scheduler, state=None):
        subscription[0] = xs.subscribe(subject[0])
    scheduler.schedule_absolute(200, action2)

    def action3(scheduler, state=None):
        subscription[0].dispose()
    scheduler.schedule_absolute(1000, action3)

    def action4(scheduler, state=None):
        subscription1[0] = subject[0].subscribe(results1)
    scheduler.schedule_absolute(300, action4)

    def action5(scheduler, state=None):
        subscription2[0] = subject[0].subscribe(results2)
    scheduler.schedule_absolute(400, action5)

    def action6(scheduler, state=None):
        subscription3[0] = subject[0].subscribe(results3)
    scheduler.schedule_absolute(900, action6)

    def action7(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(600, action7)

    def action8(scheduler, state=None):
        subscription2[0].dispose()
    scheduler.schedule_absolute(700, action8)

    def action9(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(800, action9)

    def action10(scheduler, state=None):
        subscription3[0].dispose()
    scheduler.schedule_absolute(950, action10)

    scheduler.start()

    assert results1.messages == [
        send(300, 100)]

    assert results2.messages == [
        send(400, 100),
        close(630)]

    assert results3.messages == [
        close(900)]

def test_subject_disposed():
    scheduler = TestScheduler()

    subject = [None]

    results1 = scheduler.create_observer()
    subscription1 = [None]

    results2 = scheduler.create_observer()
    subscription2 = [None]

    results3 = scheduler.create_observer()
    subscription3 = [None]

    def action1(scheduler, state=None):
        subject[0] = BehaviorSubject(0)
    scheduler.schedule_absolute(100, action1)

    def action2(scheduler, state=None):
        subscription1[0] = subject[0].subscribe(results1)
    scheduler.schedule_absolute(200, action2)

    def action3(scheduler, state=None):
        subscription2[0] = subject[0].subscribe(results2)
    scheduler.schedule_absolute(300, action3)

    def action4(scheduler, state=None):
        subscription3[0] = subject[0].subscribe(results3)
    scheduler.schedule_absolute(400, action4)

    def action5(scheduler, state=None):
        subscription1[0].dispose()
    scheduler.schedule_absolute(500, action5)

    def action6(scheduler, state=None):
        subject[0].dispose()
    scheduler.schedule_absolute(600, action6)

    def action7(scheduler, state=None):
        subscription2[0].dispose()
    scheduler.schedule_absolute(700, action7)

    def action8(scheduler, state=None):
        subscription3[0].dispose()
    scheduler.schedule_absolute(800, action8)

    def action9(scheduler, state=None):
        subject[0].send(1)
    scheduler.schedule_absolute(150, action9)

    def action10(scheduler, state=None):
        subject[0].send(2)
    scheduler.schedule_absolute(250, action10)

    def action11(scheduler, state=None):
        subject[0].send(3)
    scheduler.schedule_absolute(350, action11)

    def action12(scheduler, state=None):
        subject[0].send(4)
    scheduler.schedule_absolute(450, action12)

    def action13(scheduler, state=None):
        subject[0].send(5)
    scheduler.schedule_absolute(550, action13)

    @raises(DisposedException)
    def action14(scheduler, state=None):
        subject[0].send(6)
    scheduler.schedule_absolute(650, action14)

    @raises(DisposedException)
    def action15(scheduler, state=None):
        subject[0].close()
    scheduler.schedule_absolute(750, action15)

    @raises(DisposedException)
    def action16(scheduler, state=None):
        subject[0].throw(RxException())
    scheduler.schedule_absolute(850, action16)

    @raises(DisposedException)
    def action17(scheduler, state=None):
        subject[0].subscribe(None)
    scheduler.schedule_absolute(950, action17)

    scheduler.start()

    assert results1.messages == [
        send(200, 1),
        send(250, 2),
        send(350, 3),
        send(450, 4)]

    assert results2.messages == [
        send(300, 2),
        send(350, 3),
        send(450, 4),
        send(550, 5)]

    assert results3.messages == [
        send(400, 3),
        send(450, 4),
        send(550, 5)]
