from src.Server import Server


def test_listen():
    s = Server('0.0.0.0', 9999)
    s.initialize()
    s.listen()
    s.shutdown()
