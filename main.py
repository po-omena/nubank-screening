import json
from operation.operation import OperationHandler
# from taxHandler import

if __name__ == '__main__':
    file = open('data.json')
    data = json.load(file)

    for operation_list in data.values():
        operation_handler = OperationHandler(operation_list)
        operation_handler.calculate_operations()


