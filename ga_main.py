from genAlg import geneticAlg


def ga_main():
    ga_player = geneticAlg(100, .2)

    # timelimit in ??
    ga_player.runAlgTime(60)
    ga_player.graph.show_plot()
    



if __name__ == "__main__":
    ga_main()