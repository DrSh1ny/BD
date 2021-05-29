from flask import Flask, jsonify, request, session
import logging
import psycopg2
import time
import configparser

app = Flask(__name__)


#######################################
########## Create New User ############
#######################################


@app.route("/dbproj/user/", methods=['POST'])
def add_user():
    logger.info("[POST] /user/")
    payload = request.get_json(force=True)
    logger.debug("\tpayload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["username"], payload["email"], payload["password"])

        cur.execute("select registeruser('{0}', '{1}', '{2}');".format(
            values[0], values[1], values[2]))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()
        id = response[0][0]
        if(id in [-4, -3, -2, -1]):
            content = {'erro': 400}
        else:
            content = {'userId': id}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
########## Login User #################
#######################################


@app.route("/dbproj/user/", methods=['PUT'])
def login_user():
    logger.info("[PUT] /user/")
    payload = request.get_json(force=True)
    logger.debug("\tpayload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["username"], payload["password"])

        cur.execute("select loginUser('{0}','{1}');".format(
            values[0], values[1]))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()
        token = response[0][0]
        if(token in ['-4', '-3', '-2', '-1']):
            content = {'erro': 400}
        else:
            content = {'authToken': token}
            session["authToken"] = token

    except (Exception) as error:
        print(error)
        content = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
########## Create Auction #############
#######################################


@app.route("/dbproj/leilao/", methods=['POST'])
def create_auction():
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info("[POST] /leilao/")
    payload = request.get_json(force=True)
    logger.debug("\tpayload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["titulo"], payload["descricao"], payload["data_inicio"],
                  payload["data_fim"], payload["precoMinimo"], payload["artigoId"])

        cur.execute("select createAuction('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');".format(
            idUser, values[0], values[1], values[2], values[3], int(values[4]), int(values[5])))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()
        id = response[0][0]
        if(id in [-4, -3, -2, -1]):
            content = {'erro': 400}
        else:
            content = {'leilaoId': id}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
##### List Auctions In Progress #######
#######################################


@app.route("/dbproj/leiloes/", methods=['GET'])
def get_autions_in_progress():
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info("[GET] /leilao/")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("select * from listLeiloes();")
    response = cur.fetchall()
    logger.debug("\tresponse: {0}".format(response))
    payload = []
    for row in response:
        content = {'id': int(row[0]), 'descricao': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

#######################################
# List Auctions In Progress by Keyword
#######################################


@app.route("/dbproj/leiloes/<keyword>", methods=['GET'])
def get_autions_in_progress_by_keyword(keyword):
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info(f'[GET] /leilao/{keyword}/')

    conn = db_connection()
    cur = conn.cursor()

    cur.execute(
        "select * from listLeiloesFromKeyword({0});".format("'"+keyword+"'"))
    response = cur.fetchall()
    logger.debug("\tresponse: {0}".format(response))
    payload = []
    for row in response:
        content = {'id': int(row[0]), 'descricao': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

#######################################
######## List Auction by ID ###########
#######################################


@app.route("/dbproj/leilao/<id>", methods=['GET'])
def get_leilao_info(id):
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info(f'[GET] dbproj/Leilao/{id}')

    conn = db_connection()
    cur = conn.cursor()

    # Vencedor Info
    cur.execute("select * from getVencedor({0})".format(id))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    vencedor_info = {}
    if(rows):
        row = rows[0]
        vencedor_info = {'vencedor': row[0], 'valor final': row[1], 'tempo': row[2]}
    else:
        vencedor_info = {'vencedor': 'Vencedor ainda não determinado'}

    # Leilao Info
    cur.execute("select * from getLeilaoInfo({0})".format(id))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    leilao_info = {}
    if(rows):
        row = rows[0]
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2],
                       'data de inicio': row[3], 'data de fim': row[4], 'preco inicial': row[5]}

    # Licitacao Info
    cur.execute("select * from getLeilaoLicitacoes({0})".format(id))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    licitacoes = []
    if(rows):
        for row in rows:
            licitacao = {'data': row[2], "preco": row[0], 'licitador': row[1]}
            licitacoes.append(licitacao)

    # Mensagem Info
    cur.execute("select * from getLeilaoMensagens({0})".format(id))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    mensagens = []
    if(rows):
        for row in rows:
            mensagem = {'titulo': row[0], "descricao": row[1],
                        'data': row[2], 'licitador': row[3]}
            mensagens.append(mensagem)

    # Historico Info
    cur.execute("SELECT * from getLeilaoHistorico({0})".format(id))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    historico = []
    if(rows):
        for row in rows:
            past = {
                'titulo antigo': row[0], 'descricao antiga': row[1], 'data de alteracao': row[2]}
            historico.append(past)

    total = {'vencedor': vencedor_info,'info': leilao_info, 'licitacoes': licitacoes,'mensagens': mensagens, 'historico': historico}

    conn.close()
    return jsonify(total)


#######################################
######### List Auctions of User #######
#######################################

@app.route("/dbproj/atividade/", methods=['GET'])
def get_pessoa_activity():
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info(f'[GET] dbproj/atividade/')

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("select * from getCreatedAuctions({0});".format(idUser))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    criados = []
    for row in rows:
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2]}
        criados.append(leilao_info)

    cur.execute("select * from getLicitedAuctions({0});".format(idUser))
    rows = cur.fetchall()
    logger.debug("\tresponse: {0}".format(rows))
    licitados = []
    for row in rows:
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2]}
        licitados.append(leilao_info)

    total = {"leiloes criados": criados, "leiloes licitados": licitados}
    conn.close()
    return jsonify(total)

#######################################
########## Edit Auction ###############
#######################################


@app.route("/dbproj/leilao/<id>", methods=['POST'])
def edit_auction(id):
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info('[POST] /leilao/{id}')
    payload = request.get_json(force=True)
    logger.debug("\tpayload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["titulo"], payload["descricao"])

        cur.execute("select editAuction({0}, '{1}','{2}');".format(
            id, values[0], values[1]))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()

        id = response[0][0]
        if(id in [-4, -3, -2, -1]):
            content = {'erro': 400}
        else:
            content = {'leilaoId': id}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
######### Make Licitation #############
#######################################


@app.route("/dbproj/licitar/<id>/<value>", methods=['GET'])
def create_licitation(id, value):
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info(f'[GET] dbproj/licitar/{id}/{value}')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("select createLicitation('{0}','{1}','{2}');".format(
            idUser, id, value))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()
        token = response[0][0]
        if(token in [-4, -3, -2, -1]):
            content = {'erro': 400}
        else:
            content = {'status': 200}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}
    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)


#######################################
#######  Obtain Notifications #########
#######################################

@app.route("/dbproj/notificacoes/", methods=['GET'])
def get_notifications():
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)
    logger.info("[GET]  /notificacoes/")

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("select * from listNotifications('{0}');".format(idUser))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        cur.execute("select markNotificationAsRead('{0}');".format(idUser))
        conn.commit()
        notifications = []
        for row in response:
            notification = {'mensagem': row[0]}
            notifications.append(notification)

    except (Exception) as error:
        print(error)
        notifications = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(notifications)

#######################################
######## Write in Message Board #######
#######################################


@app.route("/dbproj/mural/", methods=['POST'])
def post_in_message_board():
    idUser = checkLogin()
    if(idUser == -1):
        content = {'erro': 401}
        return jsonify(content)

    logger.info("[POST] /mural/")
    payload = request.get_json(force=True)
    logger.debug("\tpayload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["leilaoId"], payload["titulo"], payload["descricao"])

        cur.execute("select PostMessageOnBoard('{0}', '{1}', '{2}', '{3}');".format(
            idUser, values[0], values[1], values[2]))
        response = cur.fetchall()
        logger.debug("\tresponse: {0}".format(response))
        conn.commit()
        id = response[0][0]
        if(id in [-4, -3, -2, -1]):
            content = {'erro': 400}
        else:
            content = {'status': 200}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
#### Check if Client is Logged in #####
#######################################


def checkLogin():
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""
                        select getPessoaByAuthToken('{0}'); 
                        """.format(session['authToken']))
        response = cur.fetchall()
        id = response[0][0]
        return id
    except (KeyError) as error:
        return -1

#######################################
##### Database connection #############
#######################################


def db_connection():
    configParser = configparser.RawConfigParser()
    configFilePath = "python/app/properties.txt"
    configParser.read(configFilePath)

    DB_IP = configParser.get('config', 'DB_IP')
    DB_Port = configParser.get('config', 'DB_Port')
    DB_User = configParser.get('config', 'DB_User')
    DB_Password = configParser.get('config', 'DB_Password')
    DB_Name = configParser.get('config', 'DB_Name')

    db = psycopg2.connect(user=DB_User, password=DB_Password,
                          host=DB_IP, port=DB_Port, database=DB_Name)
    db.autocommit = False
    return db

#######################################
############### Main ##################
#######################################


if __name__ == "__main__":
    # Set up the logging
    logging.basicConfig(filename="./logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    # "%Y-%m-%d %H:%M:%S") # not using DATE to simplify
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    time.sleep(1)  # just to let the DB start before this print :-)

    app.secret_key = "any random string"
    app.run(host="localhost", port=8080, debug=True, threaded=True)
