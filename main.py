from SnakeGame import Game
from agent import Agent
from helper import plot

if __name__ == '__main__':
    #epoch=int(input("enter amount of epoch's:"))
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    epoch=100
    agent=Agent()
    gm = Game()
    for i in range(epoch):
        score=gm.main(agent)

        # train long memory, plot result
        agent.n_games += 1
        agent.train_long_memory()

        if score > record:
            record = score
            agent.model.save()

        print('Game', agent.n_games, 'Score', score, 'Record:', record)

        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)

        gm.reset()
