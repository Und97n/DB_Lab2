from controller import Controller
import utils
from model import Model
from view import View


def main():
    enter_host = False
    enter_password = False
    view = View()
    controller = Controller(Model((view.request_input("Enter host:") if enter_host else "127.0.0.1"),
                                  (view.request_input("Enter password:")) if enter_password else "1"),
                            view)
    controller.start()


if __name__ == '__main__':
    main()
