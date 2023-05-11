def printheuristique():
    """
    fonction qui affiche le plateau de jeu avec l'heuristique"""
    for y in range(8,0,-1):
        y_init = y
        chaine = "  " * y
        x=0
        chaine += str(8+y_init)
        if 8+y_init == 9:   
                    chaine+= " "
        while y!=8:
            x+=1
            y+=1
            chaine+= "  " + str(8+y_init)
            if 8+y_init == 9:
                    chaine+= " "
        print(chaine)
    
    print("".join(["8"+"   " for i in range(0,9) ]))
    
    for x in range(1,9):
        x_init = x
        chaine = "  " * x
        y=0
        if 8-x_init == 0:
            chaine += ""
        chaine += str(8-x_init)

        while x!=8:
            x+=1
            y+=1
            chaine+= "   " + str(8-x_init)
        print(chaine)

if __name__ == "__main__":
    printheuristique()