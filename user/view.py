import logging
from sanic.response import text, html, json
from jinja2 import Template, PackageLoader, Environment
from sanic.blueprints import Blueprint

from models import User

bp = Blueprint('view_user')

logger = logging.getLogger(__name__)


@bp.route('/login/', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_list = await User.filter(nickname=username, password=password)
        if user_list:
            response = json(user_list)
            response.cookies[username] = username
            response.cookies[username]['domain'] = '.gotta-go-fast.com'
            response.cookies[username]['httponly'] = True
            return response
        else:
            return json({'msg': 'user not exist'})
    else:
        pass
