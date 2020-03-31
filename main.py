from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import requests
import json
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import sys
from random import choice


matplotlib.pyplot.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.pyplot.rcParams['axes.unicode_minus'] = False

def getWeaData(address):
    r = requests.get('https://www.tianqiapi.com/api?version=v1&appid=22688751&appsecret=1FBjE3aD&city=%s' % address)
    r.encoding = "utf-8"
    daysMax = []
    daysMin = []
    wea=[]
    T = []
    jt = json.loads(r.text)
    for d in jt['data']:
        T.append(d['day'])
        daysMax.append(int(d['tem1'][:-1]))
        daysMin.append(int(d['tem2'][:-1]))
        wea.append(d['wea'])
    return wea,T, daysMax, daysMin

wea,Days, Max, Min = getWeaData(sys.argv[1])
T = [0, 1, 2, 3, 4, 5, 6]
x = T
y = Max
print(Max,Min)

# 打印点和曲线最高温
plt.scatter(x, Max, c='r')
generate_Y = make_interp_spline(x, Max, k=3)
Ex_points = np.linspace(min(x), max(x), 300)  # 扩展锚点
max_smooth_line = generate_Y(Ex_points)
plt.plot(Ex_points, max_smooth_line, c='r')

# 打印点和曲线最低温
plt.scatter(x, Min, c='b')
generate_Y = make_interp_spline(x, Min, k=3)
Ex_points = np.linspace(min(x), max(x), 300)
min_smooth_line = generate_Y(Ex_points)
plt.plot(Ex_points, min_smooth_line, c='b')

# 文字标签
for maxitem in x:
    plt.text(maxitem, Max[maxitem] +(max(Max)-min(Min))/50, Max[maxitem])
    plt.text(maxitem, Min[maxitem] - (max(Max)-min(Min))/25, Min[maxitem])
    plt.text(maxitem-len(wea[maxitem])*0.087, (Min[maxitem] + Max[maxitem])/2, wea[maxitem])

plt.title(u"%s天气"%sys.argv[1])
x_labels = Days
plt.xticks(x, x_labels, rotation='10')
plt.ylabel("摄氏度 ℃")
colors=["#FF0000","#00FF00","#0000FF"]
plt.fill_between(Ex_points, max_smooth_line, min_smooth_line, color=choice(colors), alpha=0.3)
plt.rcParams['savefig.dpi'] = 150  # 图片像素
plt.rcParams['figure.dpi'] = 20


fig = plt.gcf()
path="D:\\VSCode\\PythonProject\\Service\\temp\\"+sys.argv[2]+".png"
fig.savefig(path)
