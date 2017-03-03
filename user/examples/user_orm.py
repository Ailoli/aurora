from sanic.response import json
from sanic import Blueprint
from sanic import Sanic
from user.models import User
from user.config import settings

from user.db import setup_connection, close_connection

import logging
logger = logging.getLogger()

app = Sanic(__name__)
bp = Blueprint('user', url_prefix='/v1/user')

'''
/v1/user 旨在 以orm实现业务需求
'''


@bp.route('/')
async def index(request):
    '''
    获取所有用户列表
    :param request:
    :return:
    '''
    try:
        obj_list = await User.all()
        return json(obj_list)
    except Exception as e:
        logger.error('index error', str(e))
        return json({'msg': 'fail'})


@bp.route('/<username>/')
async def get_user(request, username):
    '''
    以用户名获取指定用户对象
    :param request:
    :return:
    '''
    try:
        user_list = await User.filter(nickname=username,)
        # user_list = await User.findAll('nickname=$1', username)

        return json(user_list)
    except Exception as e:
        logger.error('get_user error', str(e))
        return json({'msg': 'fail'})


@bp.post('/save/')
async def save_user(request):
    '''
    保存user对象
    :param request:
    :return:
    '''
    try:
        if request.form:
            username = request.parsed_form.get('username', '')
            nickname = request.parsed_form.get('nickname', '')
            password = request.parsed_form.get('password', '')
            email = request.parsed_form.get('email', '')

            user = User(username=username, nickname=nickname, password=password, email=email)
            res = await user.save()

            if res:
                return json({'msg': 'ok'})
        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('user save error', str(e))
        return json({'msg': 'fail'})


@bp.post('/update/<id>/')
async def update_user(request, id):
    '''
    更新user对象

        id = request.parsed_form.get('id', '')
        username = request.parsed_form.get('username', '')
        nickname = request.parsed_form.get('nickname', '')
        password = request.parsed_form.get('password', '')
        email = request.parsed_form.get('email', '')

        user = User(id=id, username=username, nickname=nickname, password=password, email=email)

    :param request:
    :param id:
    :return:
    '''
    try:
        if request.form:
            # res = {'id': ['4'], 'email': ['em'], 'username': ['user'], 'nickname': ['ck'], 'password': ['pd']}
            res = {}
            for key in request.parsed_form.keys():
                res.update({key: request.parsed_form.get(key)})

            user = User(**res)
            await user.update()
            return json({'msg': 'ok'})
        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('user save error', str(e))
        return json({'msg': 'fail'})


@bp.post('/del/<id>/')
async def del_user(request, id):
    '''
    删除user对象
    :param request:
    :param id:
    :return:
    '''
    try:
        if request.form:
            user = User(id=id)
            await user.delete()
            return json({'msg': 'ok'})
        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('user save error', str(e))
        return json({'msg': 'fail'})


if __name__ == "__main__":
    '''
    sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
    '''
    app.blueprint(bp)
    app.run(host="0.0.0.0", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG,
            after_start=setup_connection, after_stop=close_connection)
