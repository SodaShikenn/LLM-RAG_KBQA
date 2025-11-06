from . import bp

@bp.route('/', endpoint='index')
def index():
    return 'demo.index'




