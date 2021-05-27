from flask import Flask, jsonify, request
import logging
import psycopg2
import time
import configparser 

app = Flask(__name__)

#######################################
########## Obtain All Users ###########
#######################################

@app.route("/dbproj/user/", methods=['GET'])
def get_all_user():
    logger.info("###              DEMO: GET /user              ###")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
                    select * from listUsers();
                    """)
    response = cur.fetchall()
    logger.debug("response: {0}".format(response))
    payload=[]
    for row in response:
        logger.debug(row)
        content = {'id': int(row[0]), 'nome': row[1], 'email': row[2]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

#######################################
########## Create New User ############
#######################################

@app.route("/dbproj/user/", methods=['POST'])
def add_user():
    logger.info("###              DEMO: POST /user              ###")
    payload = request.get_json(force=True)
    logger.debug("payload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["username"], payload["email"], payload["password"])
        
        cur.execute("""
                        select registeruser('{0}', '{1}', '{2}'); 
                        """.format(values[0],values[1],values[2]))
        response = cur.fetchall()
        logger.debug("response: {0}".format(response))
        conn.commit()
        id=response[0][0]
        if(id in [-3,-2,-1]):
            content={'erro':412}
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
    logger.info("###              DEMO: PUT /user              ###")
    payload = request.get_json(force=True)
    logger.debug("payload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["username"],payload["password"])
        
        cur.execute("""
                        select loginUser('{0}','{1}');
                        """.format(values[0],values[1]))
        response = cur.fetchall()
        logger.debug("response: {0}".format(response))
        conn.commit()
        token=response[0][0]
        if(token in [-1,-2,-3]):
            content={'erro':412}
        else:
            content = {'authToken': token}

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
    logger.info("###              DEMO: POST /leilao              ###")
    payload = request.get_json(force=True)
    logger.debug("payload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["authToken"], payload["titulo"], payload["descricao"],payload["data_inicio"],payload["data_fim"],payload["precoMinimo"],payload["artigoId"])
        
        cur.execute("""
                        select createAuction('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'); 
                        """.format(values[0],values[1],values[2],values[3],values[4],int(values[5]),int(values[6])))
        response = cur.fetchall()
        logger.debug("response: {0}".format(response))
        conn.commit()
        id=response[0][0]
        if(id in [-3,-2,-1]):
            content={'erro':412}
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
    logger.info("###              DEMO: GET /leilao              ###")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
                    select * from listLeiloes();
                    """)
    response = cur.fetchall()
    logger.debug("response: {0}".format(response))
    payload=[]
    for row in response:
        logger.debug(row)
        content = {'id': int(row[0]), 'descricao': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

#######################################
# List Auctions In Progress by Keyword 
#######################################

@app.route("/dbproj/leiloes/<keyword>", methods=['GET'])
def get_autions_in_progress_by_keyword(keyword):
    logger.info("###              DEMO: GET /leilao<keyword>              ###")
    logger.debug(f'keyword: {keyword}')

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
                    select * from listLeiloesFromKeyword({0});
                    """.format("'"+keyword+"'"))
    response = cur.fetchall()
    logger.debug("response: {0}".format(response))
    payload=[]
    for row in response:
        logger.debug(row)
        content = {'id': int(row[0]), 'descricao': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

#######################################
# List Auction by ID 
#######################################

@app.route("/dbproj/leilao/<id>", methods=['GET'])
def get_leilao_info(id):
    logger.info("###              DEMO: GET dbproj/Leilao/<id>              ###");   

    logger.debug(f'id: {id}')

    conn = db_connection()
    cur = conn.cursor()


    ## Leilao Info
    cur.execute("SELECT id, titulo, descricao, data_inicio, data_fim, preco_inicial FROM leilao where id = %s", (id,) )
    rows = cur.fetchall()

    row = rows[0]

    logger.debug("---- selected Leilao  ----")
    logger.debug(row)
    leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}

    

    ## Licitacao Info
    cur.execute("SELECT preco, data, pessoa.nome FROM licitacao, pessoa where  licitacao.pessoa_id = pessoa.id and  leilao_id = %s", (id,) )
    rows = cur.fetchall()
    licitacao_info={}
    if(rows):
        row = rows[0]

        logger.debug("---- best licitacao  ----")
        logger.debug(row)
        pessoa_id = row[2];
        licitacao_info= {'preco': row[0], 'data_licitacao': row[1], 'nome_licitacao': row[2]}



    ## Mensagem Info
    cur.execute("SELECT titulo, descricao, data, pessoa.nome FROM mensagem,pessoa where mensagem.pessoa_id = pessoa.id and leilao_id = %s", (id,) )
    rows = cur.fetchall()

    logger.debug("---- Mensagens  ----")
    mensagens = []
    for row in rows:
        logger.debug(row)
        mensagem = {'titulo_mensagem': row[0], "descricao_mensagem" : row[1], 'data_mensagem': row[2], 'nome_mensagem': row[3]}
        mensagens.append(mensagem);



    ## Historico Info
    cur.execute("SELECT titulo, descricao, data_alteracao FROM historico where leilao_id = %s", (id,) )
    rows = cur.fetchall()

    logger.debug("---- Historico  ----")
    historico = []
    for row in rows:
        logger.debug(row)
        past = {'titulo_antigo': row[0], 'descricao_antiga': row[1], 'data_alteracao': row[2]}
        historico.append(past)
    


    
    total = {'info': leilao_info, 'licitacao': licitacao_info, 'mensagens': mensagens, 'historico': historico}

    conn.close ()
    return jsonify(total)


#######################################
# List Auctions of User
#######################################

@app.route("/dbproj/pessoa/<id>", methods=['GET'])
def get_pessoa_activity(id):
    logger.info("###              DEMO: GET dbproj/pessoa/<id>/              ###");   

    logger.debug(f'id: {id}')

    conn = db_connection()
    cur = conn.cursor()

    ## Leilao Info
    cur.execute("SELECT id, titulo, descricao, data_inicio, data_fim, preco_inicial FROM leilao where pessoa_id = %s", (id,) )
    rows = cur.fetchall()

    logger.debug("---- selected Leilao  ----")
    criados = []
    for row in rows:
        logger.debug(row)
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}
        criados.append(leilao_info)

    

    cur.execute("select  leilao.id, leilao.titulo, leilao.descricao, leilao.data_inicio, leilao.data_fim, leilao.preco_inicial from leilao, licitacao where licitacao.leilao_id = leilao.id and licitacao.pessoa_id =%s", (id,))
    rows = cur.fetchall()
    logger.debug("---- selected Leilao  ----")
    licitados = []
    for row in rows:
        logger.debug(row)
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}
        licitados.append(leilao_info)
    

    total = {"criados": criados, "licitados": licitados}
    conn.close ()
    return jsonify(total)

#######################################
########## Edit Auction #############
#######################################

@app.route("/dbproj/leilao/<id>", methods=['POST'])
def edit_auction(id):
    logger.info("###              DEMO: POST /leilao              ###")
    payload = request.get_json(force=True)
    logger.debug("payload: {0}".format(payload))

    
    logger.debug(f'id: {id}')

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (id, payload["titulo"], payload["descricao"],payload["data_inicio"],payload["data_fim"],payload["precoMinimo"],payload["artigoId"])
        
        cur.execute("""
                        select editAuction('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'); 
                        """.format(values[0],values[1],values[2],values[3],values[4],int(values[5]),int(values[6])))
        response = cur.fetchall()
        conn.commit()
        id=response[0][0]
        if(id in [-3,-2,-1]):
            content={'erro':412}
        else:
            content = {'leilaoId': id}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}     

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)


@app.route("/dbproj/leilao/<id>/<value>", methods=['GET'])
def get_leilao_info(id, value):
    logger.info("###              DEMO: GET dbproj/licitar/<id>/<value>              ###");   

    logger.debug(f'id: {id}, value: {value}')

    conn = db_connection()
    cur = conn.cursor()

    pessoa_id = 0
    try:
        cur.execute("""
                        select createLicitation('{0}','{1}','{2}');
                        """.format(id,value, pessoa_id))
        response = cur.fetchall()
        conn.commit()
        token=response[0][0]
        if(token in [-1,-2,-3]):
            content={'erro':412}
        else:
            content = {'authToken': token}
    
    except (Exception) as error:
        print(error)
        content = {'erro': 412}     

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)
    
#######################################
######## Write in Message Board #######
#######################################

@app.route("/dbproj/mural/", methods=['POST'])
def post_in_message_board():
    logger.info("###              DEMO: POST /mural              ###")
    payload = request.get_json(force=True)
    logger.debug("payload: {0}".format(payload))

    conn = db_connection()
    cur = conn.cursor()
    try:
        values = (payload["authToken"],payload["leilaoId"], payload["titulo"], payload["descricao"])
        
        cur.execute("""
                        select PostMessageOnBoard('{0}', '{1}', '{2}', '{3}'); 
                        """.format(values[0],values[1],values[2],values[3]))
        response = cur.fetchall()
        logger.debug("response: {0}".format(response))
        conn.commit()
        id=response[0][0]
        if(id in [-3,-2,-1]):
            content={'erro':412}
        else:
            content = {'status': 'sucesso'}

    except (Exception) as error:
        print(error)
        content = {'erro': 412}     

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)

#######################################
##### Database connection #############
#######################################

def db_connection():
    configParser = configparser.RawConfigParser()
    configFilePath = "python/app/properties.txt"
    configParser.read(configFilePath)

    DB_IP= configParser.get('config', 'DB_IP')
    DB_Port= configParser.get('config', 'DB_Port')
    DB_User= configParser.get('config', 'DB_User')
    DB_Password= configParser.get('config', 'DB_Password')
    DB_Name= configParser.get('config', 'DB_Name')

    db = psycopg2.connect(user=DB_User,password=DB_Password,host=DB_IP,port=DB_Port,database=DB_Name)
    db.autocommit=False
    return db

#######################################
############### Main ##################
#######################################

if __name__ == "__main__":
    # Set up the logging
    logging.basicConfig(filename="C:/Users/franc/Desktop/BD/python/app/logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s','%H:%M:%S')
    # "%Y-%m-%d %H:%M:%S") # not using DATE to simplify
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    time.sleep(1)  # just to let the DB start before this print :-)

    app.run(host="localhost", port=8080, debug=True, threaded=True)
