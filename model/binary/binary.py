import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from sklearn.preprocessing import StandardScaler
import joblib

def get_path():
    path = os.getcwd()
    
    return path

class MDNNModel(nn.Module):
    def __init__(self, input_size, num_classes, num_domains):
        super(MDNNModel, self).__init__()
        self.num_domains = num_domains
        self.shared_fc1 = nn.Linear(input_size, 128)
        self.shared_fc2 = nn.Linear(128, 64)
        self.shared_fc3 = nn.Linear(64, 32)
        self.shared_fc4 = nn.Linear(32, num_classes)
        self.domain_fc1 = nn.ModuleList([nn.Linear(input_size, 128) for _ in range(num_domains)])
        self.domain_fc2 = nn.ModuleList([nn.Linear(128, 64) for _ in range(num_domains)])
        self.domain_fc3 = nn.ModuleList([nn.Linear(64, 32) for _ in range(num_domains)])
        self.domain_fc4 = nn.ModuleList([nn.Linear(32, num_classes) for _ in range(num_domains)])

    def forward(self, x, domain_idx):
        if domain_idx is None:
            x = F.relu(self.shared_fc1(x))
            x = F.relu(self.shared_fc2(x))
            x = F.relu(self.shared_fc3(x))
            x = self.shared_fc4(x)
            return x
        else:
            x = F.relu(self.domain_fc1[domain_idx](x))
            x = F.relu(self.domain_fc2[domain_idx](x))
            x = F.relu(self.domain_fc3[domain_idx](x))
            x = self.domain_fc4[domain_idx](x)
            return x
        
def scaler(data):
    path = get_path()
    
    scaler_obj = joblib.load(path+'/model/binary/MDNN_binary_Scaler.joblib') 
    scaled_data = scaled_data = scaler_obj.transform([data])
    
    return scaled_data

def load_model_and_predict(input_data):
    path = get_path()
    
    input_data = torch.tensor(input_data, dtype=torch.float32)
    model = MDNNModel(input_size=8, num_classes=2, num_domains=2)
    model.load_state_dict(torch.load(path+'/model/binary/binary.pt')) # 저장된 모델 위치
    model.eval()

    with torch.no_grad():
        output = model(input_data, domain_idx=1)
        _, predicted = torch.max(output.data, 1)

    return predicted.item()


