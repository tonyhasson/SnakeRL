import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model_saver.pth'):
        model_folder_path = 'model_saver'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)
        target = pred.clone()

        ##iterate over game rewards
        for i in range(len(done)):

            ##get reward for game idx
            Q_new = reward[i]

            ##if didn't lose the round
            if not done[i]:
                Q_new += self.gamma * torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = Q_new


        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

class convnet1(nn.Module):
    def __init__(self):
        super(convnet1, self).__init__()

        # Constraints for layer 1
        # self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2)
        # self.batch1 = nn.BatchNorm2d(16)
        # self.relu1 = nn.ReLU()
        # self.pool1 = nn.MaxPool2d(kernel_size=2)  # default stride is equivalent to the kernel_size
        #
        # # Constraints for layer 2
        # self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2)
        # self.batch2 = nn.BatchNorm2d(32)
        # self.relu2 = nn.ReLU()
        # self.pool2 = nn.MaxPool2d(kernel_size=2)
        #
        # # Defining the Linear layer
        # self.fc = nn.Linear(32 * 7 * 7, 10)

        # Constraints for layer 1
        self.conv1_1=nn.Conv2d(3,10,kernel_size=(5,5),padding=2)
        self.conv1_2 = nn.Conv2d(10, 20, kernel_size=(3, 3), padding=1)
        self.pool1=nn.MaxPool2d(kernel_size=2,stride=2)

        # Constraints for layer 2
        self.conv2_1 = nn.Conv2d(20, 20, kernel_size=(5, 5), padding=2)
        self.conv2_2 = nn.Conv2d(20, 10, kernel_size=(5, 5), padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Defining the Linear layer
        self.fc1 = nn.Linear(10 * 4 * 4, 255)
        self.fc2 = nn.Linear(255, 3)


        #activation function
        self.relu = nn.ReLU()

    # defining the network flow
    def forward(self, x):
        ##Layer 1:
        x=self.relu(self.conv1_1(x))
        x=self.relu(self.conv1_2(x))
        x=self.pool1(x)

        ##Layer 2:
        x = self.relu(self.conv2_1(x))
        x = self.relu(self.conv2_2(x))
        x = self.pool2(x)

        ##FC
        x = x.view(-1, 4 * 4 * 10)  # flattening
        x=self.relu(self.fc1(x))
        x=self.fc2(x)

        return x

    def save(self, file_name='model_saver_CNN.pth'):
        model_folder_path = 'model_saver'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer_CNN:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 3:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)
        target = pred.clone()

        ##iterate over game rewards
        for i in range(len(done)):



            ##get reward for game idx
            Q_new = reward[i]

            ##if didn't lose the round
            if not done[i]:
                Q_new += self.gamma * torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = Q_new


        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

