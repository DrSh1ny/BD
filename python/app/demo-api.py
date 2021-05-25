from flask import Flask, jsonify, request
import logging
import psycopg2
import time
import configparser 
import ast

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

@app.route("/dbproj/leilao/", methods=['GET'])
def get_autions_in_progress():
    logger.info("###              DEMO: GET /leilao              ###")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
                    select * from listLeiloes();
                    """)
    response = cur.fetchall()
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

@app.route("/dbproj/leilao/<keyword>", methods=['GET'])
def get_autions_in_progress_by_keyword(keyword):
    logger.info("###              DEMO: GET /leilao<keyword>              ###")
    logger.debug(f'keyword: {keyword}')

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
                    select * from listLeiloesFromKeyword({0});
                    """.format("'"+keyword+"'"))
    response = cur.fetchall()
    payload=[]
    for row in response:
        logger.debug(row)
        content = {'id': int(row[0]), 'descricao': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

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

    logger.info("\n---------------------------------------------------------------\n" +
                "API v1.0 online: http://localhost:8080/departments/\n\n")

    app.run(host="localhost", port=8080, debug=True, threaded=True)
