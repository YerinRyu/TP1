import torch
from torch import nn
from joblib import load
import numpy as np
import pandas as pd
import os

def get_path():
    path = os.getcwd()
    
    return path

class Model(nn.Module):
    def __init__(self, input_cnt, set_hidden, output_cnt):# dropout_p 추가, dropout_p # input_cnt = 입력층, set_hidden = 은닉층, output_cnt = 출력층
        super(Model, self).__init__()
        self.layers = nn.ModuleList() # 파이토치의 ModuleList 상속받아 파라미터 인식

        # 입력층 - 은닉층과의 연결, 은닉층끼리의 연결을 nn.Linear(fully-connected)를 통해 설정한 set_hidden 뉴런수를 따라 연결
        last_cnt = input_cnt
        for hidden_cnt in set_hidden:
            self.layers.append(nn.Linear(last_cnt, hidden_cnt))
            self.layers.append(nn.BatchNorm1d(hidden_cnt)) # 배치 정규화 추가 
            # self.layers.append(nn.Dropout(p=dropout_p))# 드롭아웃 추가해봤지만 성능이 더 나빠짐  (추가하려면 주석제거)
            self.layers.append(nn.ReLU())
            last_cnt = hidden_cnt
        
        # 은닉층과 출력층과의 연결   
        self.layers.append(nn.Linear(last_cnt, output_cnt))

    # 모델에 입력된 input값이 각 층을 통과하며 최종적으로 출력되는 함수 지정
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

def arrange_input(input):
    input_cnt, output_cnt = 10, 1
    data = np.zeros([1, input_cnt])
    
    # 전복의 성별 원핫인코딩 적용
    if input[0] == 'M': 
        data[0, 0] = 1
    if input[0] == 'F':
        data[0, 1] = 1
    if input[0] == 'I': 
        data[0, 2] = 1
    data[0, 3:] = input[1:]
    
    return torch.Tensor(data), input_cnt, output_cnt

def load_predict(input):
    
    path = get_path()
    
    arranged_input, input_cnt, output_cnt = arrange_input(input)
    arranged_input = arranged_input.to('cpu')

    model = Model(input_cnt = input_cnt, set_hidden = (256, 128, 64), output_cnt = output_cnt)
    model.load_state_dict(torch.load(path+'/model/regression/regreesion_model.pt'))
    model.eval()

    output = model(arranged_input)
    return output.item()

def load_predict_csv(csv_file):
    
    path = get_path()
    
    df = pd.read_csv(csv_file)
    
    outputs = []
    for i, row in df.iterrows():
        input_data = row.tolist()
        arranged_input, input_cnt, output_cnt = arrange_input(input_data)
        arranged_input = arranged_input.to('cpu')

        model = Model(input_cnt = input_cnt, set_hidden = (256, 128, 64), output_cnt = output_cnt)
        model.load_state_dict(torch.load(path+'/model/regression/regreesion_model.pt'))
        model.eval()

        output = model(arranged_input)
        outputs.append(output.item())
        
    return outputs

#예시
# input_data = ['M', 0.455, 0.365, 0.095, 0.514, 0.2245, 0.101, 0.15]
# output = load_predict(input_data)

# prediction = load_predict_csv('Regression_data_label_removed.csv')
