import time


def test_start_and_stop(migrations, server):
    assert server.is_alive() == True
    server.shutdown()
    time.sleep(0.5)
    assert server.is_alive() == False


def test_client_can_connect(migrations, server, client):
    assert server.get_clients_count() == 1


def test_cleanup(server, client):
    client.close()
    time.sleep(2)
    assert server.get_clients_count() == 0
