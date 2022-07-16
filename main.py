#from SnakeGame import Game
from SnakeGame import Game,GameGridAsState
from agent import Agent,Agent_CNN
from helper import plot

##normal running
def DQN_run():
    LR = 0.0083  ##learning rate of the model
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    epoch = 200
    agent = Agent(LR, 30)
    gm = Game()
    for i in range(epoch):
        gm.main(agent)
        # train long memory, plot result
        agent.n_games += 1
        agent.train_long_memory()

        if gm.score > record:
            record = gm.score
            agent.model.save()

        print('Game', agent.n_games, 'Score', gm.score, 'Record:', record)

        plot_scores.append(gm.score)
        total_score += gm.score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)

        gm.reset()

##new running with cnn
def CNN_run():
    LR = 0.0083  ##learning rate of the model
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    epoch = 200
    agent = Agent_CNN(LR, 80)
    gm = GameGridAsState()
    for i in range(epoch):
        gm.main(agent)
        # train long memory, plot result
        agent.n_games += 1
        agent.train_long_memory()

        if gm.score > record:
            record = gm.score
            agent.model.save()

        print('Game', agent.n_games, 'Score', gm.score, 'Record:', record)

        plot_scores.append(gm.score)
        total_score += gm.score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)

        gm.reset()





if __name__ == '__main__':
    DQN_run()
    #CNN_run()




