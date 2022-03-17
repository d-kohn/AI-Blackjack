from genAlg import geneticAlg


def ga_main():
    ga_player = geneticAlg(100, .3)

    ga_player.runAlgTime(1200)
    ga_player.graph.show_plot()
    



if __name__ == "__main__":
    ga_main()