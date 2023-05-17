import psycopg2

# ensure correct connection config aka port to Docker otherwise its defaults to port 5432 (same for username and password, etc)
con = psycopg2.connect("dbname='todo' user='italizvazquez' host='localhost' password='postgres'")
cur = con.cursor()
