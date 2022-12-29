import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import math

def radToDeg(rad):
  return rad*360/(2*np.pi)

# 逆運動学の計算
def ik(L, p2):
  x, y = p2
  l1, l2 = L
  d = math.sqrt((x*x) + (y*y))
  if x<0:
    th2 = math.pi - math.acos(((l1*l1) + (l2*l2) - ( d * d)) / (2*l1*l2))
    th1 = math.atan2(y , x) - math.acos(((l1*l1) + (d * d) - (l2*l2)) / (2*l1*d))
  else:
    th2 = math.pi + math.acos(((l1*l1) + (l2*l2) - ( d * d)) / (2*l1*l2))
    th1 = math.atan2(y , x) + math.acos(((l1*l1) + (d * d) - (l2*l2)) / (2*l1*d))
  return [th1, th2]

# 順運動学の計算
def fk(L, th):
  # 各リンクの長さと関節角度の取得
  l1, l2 = L
  th1, th2 = th
  # リンク1の手先
  x1 = l1 * math.cos(th1)
  y1 = l1 * math.sin(th1)
  # リンク2の手先
  x2 = x1 + l2 * math.cos(th1 + th2)
  y2 = y1 + l2 * math.sin(th1 + th2)
  # 手先位置をNumPy配列に格納して返す
  return np.array([[0, 0], [x1, y1], [x2, y2]])

def update(event, L, p2, graph, fig):
  # print('xdata=%f, ydata=%f' %(event.xdata, event.ydata))
  # 関節の角度を更新
  p2[0] = float(event.xdata)
  p2[1] = float(event.ydata)
  th = ik(L, p2)
  p = fk(L, th)
  # 手先位置を更新
  graph.set_data(p.T[0], p.T[1])
  set_graph(graph)
  # グラフの再描画
  fig.canvas.draw_idle()

def set_graph(graph):
  graph.set_linestyle('-')
  graph.set_linewidth(5)
  graph.set_marker('o')
  graph.set_markerfacecolor('m')
  graph.set_markeredgecolor('m')
  graph.set_markersize(15)

def main():
  # リンク1, 2の長さ
  L = [0.5, 0.7]
  p2 = [0.5, 0.5]
  # 第1, 2の関節角度
  #th = np.radians([90, 0])
  # 順運動学の計算
  th = ik(L, p2)
  p = fk(L, th)
  # グラフ描画位置の設定
  fig, ax = plt.subplots()
  plt.axis('equal')
  plt.subplots_adjust(left=0.1, bottom=0.15)
  plt.xlim([-(L[0]+L[1]), L[0]+L[1]])
  plt.ylim([-(L[0]+L[1]), L[0]+L[1]])
  # グラフ描画
  plt.grid()
  graph, = plt.plot(p.T[0], p.T[1])
  event=None
  fig.canvas.mpl_connect("button_press_event",lambda event:update(event, L,p2, graph, fig))
  r = patches.Rectangle(xy=(-0.05, -(L[0]+L[1])), width=0.1, height=L[0]+L[1], color='k')
  c = patches.Circle(xy=(0, 0), radius=L[0]+L[1], fc='w', ec='r')
  ax.add_patch(c)
  ax.add_patch(r)
  set_graph(graph)
  plt.grid()
  plt.show()

if __name__ == '__main__':
    main()
