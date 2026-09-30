import random
import msvcrt

player_score = 0
NOT_ENOUGH_SCORE = 0
ENOUGH_SCORE = 0
D2_OPEN_SCORE = 7
#(y,x)#
W = "牆"
a = "囗"
D0 = "關"
D1 = "開"
D2 = "閉"
Bx = "箱"
nn = "空"   #互動完畢方塊的位置
En = "終"
move_enable_blocks = [a,D1,nn,En]
interact_blocks = [D0,D2,Bx]
globe_map =  [[ W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [ W, a, a,Bx, W, a, a, a, a, a, a, a, a, a, W, a, a, a, a, a, a, a, a,Bx, W],
        [ W, a, a, a, W, a, a, W,D0, W, a, a, a, a, W, a, a, a, a, W, W, W,D0, W, W],
        [ W, a, a, a, W, a, a, W, a, W, W, W, W, W, W, a, W, W, W, W, a, a, a, a, W],
        [ W, a, a, a, W, a, a, W, a, a, a, a, a, W, a, a, W, a,Bx, W, a, W, W, a, W],
        [ W,D0, W, W, W, W, a, W, a, a, W, a, a, W, a, W, W, a, a, W, a, W, W, a, W],
        [ W, a, W, a,Bx, W, a, W, a, W, W, W, a,D0, a, W, W, a, a, W, a, W, W, a, W],
        [ W, a, W, a, a, W, a, W, a, a, W, a, a, W, W, W, W, a, a, W, a, a, a, a, W],
        [ W, a,D0, a, a, W, a, W, a, a, a, a, a, W, a, a, a, a, a, W, a, W, W, a, W],
        [ W, a, W, W, W, W, a, W, W, W,D0, W, W, W, a, W, W, a, a, W, a, W, W, a, W],
        [ W, a, a, a, a, a, a, W, a, a, a, a, a, a, a, W, W, a, a,D0, a, W, W, a, W],
        [ W, a, a, a, a, a, a,D0, a, a, a, a, a, a, a, W, W, W, W, W,D0, W, W, W, W],
        [ W, W, W, W,D0, W, W, W, a, W, W, W, W,Bx, nn, W, a, a, a, a, a, W, a,Bx, W],
        [ W, a, a, a, a, a, a, W, a, W, W, W, W, W, W, W, a, a, W, W, a, W, a, a, W],
        [ W, W, W, a, W, W, a, W, a, a, a, a, a, a, a,D0, a, a, W, W, a,D0, a, a, W],
        [ W, W, W, a, W, W, a, W, W, W, W, W, W, W, W, W, a, a, a, a, nn, W, a, a, W],
        [ W, a, a, a, a, a, a, W, a, W, a, a, nn, W, W, W, W, W, W, W, W, W, W, W, W],
        [ W, a, a, a, a, a, a,D0, a, W, a, W, W, W, a, a, a, a, a, a, W, a, a, a, W],
        [ W, W, W, a, W, W, a, W, a, W, a, W,Bx, W, a, a, W, W, W, a, a, a, a, a, W],
        [ W, W, W, a, W, W, a, W, a, W, a, W,D0, W, W, a, a, a, a, a, W,D2,D2,D2, W],
        [ W, a, a, a, a, a, a, W, a, a, a, a, a, a, W, a, W, W, W,D0, W, a, a, a, W],
        [ W, a, a, a, W, W, a, W, W, W, W, W, W, a, a, a, a, W, a, a, W, a, a, a, W],
        [ W, W, W, a, W, W, a,D0, a, a, a, a, W, W, W, W, W, W,Bx, a, W, a, En, a, W],
        [ W,Bx, a, a, W, W, a, W, a, a, a, a, a, a, a, a, nn, W,Bx, a, W, a, a, a, W],
        [ W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]]
background_area = [4,4]
background_position = [0,0]
#background_position = [0,17]#
player_init_y,player_init_x = [int(background_area[0]/2) if background_area[0]%2 == 1 else int((background_area[0]-1)/2),
                int(background_area[1]/2) if background_area[1]%2 == 1 else int((background_area[1]-1)/2)]
PLAYER_POSITION = [player_init_y,player_init_x]
Move_max = [background_area[0]//2-1,background_area[1]//2-1]

def update(player_score,score,NOT_ENOUGH_SCORE,ENOUGH_SCORE):
  background_area[0] += score
  background_area[1] += score
  max_pos_y = len(globe_map)-1
  max_pos_x = len(globe_map[0])-1
  print("\b"*background_area[0]*background_area[1],"\b"*background_area[0],"\b\b\b"*500,'\nscore:',player_score,sep="",end='\n\n')
  for y in range(background_area[0]):
    for x in range(background_area[1]):
      if [y,x] == PLAYER_POSITION:
        print("囚",end="")
      else:
        chy = y+background_position[0]
        chx = x+background_position[1]
        if chy <= max_pos_y and chx <= max_pos_x and chy >= 0 and chx >= 0:
          print(globe_map[y+background_position[0]][x+background_position[1]],end="")
        else:
          print('　',end='')
    print()
  if NOT_ENOUGH_SCORE:
    print('門鎖住了，分數好像不夠...')
    NOT_ENOUGH_SCORE = 0
  if ENOUGH_SCORE:
    print('好像有什麼解鎖了...')
  return NOT_ENOUGH_SCORE

def player_forward_block_check(key):
  interaction_enable = 0
  back_block = None
  if key == "w":
    block = globe_map[background_position[0]+PLAYER_POSITION[0]-1][background_position[1]+PLAYER_POSITION[1]]
    face_block_pos = [-1,0]
  elif key == "a":
    block = globe_map[background_position[0]+PLAYER_POSITION[0]][background_position[1]+PLAYER_POSITION[1]-1]
    face_block_pos = [0,-1]
  elif key == "s":
    block = globe_map[background_position[0]+PLAYER_POSITION[0]+1][background_position[1]+PLAYER_POSITION[1]]
    face_block_pos = [1,0]
  elif key == "d":
    block = globe_map[background_position[0]+PLAYER_POSITION[0]][background_position[1]+PLAYER_POSITION[1]+1]
    face_block_pos = [0,1]
  for move_enable_block in move_enable_blocks:
    if block == move_enable_block:
      back_block = block
  for interact_block in interact_blocks:
    if block == interact_block:
      back_block = block
      interaction_enable = 1
  return face_block_pos,back_block,interaction_enable

def player_move(key,face_block_pos):
  if key == "w" or key == "a":
    if PLAYER_POSITION[0] + face_block_pos[0] == Move_max[0] + face_block_pos[0]:
      background_position[0] += face_block_pos[0]
    else: PLAYER_POSITION[0] += face_block_pos[0]
    if PLAYER_POSITION[1] + face_block_pos[1] == Move_max[1] + face_block_pos[1]:
      background_position[1] += face_block_pos[1]
    else: PLAYER_POSITION[1] += face_block_pos[1]
  else:
    if PLAYER_POSITION[0] + face_block_pos[0] == background_area[0]-Move_max[0]:
      background_position[0] += face_block_pos[0]
    else: PLAYER_POSITION[0] += face_block_pos[0]
    if PLAYER_POSITION[1] + face_block_pos[1] == background_area[1]-Move_max[1]:
      background_position[1] += face_block_pos[1]
    else: PLAYER_POSITION[1] += face_block_pos[1]

def player_event(key,player_score,NOT_ENOUGH_SCORE,ENOUGH_SCORE):
  face_block = None
  score = 0
  if key == "w" or key == "a" or key == "s" or key == "d":
    face_block_pos,face_block,interaction_enable = player_forward_block_check(key)
  elif key == "q":
    return 0,0,NOT_ENOUGH_SCORE,ENOUGH_SCORE
  else: return 1,0,NOT_ENOUGH_SCORE,ENOUGH_SCORE
  if face_block == En: return 0,score,NOT_ENOUGH_SCORE,ENOUGH_SCORE
  if face_block != None:
    if interaction_enable:
      if face_block == D0:
        globe_map[background_position[0]+PLAYER_POSITION[0]+face_block_pos[0]][background_position[1]+PLAYER_POSITION[1]+face_block_pos[1]] = D1
      if face_block == D2 and player_score >= D2_OPEN_SCORE:
        globe_map[background_position[0]+PLAYER_POSITION[0]+face_block_pos[0]][background_position[1]+PLAYER_POSITION[1]+face_block_pos[1]] = nn
      elif face_block == D2 and player_score < D2_OPEN_SCORE:
        NOT_ENOUGH_SCORE = 1
      if face_block == Bx:
        globe_map[background_position[0]+PLAYER_POSITION[0]+face_block_pos[0]][background_position[1]+PLAYER_POSITION[1]+face_block_pos[1]] = nn
        score += 1
    else:
      player_move(key,face_block_pos)
  if score >= D2_OPEN_SCORE and ENOUGH_SCORE == 0:
    ENOUGH_SCORE = 1
  return 1,score,NOT_ENOUGH_SCORE,ENOUGH_SCORE

if __name__ == "__main__":
  run = 1
  NOT_ENOUGH_SCORE = update(0,0,NOT_ENOUGH_SCORE,ENOUGH_SCORE)
  while run:
    run,score,NOT_ENOUGH_SCORE,ENOUGH_SCORE = player_event(msvcrt.getch().decode(),player_score,NOT_ENOUGH_SCORE,ENOUGH_SCORE)
    player_score += score
    NOT_ENOUGH_SCORE = update(player_score,score,NOT_ENOUGH_SCORE,ENOUGH_SCORE)
  print("\n終了！")
