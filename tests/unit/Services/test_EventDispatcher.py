from src.Services.EventDispatcher import EventDispatcher


def test_dispatch():
    ed = EventDispatcher()
    called = False

    def handler(kwargs):
        nonlocal called
        called = True

    ed.add_listener('foo', handler)
    ed.dispatch('foo')
    assert called == True


def test_dispatch_with_args():
    ed = EventDispatcher()
    _kwargs = ()

    def handler(kwargs):
        nonlocal _kwargs
        _kwargs = kwargs

    ed.add_listener('foo', handler)
    ed.dispatch('foo', 123, True, 'asd', kek=123, lol='WUT')
    assert _kwargs == {'kek': 123, 'lol': 'WUT'}


def test_dispatch_to_class():
    ed = EventDispatcher()

    called = True
    _kwargs = {}

    class TstDispatch:
        def call_me(self, kwargs):
            nonlocal called, _kwargs
            called = True
            _kwargs = kwargs

    o = TstDispatch()
    ed.add_listener('foo', o.call_me)
    ed.dispatch('foo', 1, 2, 3, kek='lol')
    assert called == True
    assert _kwargs == {'kek': 'lol'}
