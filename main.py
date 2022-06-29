from SnakeGame import Game
from agent import Agent
from helper import plot


LR = 0.0083


if __name__ == '__main__':

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    epoch=200
    agent=Agent(LR)
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



