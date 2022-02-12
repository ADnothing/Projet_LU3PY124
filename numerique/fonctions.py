from lib import *

def convert(A):
    return (A*2*9.81)/380

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
    
    return (F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr)

def loi(f, sigma, v):
    return (2**(4/3))*((950/sigma)**(1/3))*v*(2*np.pi*f)**(5/3)

def plot_all(F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr, Y, th):
    
    plt.errorbar(F, A1, yerr=A1err, fmt='o', label='Mesure 1')
    plt.errorbar(F, A2, yerr=A2err, fmt='o', label='Mesure 2')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    plt.errorbar(F, A1, yerr=A1err, fmt='o', label='Mesure 1')
    plt.errorbar(F, A2, yerr=A2err, fmt='o', label='Mesure 2')
    plt.errorbar(F, seuil_far, yerr=seuil_farerr, fmt='o', label="Seuil d'instabilité")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    plt.errorbar(F, seuil_far, yerr=seuil_farerr, fmt='o', label="Seuil d'instabilité")
    plt.plot(F, Y, label='fit')
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    plt.plot(F, th, label='Modèle Théorique')
    plt.errorbar(F, seuil_far, yerr=seuil_farerr, fmt='o', label="Seuil d'instabilité")
    plt.plot(F, Y, label='fit')
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()
    
    plt.errorbar(F, seuil_co, yerr=seuil_coerr, fmt='o', label='Seuil de coalescence')
    plt.errorbar(F, seuil_far, yerr=seuil_farerr, fmt='o', label="Seuil d'instabilité")
    plt.ylabel("Accélération ($m.s^{2}$)")
    plt.legend(bbox_to_anchor=(1.1, 0.75), loc='upper left', borderaxespad=0.)
    plt.show()

