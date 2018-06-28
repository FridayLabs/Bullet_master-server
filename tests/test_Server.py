from src.Server import Server


def test_s():
    s = Server('0.0.0.0', 9999)
    s.initialize()
    s.listen()
