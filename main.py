from controller import Controller
import utils
from model import Model
from view import View


def main():
    enter_host = False
    enter_password = False
    controller = Controller(Model((utils.request_input("Enter host:") if enter_host else "127.0.0.1"),
                                  (utils.request_input("Enter password:")) if enter_password else "1"),
                            View())
    controller.start()


if __name__ == '__main__':
    main()
