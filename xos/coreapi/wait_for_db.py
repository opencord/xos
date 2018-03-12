import psycopg2
import sys
import time
import traceback

from xosconfig import Config

Config.init()

def wait_for_database():
    while True:
        db_name = Config.get("database.name")
        db_user = Config.get("database.username")
        db_password = Config.get("database.password")
        db_host = "xos-db"  # TODO: this should be configurable
        db_port = 5432      # TODO: this should be configurable

        try:
            myConnection = psycopg2.connect(host = db_host, port = db_port,
                                            user = db_user, password = db_password)



            myConnection.close()

            # Exit on successful connection
            print "Database is available"
            return
        except:
            traceback.print_exc("Exception while connecting to db")
            time.sleep(1)

wait_for_database()
