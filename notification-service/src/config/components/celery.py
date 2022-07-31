from config.settings import broker_host, broker_port

broker_url = f"amqp://{broker_host}:{broker_port}/vhost"
