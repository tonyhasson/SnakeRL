from SnakeGame import Game
from agent import Agent




if __name__ == '__main__':

    epoch=10
    stat_list=[]
    lst_lr_options=[0.0077,0.0080,0.0083]
    for option in lst_lr_options:
        print("Now Running option: ",option)
        lst_avg_score_below_50=[]
        lst_timeouts=[]
        lst_avg_score_total=[]

        for t in range(epoch):
            agent = Agent(option)
            gm = Game()
            print("Round number: ",t)
            avg_score_below_50 = 0
            timeouts = 0
            avg_score_total = 0

            for i in range(200):
                gm.main(agent)
                # train long memory, plot result
                agent.n_games += 1
                agent.train_long_memory()

                if agent.n_games%25==0:
                    print("Game number: ", agent.n_games)

                if agent.n_games<=50:
                    avg_score_below_50+=gm.score

                avg_score_total+=gm.score
                timeouts+=gm.timeout_counter



                gm.reset()

            lst_avg_score_below_50.append(avg_score_below_50/50)
            lst_timeouts.append(timeouts)
            lst_avg_score_total.append(avg_score_total/200)

        stat_list.append({"LR":option,"average score below game 50":sum(lst_avg_score_below_50)/epoch,"average score total":sum(lst_avg_score_total)/epoch,"average timeouts":sum(lst_timeouts)/epoch})

    print("\n\n")
    print(*stat_list, sep = "\n")


