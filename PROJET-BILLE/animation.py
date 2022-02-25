from library import *
from plateau import Plateau
from bille import Bille

#On définit la fennêtre graphique
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
#Ici on définit les éléments qui seront animés
#line : la ligne du plateau
#dot : la bille
line, = ax.plot([], [], lw=2)
dot, = ax.plot([], [], ls="none", marker="o")

#fonction d'initialisation des paramètres
def init():
    line.set_data([], [])
    dot.set_data([], [])
    return dot, line

#fonction d'animation, actualise les trajectoires du paramètres i
def animate(i):
    x = np.linspace(0, 2, 1000)
    x2 = 1
    y = Plateau.z
    y2 = Bille.z
    line.set_data(x, y)
    dot.set_data(x2, y2)
    return dot,line

#Création de l'animation et sauvegarde
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

anim.save('basic_animation.gif', fps=30)
