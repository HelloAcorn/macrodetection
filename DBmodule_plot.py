import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets
from torch.utils.data import TensorDataset, DataLoader, random_split, Dataset
from torch import optim
import torch.backends.cudnn as cudnn
from torch.utils.tensorboard import SummaryWriter


import random
import time
import os
import cx_Oracle
import numpy as np
import math
import matplotlib.pyplot as plt



torch.manual_seed(777)
random.seed(777)
np.random.seed(777)



############################DB PART##############################
    
LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
db = cx_Oracle.connect('c##mapledata', 'next0507', dsn)
cursor = db.cursor()



    


def Return_key(dbname,block): # 한 블록에 들어간 key값만 리턴
    cursor.execute("select trim(key) from %s where block = '%d'" %(dbname,block))
    data = cursor.fetchall()
    arr = []
    for i in range(len(data)):
        arr.append(data[i][0])
    return arr

def Return_Kill_Monster(dbname,block): # 한 블록에서 처치한 몬스터 마리수 리턴
    cursor.execute("select MAX(monster) , MIN(monster) from %s where block = '%d'" %(dbname,block))
    data = cursor.fetchall()
    max_num = data[0][0];
    min_num = data[0][1];
    return max_num - min_num


def Used_Kind_Of_Key(dbname,block):  # 한 블록에서 사용된 키 리턴(중복제거)
    cursor.execute("select distinct(key) from %s where block = '%d'" %(dbname,block))
    data = cursor.fetchall()
    
    arr = []
    for i in range(len(data)):
        arr.append(data[i][0])
    
    return arr
    
def Character_point(dbname,block):  # 블록의 첫 데이터에서의 캐릭터 위치.
    cursor.execute("select char_x, char_y from %s where ROWNUM = 1 and block = '%d'" %(dbname,block))
    data = cursor.fetchall()
    try:
        return data[0][0] , data[0][1]
    except IndexError:
        return "Character_point error"


def Key_Per_Minute(dbname, blockname): #kpm처럼 키 누른 횟수 per minute 값 가져오기.
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])
    
    cursor.execute("select trim(key) from %s" % (dbname))
    data = cursor.fetchall()
    key = []
    for i in range(len(data)):
        key.append(data[i][0])
        
    data = np.array(key)
    skillname, counts = np.unique(data, return_counts = True)  # 스킬 이름, kpm
    counts = counts / blocks * 2 


    uniq_cnt_dict = dict(zip(skillname, counts))
    print(uniq_cnt_dict)
    return counts



def Vectors_Per_Minute(dbname, blockname):
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])
    
    cursor.execute("select char_x, char_y from %s" % (dbname))
    data = cursor.fetchall()
    data = np.reshape(data,(len(data),2))

    distance = np.array([])
    for i in range(len(data)-1):
        a = data[i][0] - data[i+1][0]
        b = data[i][1] - data[i+1][1]
        distance = np.append(distance, math.sqrt((a * a) + (b * b)))


    print(np.sum(distance)/ blocks * 2) #움직인 값 per minute
    print(np.cov(distance))
    print(np.std(distance)) #표준편차
    
    
    
    

def key_STD(): #키 값들의 표준편차
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])
    
    cursor.execute("select trim(key) from %s" % (dbname))
    data = cursor.fetchall()
    key = []
    for i in range(len(data)):
        key.append(data[i][0])
        
    data = np.array(key)
    skillname, counts = np.unique(data, return_counts = True)  # 스킬 이름, kpm
    uniq_cnt_dict = dict(zip(skillname, counts))

    pass



key_name = ['buchaechain', 'chasingghost', 'clonesage', 'comflagrationchain', 'crestofthesollar', 'down',
 'earthchain', 'energyillusion', 'extremeclone', 'flyingfan', 'flyingnimbus',
 'goldcudgel','grandisgoddess', 'jump', 'left', 'phantasmalclone', 'rainbowbutterfiles',
 'readytodie', 'right', 'rockchain','ropeconnect', 'spacedistortion', 'spyderinmirror',
 'strangegods', 'summontiger', 'taeuldivine', 'up']

def KPMData(dbname, blockname):
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])

    max_data = []
    
    for i in range(blocks):
        cursor.execute("select trim(key) from %s where block = '%d'" % (dbname, i))
        data = cursor.fetchall()
        if len(data) == 0:
            continue
        
        skillname, counts = np.unique(data, return_counts = True)  # 스킬 이름, kpm
        counts = counts
        temp_index = 0
        
        temp_data =[0.0 for i in range(len(key_name))]

        for i in range(len(key_name)):
            if temp_index >= len(skillname):
                break
            if skillname[temp_index] == key_name[i]:
                temp_data[i] = counts[temp_index]
                temp_index = temp_index +1

        max_data.append(temp_data)
    max_data = np.array(max_data)
    max_data = np.reshape(max_data, (len(max_data),len(key_name)))
    
    return max_data

    
  
def MoveData(dbname, blockname):
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])

    mean_stdarr = []
    for a in range(blocks):
        cursor.execute("select trim(char_x), trim(char_y) from %s where block = '%d'" % (dbname, a))
        data = cursor.fetchall()
        data = np.array(data, dtype=int)
        if len(data) == 0:
            continue
        distance_arr = []
        for b in range(len(data)-1):  
            x_dit = data[b,0] - data[b+1,0]
            y_dit = data[b,1] - data[b+1,1]
            distance_arr.append(math.sqrt((x_dit * x_dit) + (y_dit * y_dit)))
        distance_arr = np.array(distance_arr)
        mean_stdarr.append(np.mean(distance_arr))
        mean_stdarr.append(np.std(distance_arr))

    mean_stdarr = np.array(mean_stdarr)
    mean_stdarr = np.reshape(mean_stdarr, (int(len(mean_stdarr)/2), 2))

    return mean_stdarr
    



def MonsterData(dbname, blockname):
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])

    #전체 정보
    monster_arr = []
    temp = []
    #블록정보
    
    for i in range(1):
        cursor.execute("select trim(MONSTER) from %s where block = '%d'" % (dbname, 23))
        data = cursor.fetchall()
        data = np.array(data, dtype=int)
        if len(data) == 0:
            continue
        monsterblock_arr = []
        data = data - data[np.argmin(data)]
        temp = np.squeeze(data)
        div_quadrature = math.sqrt(np.sum(data) * 30 / len(data))
        
        monsterblock_arr.append(data[np.argmax(data)][0])           #높이
        monsterblock_arr.append(div_quadrature)                     #넓이
        monster_arr.append(monsterblock_arr)

    monster_arr = np.array(monster_arr)

    x = range(len(temp))
    print(temp)
    print(x)
    plt.xlabel('action')
    plt.ylabel('kill_monsters')
    plt.title("macro sililar user")
    plt.bar(x, temp, width=1, color="purple")
    plt.show()
    return monster_arr

    
def TimeData(dbname, blockname):
    cursor.execute("select trim(count) from %s" % (blockname))
    blocks = cursor.fetchall()
    blocks = int(blocks[0][0])



def gather_data(dbname, blockname, amplification, label):
    kpm = KPMData(dbname, blockname)
    move = MoveData(dbname, blockname)
    monster = MonsterData(dbname, blockname)
    
    copy_move = np.copy(move)
    for i in range(amplification-1):
        move = np.concatenate((move, copy_move), axis=1)

    copy_monster = np.copy(monster)
    for i in range(amplification-1):
        monster = np.concatenate((monster, copy_monster), axis=1)
        
    X_Data = np.concatenate((kpm, move, monster), axis=1)
    y, _ = np.shape(X_Data)

    #X_Data = kpm
    Y_Data = np.array([[label] for i in range(y)])

    
    return X_Data, Y_Data
    


####################데이터셋 구성######################
class CustomDataset(Dataset): 
  def __init__(self, x_data, y_data):
    self.x_data = x_data
    self.y_data = y_data

  # 총 데이터의 개수를 리턴
  def __len__(self): 
    return len(self.x_data)

  # 인덱스를 입력받아 그에 맵핑되는 입출력 데이터를 파이토치의 Tensor 형태로 리턴
  def __getitem__(self, idx): 
    x = torch.FloatTensor(self.x_data[idx])
    y = torch.FloatTensor(self.y_data[idx])
    return x, y



class CustomModel(nn.Module):
    def __init__(self, input_node):
        super(CustomModel, self).__init__()
        self.input_layer = nn.Linear(input_node, 128) # 입력계층 input_node
        self.hidden_layer = nn.Linear(128,32)    # 은닉계층 512, 은닉2계층 128
        self.output_layer = nn.Linear(32,3)    # 은닉3계층 32, 출력계층 10
        self.dropout = nn.Dropout(0.25)
        
    def forward(self, x):
        x = self.input_layer(x)       # 입력계층 -> 은닉1계층
        x = F.relu(x)
        x = self.dropout(x)
        x = self.hidden_layer(x)       # 은닉1계층 -> 은닉2계층
        x = F.relu(x)
        x = self.dropout(x)
        output = self.output_layer(x) # 은닉3계층 -> 출력계층
        return output


SEEDS = 100
copynode = 1
n_epochs = 500


MonsterData('yoonhong', 'good_keyblock')


'''
macro_x, macro_y  = gather_data('east_wall', 'key_block', copynode, 0)
macrohuman_x, macrohuman_y = gather_data('yoonhong', 'bad_keyblock', copynode, 1)
human_x, human_y = gather_data('real_yoonhong', 'good_keyblock', copynode, 2)



dataset_x = np.concatenate((macro_x, macrohuman_x, human_x), axis=0)
_, input_layer = np.shape(dataset_x)
dataset_y = np.concatenate((macro_y, macrohuman_y, human_y), axis=0)


dataset = CustomDataset(dataset_x, dataset_y)


dataset_size = len(dataset)
train_size = int(dataset_size * 0.8)
test_size = dataset_size - train_size 

train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, drop_last=True)
test_loader = DataLoader(test_dataset, batch_size=5, shuffle=True, drop_last=True)    




device = "cuda" if torch.cuda.is_available() else "cpu"


writer = SummaryWriter("C:\\mycareer\\event_data")

np.random.seed(SEEDS)
torch.manual_seed(SEEDS)
random.seed(SEEDS)
model = CustomModel(input_layer).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0008)
    
for epoch in range(n_epochs):
    avg_loss = 0
    total_batch = len(train_loader)  # 에포크의 총 미니 배치 수
            

    # 데이터로더에서 미니배치를 하나씩 꺼내 학습을 수행
    for data, targets in train_loader:
        optimizer.zero_grad()         # 경사를 0으로 초기화                         


    prediction = model(data)
    targets = targets.squeeze(dim=-1)
    targets = torch.tensor(targets, dtype=torch.long, device=device)
    # 예측과 라벨 간의 오차 계산
    loss = loss_fn(prediction, targets)
    loss.backward()       # 오차를 역전파 계산
    optimizer.step()
    avg_loss += loss / total_batch      # 역전파 계산한 값으로 가중치를 수정
    writer.add_scalar("Loss/epoch", loss, epoch)
        
    if epoch % (n_epochs/50) == 0:
        model.eval()          # 신경망을 평가 모드로 전환
        correct = 0                 # 올바른 예측(정답) 누적 값
        with torch.no_grad():        # 평가 과정에는 미분이 필요없음
            for data, targets in test_loader:
                prediction = model(data)        # 모델 예측, (64,10) shape
                output, predicted = torch.max(prediction, 1) # torch.max()는 최대값(확률)과 인덱스(숫자)를 리턴
                targets = targets.squeeze(dim=-1)
                targets = torch.tensor(targets, dtype=torch.long, device=device)
                # predicted, targets의 두 1차원 배열을 비교한 결과의 부울 배열의 원소 값을 더함
                correct += predicted.eq(targets).sum()       # 정답과 일치한 경우 정답 카운트를 증가

            # 정확도 출력
            data_num = len(test_loader.dataset)       # 데이터 총 건수
            predict_percent = 100. * correct /data_num
            writer.add_scalar("accuracy/epoch", predict_percent, epoch)


print("epoch = {}, copynode = {}".format(n_epochs, copynode))
writer.flush()
writer.close()

'''


