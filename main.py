from App.model import DB_Charmer
from App.view import API_Charmer
from App.controller import MicroApp

def main():
    db = DB_Charmer()
    api = API_Charmer()
    app = MicroApp(db, api)
    app.daemon_check()

if __name__ == "__main__":
    main()