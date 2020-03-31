from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import requests
import json
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import sys
import pandas as pd
from random import choice


matplotlib.pyplot.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.pyplot.rcParams['axes.unicode_minus'] = False



def getGlobalXY(address):
    gdf = pd.read_csv("D:\\VSCode\\PythonProject\\GA.csv", index_col=['城市名中文'],encoding='utf-8')
    res=gdf.纬度.loc[address],gdf.经度.loc[address]
    return res

def getChinaXY(address):
    df=pd.read_csv("D:\\VSCode\\PythonProject\\CA.csv" ,index_col=['district'],encoding='utf-8')
    try:
        x,y= df.lng.loc[address],df.lat.loc[address]
        if float(x):
            return x,y
        if isinstance(x,'pandas.core.series.Series'):
            if float(x[0]):
                return x[0],y[0]
    except:
        try:
            print(2)
            x,y= df.lng.loc[address+"省"],df.lat.loc[address+"省"]
            if float(x):
                return x,y
            if isinstance(x,'pandas.core.series.Series'):
                if float(x[0]):
                    return x[0],y[0]
        except:
            try:
                print(3)
                x,y= df.lng.loc[address+"市"],df.lat.loc[address+"市"]
                if float(x):
                    return x,y
                if isinstance(x,'pandas.core.series.Series'):
                    if float(x[0]):
                        return x[0],y[0]
            except:
                try:
                    print(4)
                    x,y= df.lng.loc[address+"县"],df.lat.loc[address+"县"]
                    if float(x):
                        return x,y
                    if isinstance(x,'pandas.core.series.Series'):
                        if float(x[0]):
                            return x[0],y[0]
                except:
                    try:
                        print(5)
                        x,y= df.lng.loc[address+"区"],df.lat.loc[address+"区"]
                        if float(x):
                            return x,y
                        if isinstance(x,'pandas.core.series.Series'):
                            if float(x[0]):
                                return x[0],y[0]
                    except:
                        fuck


def getXY(address):
    try:
        return getChinaXY(address)
    except:
        try:
            return getGlobalXY(address)
        except:
            return 0

def getWeaData(address):
    temp=getXY(address)
    if not temp:
        return "查询失败！",["HAIL","HEAVY_HAZE","STORM_SNOW","HEAVY_HAZE","HAIL"],[100,0,100,0,100],[0,100,0,100,0],[6,6,6,6,6]
    x,y=temp
    # r = requests.get('https://www.tianqiapi.com/api?version=v1&appid=22688751&appsecret=1FBjE3aD&city=%s' % address)
    r=requests.get("https://api.caiyunapp.com/v2/vXrEEGJlGcyJBmmj/%s,%s/forecast.json"%(x,y))
    r.encoding = "utf-8"
    day5temMax=[]
    day5temMin=[]
    day5Name=[]
    jt = json.loads(r.text)
    for i in jt['result']['daily']['temperature']:
        day5temMax.append(i['max'])
        day5temMin.append(i['min'])
        day5Name.append(i['date'])
    day5humMax=[]
    day5humMin=[]
    day5humAvg=[]
    for i in jt['result']['daily']['humidity']:
        day5humMax.append(i['max'])
        day5humMin.append(i['min'])
        day5humAvg.append(i['avg'])
    day5sky=[]
    for i in jt['result']['daily']['skycon']:
        day5sky.append(i['value'])
    day5preMax=[]
    for i in jt['result']['daily']['precipitation']:
        day5preMax.append(i['max'])
    return day5Name,day5sky,day5temMax,day5temMin,day5preMax



Days,skycon,Max,Min,preMax = getWeaData(sys.argv[1])

wea=["晴" if x=="CLEAR_DAY" else "多云" if x=="PARTLY_CLOUDY_DAY" else "阴" if x=="CLOUDY" else "雨" if x=="RAIN" else "雪" if x=="SNOW" else "轻度雾霾" if x=="LIGHT_HAZE" else "中度雾霾" if x=="MODERATE_HAZE" else "重度雾霾" if x=="HEAVY_HAZE" else "小雨" if x=="LIGHT_RAIN" else "中雨" if x=="MODERATE_RAIN" else "大雨" if x=="HEAVY_RAIN" else "暴雨" if x=="STORM_RAIN" else "雾" if x=="FOG" else "小雪" if x=="LIGHT_SNOW" else "中雪" if x=="MODERATE_SNOW" else "大雪" if x=="HEAVY_SNOW" else "暴雪" if x=="STORM_SNOW" else "浮尘" if x=="DUST" else "沙尘" if x=="SAND" else "大风" if x=="WIND" else "雷阵雨" if x=="THUNDER_SHOWER" else "冰雹" if x=="HAIL" else "雨夹雪" if x=="SLEET" else "???" for x in skycon]
T = [0, 1, 2, 3, 4]
x = T
y = Max
print(T)


plt.subplot(211)
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
#


# 文字标签i
for i in x:
    plt.text(i, Max[i] +(max(Max)-min(Min))/50, Max[i])
    plt.text(i, Min[i] - (max(Max)-min(Min))/25, Min[i])
    # plt.text(i-len(wea[i])*0.00005,(Min[i] + Max[i])/2, wea[i])

# 标题
plt.title(sys.argv[1]+"天气")

# 日期标签
x_labels = Days

# y轴标签
plt.xticks(x, wea, rotation='0')
plt.ylabel("摄氏度 ℃")

colors=["#FF0000","#00FF00","#0000FF","#66ccff","#000000"]
# 填充两条曲线
plt.fill_between(Ex_points, max_smooth_line, min_smooth_line, color=choice(colors), alpha=0.25)


#降水
plt.subplot(212)

plt.xticks(x, x_labels, rotation='0')
plt.ylabel("降水量 mm")
plt.bar([0,1,2,3,4], preMax,color="#66ccff")

plt.rcParams['savefig.dpi'] = 150  # 图片像素
plt.rcParams['figure.dpi'] = 10

# plt.show()
# gcf: Get Current Figure
fig = plt.gcf()
path="D:\\VSCode\\PythonProject\\Service\\temp\\"+sys.argv[2]+".png"
fig.savefig(path)
