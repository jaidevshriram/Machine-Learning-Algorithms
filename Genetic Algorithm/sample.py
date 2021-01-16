from local_settings import *
from client_moodle import *
from colorama import Fore

TEST = [-2.969319343154344e-11, 1.8715420139593866, -6.922088493160181, 0.06549782444542824, 0.03870620199603078, 9.28803139883789e-05, -6.01876914689282e-05, -1.2957851278314178e-07, 3.484096383229683e-08, 3.825538145448347e-11, -6.732420176902685e-12]

fitness = get_errors(KEY, BEST)
print(TEST)
print(Fore.GREEN + str((fitness[0] + fitness[1])/2) + Fore.RESET, fitness)