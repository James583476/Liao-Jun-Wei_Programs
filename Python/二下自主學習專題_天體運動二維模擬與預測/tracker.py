import numpy as np

X = {}  #[id,(X,P)]
pred_num = 50
return_pred = {}  #[id,(x,y)]
FPS = 60
t =  1/(FPS*12*300)   #main.py中變更模式(169~172行)必須更改此值！
F = np.array([[1,0,t,0,0.5*t**2,0],
        [0,1,0,t,0,0.5*t**2],
        [0,0,1,0,t,0],
        [0,0,0,1,0,t],
        [0,0,0,0,1,0],
        [0,0,0,0,0,1]])
H = np.array([[1,0,0,0,0,0],
        [0,1,0,0,0,0]])
q = 0.1
Q = q * np.array([
    [t**5/20, 0, t**4/8, 0, t**3/6, 0],
    [0, t**5/20, 0, t**4/8, 0, t**3/6],
    [t**4/8, 0, t**3/3, 0, t**2/2, 0],
    [0, t**4/8, 0, t**3/3, 0, t**2/2],
    [t**3/6, 0, t**2/2, 0, t, 0],
    [0, t**3/6, 0, t**2/2, 0, t]])
r = 0#noise.sigma**2  #觀測值的變異數
R = np.eye(2)*r
I = np.eye(6)
#預測
def predict(x,P):
  x_pred = F @ x
  P_pred = F @ P @ F.T + Q
  return x_pred,P_pred
#校正(z為觀測值)
def update(x_pred,P_pred,z):
  if True:#z[0]>0 and z[1]>0
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(S)#逆矩陣
    m = z - H @ x_pred
    x_new = x_pred + K @ m  #x' = x + K(z-Hx)
    P_new = (I - K @ H) @ P_pred
    return x_new,P_new,1
  else:
    return x_pred,P_pred,0

def main(data_X_old): #data_X {id: [z_x, z_y]}
  return_pred.clear()
  data_X = noise.main(data_X_old)
  for point_id, z in data_X.items():
    z_np = np.array(z, dtype=np.float64)

    if point_id not in X:
      # 初始狀態：位置設為 z，初速度設為 0
      # 狀態向量：[x, y, vx, vy, ax, ay]
      initial_x = np.zeros(6)
      initial_x[0:2] = z_np
      # P 矩陣：對位置給予小不確定性，對速度/加速度給予大不確定性
      initial_p = np.eye(6) * 0.1

      X[point_id] = (initial_x, initial_p)
      return_pred[point_id] = [(z_np[0], z_np[1])]
      continue
    curr_x, curr_p = X[point_id]
    x_pred, p_pred = predict(curr_x, curr_p)
    updated_x, updated_p, success = update(x_pred, p_pred, z_np)
    path = []
    temp_x, temp_p = updated_x.copy(), updated_p.copy()
    for _ in range(pred_num):
      temp_x, temp_p = predict(temp_x, temp_p)
      path.append((float(temp_x[0]), float(temp_x[1])))
    X[point_id] = (updated_x, updated_p) # 儲存狀態供下次呼叫使用
    return_pred[point_id] = path
  return return_pred
