from flask import request, session

from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game
from WebsiteEasiest.logger import logger


def check_law(law: str, need_len: int = 3, allowed_x: bool = True) -> bool:
    allowed_literals = ['B', 'R']
    if allowed_x:
        allowed_literals.append('X')
    if len(law) != need_len:
        return False
    for char in law:
        if char not in allowed_literals:
            return False
    return True



def laws_vote(game_name: str):
    if 'username' not in session:
        return {'success': False, 'message': 'Необходимо войти в аккаунт'}, 401
    law = request.json.get('laws')
    if law is None:
        return {'success': False, 'message': 'Не указан закон'}, 400
    found_game, game_data = get_data_of_game(game_name)
    if not found_game:
        return {'success': False, 'message': f'Игра {repr(game_name)} не найдена: {game_data}'}, 404
    if session['username'] not in game_data['players']:
        return {'success': False, 'message': 'Вы не участвуете в этой игре'}, 403
    if game_data.get('president') is None:
        return {'success': False, 'message': 'Президент этой игры еще не был выбран'}, 400
    if game_data.get('president') != session['username']:
        if game_data.get('chancellor') is None:
            return {'success': False, 'message': 'Канцлер еще не был выбран'}, 400
        if game_data.get('chancellor') != session['username']:
            return {'success': False, 'message': 'Вы не президент и не канцлер этого раунда'}, 403
        else:
            if game_data.get('chancellor-lock') is True:
                return {'success': False, 'message': 'Канцлер уже назвал законы или президент ещё не успел сделать ход'}, 403
            if game_data.get('ccs') is None:
                if check_law(law, 2):
                    game_data['ccs'] = law
                    save_data_of_game(game_name, game_data)
                    return {'success': True, 'message': 'Канцлер назвал законы'}, 200
                else:
                    return {'success': False, 'message': 'Некорректный закон. Используйте только B, R, X длины 2'}, 400
            elif game_data.get('ccp') is None:
                if check_law(law, 1, allowed_x=game_data.get('veto', False)):
                    game_data['ccp'] = law
                    game_data['chancellor-lock'] = True
                    save_data_of_game(game_name, game_data)
                    return {'success': True, 'message': 'Канцлер принял закон'}, 200
                else:
                    return {'success': False, 'message': 'Некорректный закон. Используйте только B, R длины 1, если veto=False, иначе можно X'}, 400
            else:
                logger.warning(
                    f"Неизвестная ситуация с законом {law} в игре {game_name} с канцлером {session['username']}: {game_data}")
                game_data['ccs'] = None
                game_data['ccp'] = None
                game_data['chancellor-lock'] = False
                save_data_of_game(game_name, game_data)
                return {'success': False,
                        'message': "Неизвестная ситуация с канцлером, попробуйте начать сначала (назовите законы)"}, 500
    else:
        if game_data.get('president-lock') is True:
            return {'success': False, 'message': 'Президент уже назвал законы'}, 403
        if game_data.get('cps') is None:
            if check_law(law, 3):
                game_data['cps'] = law
                save_data_of_game(game_name, game_data)
                return {'success': True, 'message': 'Президент назвал законы'}, 200
            else:
                return {'success': False, 'message': 'Некорректный закон. Используйте только B, R, X длины 3'}, 400
        elif game_data.get('ccg') is None:
            if check_law(law, 2, allowed_x=False):
                game_data['ccg'] = law
                game_data['president-lock'] = True
                save_data_of_game(game_name, game_data)
                return {'success': True, 'message': 'Президент передал законы канцлеру'}, 200
            else:
                return {'success': False, 'message': 'Некорректный закон. Используйте только B, R длины 2'}, 400
        else:
            game_data['cps'] = None
            game_data['ccg'] = None
            game_data['president-lock'] = False
            save_data_of_game(game_name, game_data)
            return {'success': False, 'message': 'Неизвестная ситуация с президентом, попробуйте заново'}, 500


