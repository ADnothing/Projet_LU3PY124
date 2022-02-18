from lib import *
from fonctions import *

if __name__ == "__main__":
    
    F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr, march, marcherr = get_datas()
    
    popt, pcov = curve_fit(loi, F, seuil_far)
    Y = loi(F, popt[0], popt[1])
    th = loi(F, 21e-3, 20e-6)

    plot_all(F, A1, A1err, A2, A2err, seuil_far, seuil_farerr, seuil_co, seuil_coerr,march, marcherr, Y, th)

    print("sigma = {:.3} (+/-) {:.3}".format(popt[0], np.sqrt(pcov[0][0])))
    print("v = {:.3} (+/-) {:.3}".format(popt[1], np.sqrt(pcov[1][1])))
    print("erreur relative sigma : {:.4} %".format((popt[0]-21e-3)*100/21e-3))
    print("erreur relative v : {:.3} %".format(-(popt[1]-20e-6)*100/20e-6))