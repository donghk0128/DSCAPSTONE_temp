# my_style.py
import matplotlib.pyplot as plt
import platform

def set_korean():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    else:
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False