from lib import *

#Calibration des mesures
#Donne l'accélération du plateau à partir 
#de l'intensité du courrant électrique de l'accéléromètre
def convert(A):
    return (A*2*9.81)/380

#récupère les donnés du diagramme des phases depuis le csv "DATA.csv"
def get_datas():
    
    datas = pd.read_csv('DATA.csv')
    
    #Fréquences
    F = datas['F'].values
    
    #Mesures instabilités de Faraday
    M1 = datas['M1'].values/2
    M1err = datas['M1err'].values 
    
    M2 = datas['M2'].values/2
    M2err = datas['M2err'].values
    
    #Seuil coalescence
    sc = datas['seuil_bas'].values/2
    scerr = datas['seuil_baserr'].values
    
    m = datas['marcheurs'].values/2
    merr = datas['marcheurserr'].values
    
    #Convertion (cf calibration)
    A1 = convert(M1)
    A1err = convert(M1err)
    
    A2 = convert(M2)
    A2err = convert(M2err)
    
    #Seuil de l'instabilité de Faraday en accélération
    seuil_far = (A1+A2)/2

    std_err = np.empty((1, A1.size))
    for i in range(A1.size):
        a = np.array([A1[i], A2[i]]).std()
        std_err[0][i] = a
    seuil_farerr = np.sqrt(((A1err+A2err)/2)**2 + std_err[0]**2)
    
    #Seuil de coalescence en accélération
    seuil_co = convert(sc)
    seuil_coerr = convert(scerr)
    
    march = convert(m)
    marcherr = convert(merr)
    
    return (F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr, march, marcherr)

#Loi théorique trouvé par analyse dimentionnelle du seuil de l'instabilité de
#faraday en fonction de la fréquence
def loi(f, sigma, v):
    return (2**(4/3))*((950/sigma)**(1/3))*v*(2*np.pi*f)**(5/3)

#Plot chaques étapes de la réalisation du diagramme des phases
def plot_all(F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr, march, marcherr, Y, th):
    
    #Plot des deux mesures de l'instabilité de faraday
    plt.errorbar(F, A1, fmt='-o', label='Mesure 1')
    plt.errorbar(F, A2, fmt='-o', label='Mesure 2')
    plt.fill_between(F, A1-A1err, A1+A1err, alpha=0.75)
    plt.fill_between(F, A2-A2err, A2+A2err, alpha=0.75)
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    #Plot comparatif de la moyenne des instabilités de faraday avec incertitudes
    plt.errorbar(F, A1, fmt='-o', label='Mesure 1')
    plt.errorbar(F, A2, fmt='-o', label='Mesure 2')
    plt.errorbar(F, seuil_far, fmt='-o', label="Seuil d'instabilité")
    plt.fill_between(F, A1-A1err, A1+A1err, alpha=0.75)
    plt.fill_between(F, A2-A2err, A2+A2err, alpha=0.75)
    plt.fill_between(F, seuil_far-seuil_farerr, seuil_far+seuil_farerr, alpha=0.75)
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    #Plot fit de l'isntabilité de faraday
    plt.errorbar(F, seuil_far, fmt='-o', label="Seuil d'instabilité")
    plt.fill_between(F, seuil_far-seuil_farerr, seuil_far+seuil_farerr, alpha=0.75)
    plt.plot(F, Y, label='fit')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    #comparasion fit et théorique
    plt.plot(F, th, label='Modèle Théorique')
    plt.errorbar(F, seuil_far, fmt='-o', label="Seuil d'instabilité")
    plt.fill_between(F, seuil_far-seuil_farerr, seuil_far+seuil_farerr, color='orange', alpha=0.75)
    plt.plot(F, Y, label='fit')
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.xlabel("Fréquence (Hz)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    
    #Diagramme des phases avec régions colorés
    plt.errorbar(F, seuil_co, fmt='-o', color='black')
    plt.errorbar(F, seuil_far, fmt='-o', color='black')
    plt.errorbar(F, march, fmt='-o', color='black')
    
    plt.fill_between(F, seuil_far, march, color='springgreen')
    plt.fill_between(F[F<=45], seuil_far[F<=45], seuil_co[F<=45], color='gold')
    plt.fill_between(F[F>=45], march[F>=45], seuil_co[F>=45], color='gold')
    plt.fill_between(F, seuil_co, color='deepskyblue')
    plt.fill_between(F, seuil_far, np.max(seuil_far), color='lightcoral')
    
    plt.fill_between(F, seuil_co-seuil_coerr, seuil_co+seuil_coerr, alpha=0.75)
    plt.fill_between(F, seuil_far-seuil_farerr, seuil_far+seuil_farerr, alpha=0.75)
    plt.fill_between(F, march-marcherr, march+marcherr, alpha=0.75)
    
    plt.text(25,20,'Instabilité de Faraday')
    plt.text(60, 17.5,'Marcheurs')
    plt.text(50,1,'Coalescence')
    plt.text(45,8,'Rebonds')
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.xlabel("Fréquence (Hz)")
    plt.show()
    
    #Diagramme des phases avec régions colorés + fit
    plt.errorbar(F, seuil_co, fmt='-o', color='black')
    plt.errorbar(F, seuil_far, fmt='-o', color='black')
    plt.errorbar(F, march, fmt='-o', color='black')
    plt.plot(F, Y, ls='--', color='white', lw=3,label='fit del\'instabilité\nde faraday')
    
    plt.fill_between(F, seuil_far, march, color='springgreen')
    plt.fill_between(F[F<=45], seuil_far[F<=45], seuil_co[F<=45], color='gold')
    plt.fill_between(F[F>=45], march[F>=45], seuil_co[F>=45], color='gold')
    plt.fill_between(F, seuil_co, color='deepskyblue')
    plt.fill_between(F, seuil_far, np.max(seuil_far), color='lightcoral')
    
    plt.fill_between(F, seuil_co-seuil_coerr, seuil_co+seuil_coerr, alpha=0.75)
    plt.fill_between(F, seuil_far-seuil_farerr, seuil_far+seuil_farerr, alpha=0.75)
    plt.fill_between(F, march-marcherr, march+marcherr, alpha=0.75)
    
    plt.text(25,20,'Instabilité de Faraday')
    plt.text(60, 17.5,'Marcheurs')
    plt.text(50,1,'Coalescence')
    plt.text(45,8,'Rebonds')
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.xlabel("Fréquence (Hz)")
    plt.legend(bbox_to_anchor=(1.05, 0.75), loc='upper left', borderaxespad=0., facecolor='black', labelcolor='white')
    plt.show()
    
#Donne la taille moyenne des goutes avec incertitude
def taille_gouttes(file_npz):
        
    Rg = file_npz.f.arr_0
    Rg_err = file_npz.f.arr_1
        
    R = Rg.mean()
    a = Rg_err.mean()
    b = Rg.std()
    c = Rg_err.std()
    R_err = np.sqrt(a**2 + b**2 + c**2)
        
    print("La taille des petites gouttes est : {:.2} (+/-) {:.2}".format(R, R_err))