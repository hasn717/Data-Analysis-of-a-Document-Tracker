import datetime
import json
import os
from argparse import ArgumentParser


from GUI import GUI
from MainClass import MainClass


if __name__ == '__main__':
    #CLI
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-u', '--user_uuid', type=str, action='store', help='User id you want to query with')
    arg_parser.add_argument('-d', '--document_uuid', type=str, action='store', help='Document id you want to query with')
    arg_parser.add_argument('-t', '--task', type=str, action='store', choices=['2a', '2b', '3a', '3b', '4', '5d', '6', '7'], help='Coursework task that you want to test')
    arg_parser.add_argument('-s', '--sorter', type=str, action='store', help='Sorter for Task 5d')
    
    args = vars(arg_parser.parse_known_args()[0])

    if args['task'] == '7' or args['task'] is None:
        args = vars(arg_parser.parse_args())
        gui = GUI()
    else:
        requiredNamed = arg_parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-f', '--file_name', type=str, action='store', help='File name containing JSON data', required=True)
        args = vars(arg_parser.parse_args())
        MainClass().runTasks(args)
