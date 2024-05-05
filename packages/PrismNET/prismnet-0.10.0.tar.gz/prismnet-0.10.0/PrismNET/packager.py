import os
import sys
import time
import random
import shutil
class PrismNET:
    def create_file(filename):
        if os.path.exists(filename):
            os.remove(filename)
        os.mknod(filename)
    def delete_file(filename):
        if os.path.exists(filename):
            os.remove(filename)
    def create_dir(dirname):
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.mkdir(dirname)
    def delete_dir(dirname):
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
    def get_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    def get_random_string(length):
        return ''.join(random.choice('0123456789abcdef') for _ in range(length))
    def get_random_number(length):
        return ''.join(random.choice('0123456789') for _ in range(length))
    def get_random_lowercase(length):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))  
    def get_random_uppercase(length):
        return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length))
    def check_file_exists(filename):
        if os.path.exists(filename):
            return True
        else:
            return False
    def find_file(filename):
        if os.path.exists(filename):
            return True
        else:
            return False
    def check_dir_exists(dirname):
        if os.path.exists(dirname):
            return True
        else:
            return False    