import os
import sys
import time
from gpiozero import LEDBoard
import speech_recognition as sr

leds_portail = LEDBoard(17, 27, 22, 10, pwm=True)

def animation_chargement():
    os.system('clear')
    
    etapes = [
        "[INIT] Connexion au réseau sub-spatial Dimension C-137...",
        "[FETCH] Récupération de portal_gun_firmware_v4.2.bin",
        "[DL] Downloading: [==========>                    ] 34% (12.4 MB/s)",
        "[DL] Downloading: [====================>          ] 68% (18.1 MB/s)",
        "[DL] Downloading: [==============================] 100% (22.5 MB/s)",
        "[CHECK] Intégrité MD5 : a8f9c43b2e71... VALIDE",
        "[UNPACK] Décompression des matrices quantiques...",
        "[GPIO] Initialisation des broches 17, 27, 22, 10... [OK]",
        "[CALIBRATE] Densité du liquide de portail : 98.4%... [OK]",
        "[READY] Synchronisation neuronale établie."
    ]

    for etape in etapes:
        print(etape, flush=True)
        time.sleep(0.25)

    time.sleep(0.8)
    os.system('clear')
    afficher_interface()

def afficher_interface():
    print("=============================================", flush=True)
    print("    🧪 LABORATOIRE RICKLAB™ - OPÉRATIONNEL   ", flush=True)
    print("=============================================", flush=True)
    print("\n[À l'écoute...]\n", flush=True)

def ecouter_labo():
    reconnaissance = sr.Recognizer()

    with sr.Microphone() as source:
        reconnaissance.adjust_for_ambient_noise(source, duration=1)
        os.system('clear')
        print("...\n", flush=True)

        while True:
            try:
                audio = reconnaissance.listen(source, timeout=None, phrase_time_limit=5)
                texte = reconnaissance.recognize_google(audio, language="fr-FR").lower()
                texte_nettoye = texte.replace(",", "").replace(".", "").strip()
                print(f"🗣️ Entendu : \"{texte}\"")

                if "salut méta tu es avec moi" in texte_nettoye:
                    print ("\nToujours présent, je suis à votre écoute")

                elif "ok lance le programme" in texte_nettoye:
                        animation_chargement()

                elif "méta active le portail" in texte_nettoye:
                    print("\n🟢 [RICKLAB] : OUVERTURE DU PORTAIL EN COURS !")
                    leds_portail.pulse(fade_in_time=1.2, fade_out_time=1.2, background=True)
                    print("\n[Portail actif - En attente de l'ordre d'extinction...]\n")

                elif "méta désactive le portail" in texte_nettoye:
                    print("\n🔒 [RICKLAB] : FERMETURE DU PORTAIL...")
                    leds_portail.off()
                    print("Retour en veille.\n")
                    print("[À l'écoute...]")

                elif "méta fin de programme" in texte_nettoye:
                    print("\n[RICKLAB] : ARRET DU PROGRAMME")
                    break

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"❌ Erreur réseau : {e}")
                break
            except KeyboardInterrupt:
                leds_portail.off()
                print("\nArrêt d'urgence du système.")
                break

if __name__ == "__main__":
    ecouter_labo()