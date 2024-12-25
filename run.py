import os
import threading
 
def main():
    os.system(r'python /Users/arina/Documents/service/main.py')
def db():
    os.system(r'python /Users/arina/Documents/service/db.py')
def descr():
    os.system(r'python /Users/arina/Documents/service/descriptions.py')
def prod():
    os.system(r'python /Users/arina/Documents/service/products.py')

main_t = threading.Thread(target=main)
db_t = threading.Thread(target=db)
descr_t = threading.Thread(target=descr)
prod_t = threading.Thread(target=prod)

main_t.start()
db_t.start()
descr_t.start()
prod_t.start()
