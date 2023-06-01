from models.scheme import init_db
from widgets.app import App


def main():
    init_db()
    App().mainloop()


if __name__ == '__main__':
    main()
