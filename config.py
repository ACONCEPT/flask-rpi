def set_mqtt_config(app):
    app.config['MQTT_BROKER_URL'] = '192.168.1.14'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False
