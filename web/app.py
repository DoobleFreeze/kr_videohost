from flask import Flask, jsonify, make_response, request, send_from_directory
from generate_code import generate_code
from flasgger import Swagger
from configs.app_cfg import *
from data import db_session
from data.users import Users
from data.videos import Videos

import logging.config
import traceback
import logging
import redis
import yaml
import os

app = Flask(__name__)
app.config['SWAGGER'] = {
    'openapi': '3.0.3',
    'title': 'API Documentation',
}
app.config['SECRET_KEY'] = "7F0zF26aIBnxfDdUvh59YJ26"

swagger = Swagger(app, template=template)

db_session.global_init("/opt/app/db/manager.sqlite")

client = redis.StrictRedis(
    host="REDIS",
    port=6379,
    password='MDZ17Qyb',
    charset='utf-8',
    decode_responses=True
)

json_response_200 = {'result': 'Success'}
json_response_400 = {'error': "Invalid request"}
json_response_404 = {'error': 'Page not found'}

LOGGING_CFG_PATH = "configs/logging.cfg.yml"


def get_logger(logging_cfg_path: str = None) -> logging.Logger:
    """
    Инициализация логирования.

    Отключает логирование от requests и Flask, поскольку из-за постоянных
    HTTP запросов захламляет логи. Создает оператор логирования с учетом
    конфигурации, прописанной в файле. Путь к файлу передается как строковый
    параметр.

    Arguments:
        logging_cfg_path (str): Путь до файла с конфигурацией.

    Returns:
        logging.Logger: Оператор логирования.
    """
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    logger_api = logging.getLogger('api_logger')

    with open(logging_cfg_path) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin.read()))

    return logger_api


# Подключение логов
logger = get_logger(logging_cfg_path=LOGGING_CFG_PATH)


@app.errorhandler(404)
def not_found(_error):
    """
    Обработчик ошибки 404

    Обработчик запросов не инициализированных ссылок. Вернёт ответ 404 и
    JSON с ошибкой, что страница не найдена.

    Arguments:
        _error (werkzeug.exceptions.NotFound): Представление ошибки, созданное
            библиотекой werkzeug. Обязательный параметр при использовании
            декоратора errorhandler().

    Returns:
        flask.wrappers.Response: Данные в формате JSON и код ответа с
            расшифровкой.
    """
    try:
        return make_response(jsonify(json_response_404), 404)
    except Exception as e:
        logger.error(f'Возникла ошибка с обработчиком страницы 404: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


def main() -> None:
    """
    Запуск API сервера

    Returns:
        None: Нет возвращаемых данных.
    """
    try:
        app.run(port=6556, host='localhost')
    except Exception as e:
        logger.error(f'Возникла ошибка с запуском сервера: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обработчик страницы `/register`

    Обработчик POST и GET запросов страницы `/register`.

    При GET запросе возвращается строка с текстовым представлением функционала
    метода. Строка является заглушкой, которую в последующем можно заменить на
    полноценную клиентскую сторону в формате html.

    При POST запросе принимает на вход данные в формате JSON, отправленные в
    запросе с двумя параметрами:`name` - имя пользователя и `password` - пароль
    пользователя. Если параметры присутствуют в запросе и имя пользователя не
    занято, то добавляется новая запись в БД с этими данными, иначе возвращается
    ошибка в формате JSON и код 400.

    Returns:
        flask.wrappers.Response: Данные в формате JSON (Или текстовая строка) и
            код ответа с расшифровкой.
    """
    try:
        if request.method == "GET":
            return make_response("Отправьте POST запрос с JSON данными: name, password")
        else:
            r_json = request.json
            if "name" in r_json and "password" in r_json:
                if r_json['name'] and r_json['password']:
                    session = db_session.create_session()
                    user = session.query(Users).filter(Users.user_name == r_json['name']).first()
                    if user:
                        json_response = {"error": f'User {r_json["user"]} already exists'}
                        return make_response(jsonify(json_response), 400)
                    new_user = Users(user_name=r_json['name'],
                                     user_password=r_json['password'])
                    session.add(new_user)
                    session.commit()
                    return make_response(jsonify(json_response_200), 200)
            return make_response(jsonify(json_response_400), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /register: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
        if request.method == "GET":
            return make_response("Отправьте POST запрос с JSON данными: name, password")
        else:
            r_json = request.json
            if "name" in r_json and "password" in r_json:
                if r_json['name'] and r_json['password']:
                    session = db_session.create_session()
                    user = session.query(Users).filter(Users.user_name == r_json['name'],
                                                       Users.user_password == r_json['password']).first()
                    if not user:
                        json_response = {"error": f'Name or password is incorrect'}
                        return make_response(jsonify(json_response), 400)
                    new_key = generate_code()
                    client.set(new_key, user.user_name, 60 * 60 * 24)
                    json_response = {"key": new_key, "time_life (sec)": 60 * 60 * 24}
                    return make_response(jsonify(json_response), 200)
            return make_response(jsonify(json_response_400), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /auth: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/add_video/<string:key>', methods=['GET', 'POST'])
def add_video(key):
    try:
        if request.method == "GET":
            return make_response("Отправьте POST запрос с файлом формата .mp4")
        else:
            user_redis = client.get(key)
            if user_redis:
                session = db_session.create_session()
                user = session.query(Users).filter(Users.user_name == user_redis).first()
                if user:
                    if "video" in request.files:
                        if request.files["video"].filename[-4:] == ".mp4":
                            video = request.files['video'].read()
                            new_name = generate_code(len_key=64)
                            with open(f'video_storage/{new_name}.mp4', "wb") as f:
                                f.write(video)
                            new_video = Videos(user_id=user.id, video_name=request.files["video"].filename[:-4],
                                               video_path=new_name, count_view=0)
                            session.add(new_video)
                            session.commit()
                            return make_response(jsonify(json_response_200), 200)
                        else:
                            json_response = {'error': "file is not mp4"}
                            return make_response(jsonify(json_response), 400)
                    else:
                        json_response = {'error': "file is not found"}
                        return make_response(jsonify(json_response), 400)
                else:
                    json_response = {'error': "User is not found"}
                    return make_response(jsonify(json_response), 400)
            else:
                json_response = {'error': "API key out of date"}
                return make_response(jsonify(json_response), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /add_video: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/get_video/<string:file_path>', methods=['GET'])
def get_video(file_path):
    try:
        session = db_session.create_session()
        video = session.query(Videos).filter(Videos.video_path == file_path).first()
        if video:
            video.count_view += 1
            session.commit()
            return send_from_directory(f"video_storage", file_path + '.mp4')
        else:
            return make_response(jsonify(json_response_400), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /get_video: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/get_all_videos', methods=['GET'])
def get_all_videos():
    try:
        session = db_session.create_session()
        videos = session.query(Videos)
        dict_response = {}
        for video in videos:
            user = session.query(Users).filter(Users.id == video.user_id).first()
            dict_response[video.id] = [user.user_name, video.video_name,
                                       f'http://localhost:1337/get_video/{video.video_path}', video.count_view]
        return make_response(jsonify(dict_response), 200)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /get_all_video: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/get_user_videos/<string:user_name>', methods=['GET'])
def get_user_videos(user_name):
    try:
        session = db_session.create_session()
        user = session.query(Users).filter(Users.user_name == user_name).first()
        if user:
            videos = session.query(Videos).filter(Videos.user_id == user.id)
            dict_response = {}
            for video in videos:
                dict_response[video.id] = [user.user_name, video.video_name,
                                           f'http://localhost:1337/get_video/{video.video_path}', video.count_view]
            return make_response(jsonify(dict_response), 200)
        else:
            json_response = {'error': "User is not found"}
            return make_response(jsonify(json_response), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /get_users_videos: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/search_video/<string:search_phrase>', methods=['GET'])
def search_video(search_phrase):
    try:
        session = db_session.create_session()
        videos = session.query(Videos)
        dict_response = {}
        for video in videos:
            if search_phrase in video.video_name:
                user = session.query(Users).filter(Users.id == video.user_id).first()
                dict_response[video.id] = [user.user_name, video.video_name,
                                           f'http://localhost:1337/get_video/{video.video_path}', video.count_view]
        return make_response(jsonify(dict_response), 200)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /get_users_videos: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        session = db_session.create_session()
        users = session.query(Users)
        dict_response = {}
        for user in users:
            dict_response[user.id] = [user.user_name,
                                      f'http://localhost:1337/get_user_videos/{user.user_name}']
        return make_response(jsonify(dict_response), 200)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /get_users: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


@app.route('/delete_video/<string:file_path>/<string:key>', methods=['DELETE'])
def delete_video(file_path, key):
    try:
        user_redis = client.get(key)
        if user_redis:
            session = db_session.create_session()
            user = session.query(Users).filter(Users.user_name == user_redis).first()
            if user:
                video = session.query(Videos).filter(Videos.video_path == file_path,
                                                     Videos.user_id == user.id).first()
                if video:
                    os.remove(f'video_storage/{video.video_path + ".mp4"}')
                    session.delete(video)
                    session.commit()

                    return make_response(jsonify(json_response_200), 200)
                else:
                    json_response = {'error': "file is not found"}
                    return make_response(jsonify(json_response), 400)
            else:
                json_response = {'error': "User is not found"}
                return make_response(jsonify(json_response), 400)
        else:
            json_response = {'error': "API key out of date"}
            return make_response(jsonify(json_response), 400)
    except Exception as e:
        logger.error(f'Возникла ошибка со страницей /delete_video: {str(e)}')
        logger.debug(f'Ошибка:\n{traceback.format_exc()}')


if __name__ == "__main__":
    main()
