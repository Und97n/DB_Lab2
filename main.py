from controller import Controller
import utils
from model import Model
from view import View


def main():
    controller = Controller(Model("127.0.0.1", "1"), View())
    controller.start()


if __name__ == '__main__':
    main()
