# Python 語言實作內容概述

---

**二下自主學習專題_天體運動二維模擬與預測**

main.py程式概述：
* 引用tracker.py作為質點預測程式庫
* 使用pygame函式庫作質點數據可視化
* 類別Ball定義質點物理性質及是否受引力影響
* 以簡化韋爾萊積分法進行加速度的運算，減少時間不連續性的加速度誤差
* 前綴fix_的重力運算函式以numpy運算速度的優勢改善多質點的運算效能問題
* 定義三種天體模式加入主函式手動修改

tracker.py程式概述：
* 使用修改版卡爾曼濾波（統稱KFA）理論預測非線性數據
* 規定輸入與輸出質點座標格式
* 紀錄歷史座標資料用於下一次預測

[程式GIF](https://github.com/James583476/Program/blob/main/Python/image/gif_1.gif)

---

**三維模擬.py**

參考OpenGL空間投影邏輯，以平面遊戲開發程式庫pygame繪製空間座標：
* 類別Point定義立方體頂點屬性
* model_matrix作為物件基本行為定義（程式中未描寫物件行為）
* view_matrix定義相機行為（輸出相機的xy座標軸作為視角變動依據）
* projection_matrix描述透視投影邏輯
* 點更新及繪製邊緣（尚未以質點深度排序更新順序）
* mov定義相機移動邏輯
* mouse_mov定義視角變動邏輯（以滑鼠向量做view_matrix輸出之相機xy軸分量）
* 主迴圈執行矩陣運算與事件偵測

[程式GIF](https://github.com/James583476/Program/blob/main/Python/image/gif_2.gif)
![](Python/image/image_1.png)

---

**繩受力模擬.py**

結合高二選修物理牛頓力學與pygame程式庫數據可視化，模擬單擺擺動情形：
* 全域變數Do_UPDATE簡單區分物理更新及化面更新
* 定義向量的四則運算、內積、正射影及向量長度(範數)邏輯
* 類別Point定義質點屬性
* 類別Line定義連接質點間繩子的屬性
* update_1及_2表示簡化版韋爾萊積分法更新質點速度與加速度
* 主迴圈中實際模擬繩子的方式為  **質點位置更新->以兩質點權重修正繩長->修正質點位置->修正質點速度與加速度**

[程式GIF](https://github.com/James583476/Program/blob/main/Python/image/gif_3.gif)

---

**二下選修專案_終端機小遊戲**

* NOT_ENOUGH_SCORE作為與"閉"互動時分數不足輸出提示的變數
* ENOUGH_SCORE為提示玩家分數足夠開"閉"的變數
* globe_map定義完整地圖
* background_area定義玩家實際看到的視野大小
* background_position定義視角坐落於完整地圖的位置
* 玩家初始位置置中視野範圍中間
* Move_max使玩家將要超出視野時一並移動background_position
* update定義畫面輸出
* player_forward_block_check定義玩家移動方向是否為可互動方塊
* player_move定義玩家與視野(Move_max)移動邏輯
* player_event接收移動鍵並呼叫player_forward_block_check或player_move，並定義互動方塊的影響
* 主迴圈接收方向鍵並呼叫player_event、更新畫面

[程式GIF](https://github.com/James583476/Program/blob/main/Python/image/gif_4.gif)

---

**高二上自主學習_Flappy Bird**

* 類別Bird定義角色屬性與照片節錄位置
* 類別BackGround定義背景屬性、照片位置及位移邏輯->為了連續輸出背景一次兩張同時運作顯示
* 類別Ground同BackGround
* 類別Tube定義水管屬性、照片位置以及照片裁剪方式
* move定義水管移動邏輯與消失時機
* Menu_main定義執行至按下跳躍鍵前的非遊戲畫面
* main定義遊戲主迴圈
* Player_data_write紀錄遊玩分數至"Player_data.txt"

[程式GIF](https://github.com/James583476/Program/blob/main/Python/image/gif_5.gif)
