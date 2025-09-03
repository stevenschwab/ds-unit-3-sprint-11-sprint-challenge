from .aq_dashboard import create_app

# telling flask to use our create_app function (factory)
# app will be named "APP"
APP = create_app()
