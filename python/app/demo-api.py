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

@app.route("/user/", methods=['GET'])
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

@app.route("/user/", methods=['POST'])
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
        content = {'erro': 412}     

    finally:
        if conn is not None:
            conn.close()
    return jsonify(content)
    




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
