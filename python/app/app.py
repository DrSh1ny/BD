from flask import Flask, jsonify, request
import logging, psycopg2, time

app = Flask(__name__) 




##
##      GET
##
## Obtain leiloes
##
## To use it, access: 
## 
##   http://localhost:8080/dbproj/leiloes
##

@app.route("/dbproj/leiloes", methods=['GET'])
def get_leiloes():

    logger.info("###              DEMO: GET dbproj/Leiloes             ###");   


    conn = db_connection()
    cur = conn.cursor()


    ## Leilao Info
    cur.execute("SELECT id, titulo, descricao, data_inicio, data_fim, preco_inicial FROM leilao" )
    rows = cur.fetchall()

    logger.debug("---- selected Leilao  ----")
    leiloes = []
    for row in rows:

        logger.debug(row)
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}
        leiloes.append(leilao_info)

    conn.close ()
    return jsonify(leiloes)


##
##      GET
##
## Obtain leilao with keyword <keyword>
##
## To use it, access: 
## 
##   http://localhost:8080/dbproj/leiloes/jogo
##

@app.route("/dbproj/leiloes/<keyword>", methods=['GET'])
def get_leilao_by_keyword(keyword):
    logger.info("###              DEMO: GET dbproj/Leilao/<keyword>              ###");   

    logger.debug(f'keyword: {keyword}')

    conn = db_connection()
    cur = conn.cursor()


    ## Leilao Info
    cur.execute("SELECT id, titulo, descricao, data_inicio, data_fim, preco_inicial FROM leilao where descricao like '%%s%'",(keyword,) )
    rows = cur.fetchall()

    logger.debug("---- selected Leilao  ----")
    leiloes = []
    for row in rows:

        logger.debug(row)
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}
        leiloes.append(leilao_info)

    conn.close ()
    return jsonify(leiloes)

##
##      GET
##
## Obtain leilao with id <id>
##
## To use it, access: 
## 
##   http://localhost:8080/dbproj/leilao/10
##

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
    cur.execute("SELECT preco, data, pessoa.nome FROM licitacao, pessoa where  licitacao.pessoa_id = pessoa.id and  id = %s", (id,) )
    rows = cur.fetchall()

    row = rows[0]

    logger.debug("---- best licitacao  ----")
    logger.debug(row)
    pessoa_id = row[2];
    licitacao_info= {'preco': row[0], 'data_licitacao': row[1], 'nome_licitacao': row[2]}



    ## Mensagem Info
    cur.execute("SELECT titulo, descricao, data, pessoa.nome FROM licitacao, pessoa where licitacao.pessoa_id = pessoa.id and id = %s", (id,) )
    rows = cur.fetchall()

    logger.debug("---- Mensagens  ----")
    mensagens = []
    for row in rows:
        logger.debug(row)
        mensagem = {'titulo_mensagem': row[0], "descricao_mensagem" : row[1], 'data_mensagem': row[2], 'nome_mensagem': row[3]}
        mensagens.append(mensagem);



    ## Historico Info
    cur.execute("SELECT titulo, descricao, data_alteracao FROM historico where and id = %s", (id,) )
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



##
##      GET
##
## Obtain leiloes by <pessoa_id>
##
## To use it, access: 
## 
##   http://localhost:8080/dbproj/pessoa/10
##



@app.route("/dbproj/pessoa/<id>", methods=['GET'])
def get_leilao_info(id):
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

    logger.debug("---- selected Leilao  ----")
    licitados = []
    for row in rows:
        logger.debug(row)
        leilao_info = {'id': row[0], 'titulo': row[1], 'descricao': row[2], 'data_inicio': row[3], 'data_fim' :row[4], 'preco_inicial': row[5]}
        licitados.append(leilao_info)
    

    total = {"criados": criados, "licitados": licitados}
    conn.close ()
    return jsonify(total)

##
##      GET
##
## Obtain licitacao in <leilaoId> with <value>
##
## To use it, access: 
## 
##   http://localhost:8080/dbproj/licitar/10/100
##



@app.route("/dbproj/leilao/<id>/<value>", methods=['GET'])
def get_leilao_info(id, value):
    logger.info("###              DEMO: GET dbproj/licitar/<id>/<value>              ###");   

    logger.debug(f'id: {id}, value: {value}')

    conn = db_connection()
    cur = conn.cursor()

    tempo = time.now();
    try:
        cur.execute("""
                        select createLicitation('{0}','{1}','{2}');
                        """.format(id,value, tempo))
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






##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    db = psycopg2.connect(user = "aulaspl",
                            password = "aulaspl",
                            host = "db",
                            port = "5432",
                            database = "dbfichas")
    return db


##########################################################
## MAIN
##########################################################
if __name__ == "__main__":

    # Set up the logging
    logging.basicConfig(filename="logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s',
                              '%H:%M:%S')
                              # "%Y-%m-%d %H:%M:%S") # not using DATE to simplify
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    time.sleep(1) # just to let the DB start before this print :-)


    logger.info("\n---------------------------------------------------------------\n" + 
                  "API v1.0 online: http://localhost:8080/departments/\n\n")


    

    app.run(host="0.0.0.0", debug=True, threaded=True)