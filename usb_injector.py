import pcbnew

def inject_usb_c():
    # Récupérer le design en cours
    board = pcbnew.GetBoard()
    
    # Création du composant "GHOST" (pas besoin de librairie sur disque)
    footprint = pcbnew.FOOTPRINT(board)
    footprint.SetReference("USB_AI_GHOST")
    footprint.SetValue("USB-C-16P")
    
    # --- DÉFINITION DES PADS (Version ultra-stable KiCad 6) ---
    # Format : (Nom du Pad, X, Y, Largeur, Hauteur)
    # Les coordonnées sont en mm, converties pour le moteur interne
    pads_to_create = [
        ("A1", -3.2, -4.0, 0.6, 1.5), ("A4", -2.4, -4.0, 0.6, 1.5),
        ("B12", 3.2, -4.0, 0.6, 1.5), ("B9", 2.4, -4.0, 0.6, 1.5),
        ("A5", -1.25, -4.0, 0.3, 1.5), ("B8", 1.25, -4.0, 0.3, 1.5),
        ("A6", -0.25, -4.0, 0.3, 1.5), ("A7", 0.25, -4.0, 0.3, 1.5)
    ]

    for name, x, y, w, h in pads_to_create:
        pad = pcbnew.PAD(footprint)
        pad.SetNumber(name)
        
        # LA MAGIE DU wxPoint : Stable sur Raspberry Pi
        pad.SetPosition(pcbnew.wxPoint(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        pad.SetSize(pcbnew.wxSize(pcbnew.FromMM(w), pcbnew.FromMM(h)))
        
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        pad.SetLayerSet(pcbnew.LSET(pcbnew.F_Cu))
        footprint.Add(pad)

    # Positionner le connecteur au milieu de ta zone de travail (100mm, 100mm)
    footprint.SetPosition(pcbnew.wxPoint(pcbnew.FromMM(100), pcbnew.FromMM(100)))
    
    # Injection finale dans le cuivre
    board.Add(footprint)
    pcbnew.Refresh()
    
    print("✅ [PCBAI] : Connecteur USB-C injecté avec succès via le Cloud.")

if __name__ == "__main__":
    inject_usb_c()
