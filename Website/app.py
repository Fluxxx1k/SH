from flask import Flask, render_template
from jinja2 import Undefined
from flask import request
from HTML_logs import create_HTML_logs_cards_for_Website
app = Flask(__name__, static_folder='static')
class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return 'error'

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = \
        __int__ = __float__ = __complex__ = __pow__ = __rpow__ = \
        __sub__ = __rsub__ = _fail_with_undefined_error


app.jinja_env.undefined = SilentUndefined
@app.route('/')
@app.route('/index.html')
@app.route('/index')
@app.route('/main.html')
@app.route('/main')
def index():
    return render_template('index.html',
                           )


@app.route('/game')
@app.route('/game.html')
def game():
    return render_template('account.html',
                           safelog = create_HTML_logs_cards_for_Website(),


    )

if __name__ == '__main__':
    app.run(debug=True)