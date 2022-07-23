from config.settings import broker_host, broker_port

broker_url = f"redis://{broker_host}:{broker_port}/0"
