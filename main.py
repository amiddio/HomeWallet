from models.scheme import init_db, TypeEnum
from widgets.app import App


def main():
    init_db()
    # import_data(file_name='./import/expense.csv', type_=TypeEnum.VOUT)
    # import_data(file_name='./import/incoming.csv', type_=TypeEnum.VIN)
    App().mainloop()


if __name__ == '__main__':
    main()
