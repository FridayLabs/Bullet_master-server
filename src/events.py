from axel import Event

on_server_start = Event()
on_server_stop = Event()

on_client_connected = Event()
on_client_disconnected = Event()

on_message_received = Event()
