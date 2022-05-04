def test_development_config(application):
    application.config.from_object('app.config.DevelopmentConfig')