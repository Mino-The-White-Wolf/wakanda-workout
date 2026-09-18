import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Wakanda Workout"
    page.bgcolor = "#0a0a0c"
    page.scroll = "auto"
    page.window_width = 400

    # Données des séances avec détails techniques
    seances = {
        "A": [
            {"nom": "1. Pompes", "detail": "Mains largeur d'épaules. Descends en gardant les coudes le long du corps à 45° (en forme de flèche, pas en croix). Rentre le ventre, le corps est une planche droite."},
            {"nom": "2. Développé Militaire", "detail": "Pieds sur l'élastique. Poings au niveau des clavicules. Pousse vers le plafond. Rentre le ventre et contracte les fessiers pour ne pas creuser le bas du dos."},
            {"nom": "3. Écartés (Chest Fly)", "detail": "Élastique accroché à la porte, tourne-lui le dos. Bras légèrement fléchis, referme-les devant ton sternum comme si tu voulais enlacer un grand arbre. Ne tends pas les coudes."},
            {"nom": "4. Extensions Triceps", "detail": "Élastique à la porte, fais-lui face. Coudes fermement collés contre tes côtes. Seuls les avant-bras bougent pour tirer vers le bas."}
        ],
        "B": [
            {"nom": "1. Tirage Dos (Rowing)", "detail": "Assis, élastique derrière les pieds. Dos droit. Tire en ramenant les coudes le plus loin possible en arrière. Sors la poitrine et resserre tes omoplates (imagine écraser une noix entre elles)."},
            {"nom": "2. Band Pull-Apart", "detail": "Debout, bras tendus devant toi. Écarte les bras en croix pour déchirer l'élastique jusqu'à ce qu'il tape ta poitrine. Règle la difficulté en écartant plus ou moins les mains au départ."},
            {"nom": "3. Curl Biceps", "detail": "Debout sur l'élastique. Coudes plaqués contre les côtes, ils ne doivent ni avancer ni reculer. Remonte les poings vers les épaules, freine la descente."},
            {"nom": "4. Planche Commando", "detail": "Gainage sur les coudes. Passe sur la main droite, puis la main gauche, puis redescends sur les coudes. Garde les fessiers serrés pour que le bassin ne bascule pas de droite à gauche."}
        ]
    }

    # Variables d'état
    etat = {"seance": "A", "index": 0, "temps": 40, "en_cours": False}

    # UI Elements
    titre = ft.Text("SÉANCE A (Poussée)", size=24, weight="bold", color="#00e5ff")
    exo_titre = ft.Text(seances["A"][0]["nom"], size=22, weight="bold", color="white")
    exo_detail = ft.Text(seances["A"][0]["detail"], size=16, color="#b0bec5", italic=True)
    chrono_txt = ft.Text("40", size=80, weight="bold", color="#5e2a84")
    
    def update_ui():
        exo_titre.value = seances[etat["seance"]][etat["index"]]["nom"]
        exo_detail.value = seances[etat["seance"]][etat["index"]]["detail"]
        chrono_txt.value = str(etat["temps"])
        page.update()

    async def run_timer(e):
        etat["en_cours"] = True
        btn_play.disabled = True
        btn_pause.disabled = False
        page.update()
        
        while etat["temps"] > 0 and etat["en_cours"]:
            await asyncio.sleep(1)
            etat["temps"] -= 1
            chrono_txt.value = str(etat["temps"])
            page.update()
            
        btn_play.disabled = False
        btn_pause.disabled = True
        page.update()

    def pause_timer(e):
        etat["en_cours"] = False
        btn_play.disabled = False
        btn_pause.disabled = True
        page.update()

    def next_step(e):
        etat["en_cours"] = False
        btn_play.disabled = False
        btn_pause.disabled = True
        # Alternance Effort (40s) et Repos (20s)
        if etat["temps"] > 20 or etat["temps"] == 0: 
            etat["temps"] = 20 # Passe en repos
            chrono_txt.color = "#00e5ff"
            exo_titre.value = "Repos ! Prépare le suivant :"
        else:
            etat["temps"] = 40 # Passe à l'effort suivant
            chrono_txt.color = "#5e2a84"
            etat["index"] = (etat["index"] + 1) % 4
        update_ui()

    def choose_seance(seance_id):
        etat["seance"] = seance_id
        etat["index"] = 0
        etat["temps"] = 40
        etat["en_cours"] = False
        chrono_txt.color = "#5e2a84"
        titre.value = f"SÉANCE {seance_id}"
        update_ui()

    # Boutons de contrôle
    btn_play = ft.ElevatedButton("Lancer", on_click=run_timer, bgcolor="#5e2a84", color="white")
    btn_pause = ft.ElevatedButton("Pause", on_click=pause_timer, disabled=True, bgcolor="#333333", color="white")
    btn_next = ft.ElevatedButton("Suivant", on_click=next_step, bgcolor="#00e5ff", color="black")
    
    controle_row = ft.Row([btn_play, btn_pause, btn_next], alignment=ft.MainAxisAlignment.CENTER)

    # Boutons de sélection
    btn_sa = ft.OutlinedButton("Séance A", on_click=lambda e: choose_seance("A"))
    btn_sb = ft.OutlinedButton("Séance B", on_click=lambda e: choose_seance("B"))
    selection_row = ft.Row([btn_sa, btn_sb], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column([
            titre,
            ft.Divider(color="#5e2a84"),
            selection_row,
            ft.Container(content=ft.Column([exo_titre, exo_detail]), padding=20, bgcolor="#1a1a1a", border_radius=10, margin=ft.margin.symmetric(vertical=20)),
            ft.Row([chrono_txt], alignment=ft.MainAxisAlignment.CENTER),
            controle_row
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
ft.run(main)
