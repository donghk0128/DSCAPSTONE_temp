# plt 한글 깨짐 우회 코드 (윈도우, 맥)
import matplotlib.pyplot as plt
import platform

def set_korean():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    else:
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False