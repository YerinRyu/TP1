from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # blueprint
    from WEB.views import main_views, binary_views, multi_views, regression_views, training_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(binary_views.bp)
    app.register_blueprint(multi_views.bp)
    app.register_blueprint(regression_views.bp)
    app.register_blueprint(training_views.bp)

    return app