from flask import Blueprint, render_template #,url_for
# from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    return render_template('main.html')