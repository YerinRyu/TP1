from flask import Blueprint, render_template #,url_for
# from werkzeug.utils import redirect

bp = Blueprint('training', __name__, url_prefix='/')

@bp.route('/training')
def training_main():
    return render_template('main/training.html')

@bp.route('/training/result')
def training():
    return render_template('result/trainig_result.html')