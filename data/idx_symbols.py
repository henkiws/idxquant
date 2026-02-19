import requests

def get_idx_symbols():

    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"

    # fallback manual large IDX list
    return [

        "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK",
        "TLKM.JK","ASII.JK","UNVR.JK","ICBP.JK",
        "INDF.JK","CPIN.JK","ANTM.JK","ADRO.JK",
        "ITMG.JK","MDKA.JK","SMGR.JK",

        "ACES.JK","AKRA.JK","AMRT.JK","ARTO.JK",
        "BBTN.JK","BDMN.JK","BRPT.JK","BUKA.JK",
        "ESSA.JK","EXCL.JK","GOTO.JK","HRUM.JK",
        "ICBP.JK","INCO.JK","INDY.JK","JPFA.JK",
        "KLBF.JK","MAPI.JK","MEDC.JK","PGAS.JK",
        "PTBA.JK","SIDO.JK","SMRA.JK","TINS.JK",
        "TKIM.JK","TOWR.JK","UNTR.JK","WSKT.JK"

    ]
