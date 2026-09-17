- RickLab - Contrôle Vocal Meta & GPIO
Interface vocale interactive en Python connectée aux GPIO d'un Raspberry Pi (LEDs et buzzer piézoélectrique), pensée pour interagir avec des lunettes connectées Meta ou un micro Bluetooth.

- Fonctionnalités
Reconnaissance vocale en temps réel via l'API Google Speech Recognition.
Retours sonores via un buzzer piézoélectrique (bips, séquences d'ouverture et fermeture).
Animation lumineuse des broches GPIO à l'activation des commandes.
Animation de démarrage stylisée dans le terminal.

- Matériel requis
Raspberry Pi (ou carte compatible avec GPIO)
Microphone (micro des lunettes Meta connecté en Bluetooth ou micro USB)
4 LEDs (broches GPIO 17, 27, 22, 10)
1 Buzzer passif / piézoélectrique (broche GPIO 18)

- Prérequis logiciels
Installez les paquets système nécessaires pour la gestion du son :

bash
sudo apt-get update
sudo apt-get install python3-pip portaudio19-dev
Commandes vocales disponibles
"salut meta tu es avec moi" : joue un bip sonore de confirmation.

"ok lance le programme" : lance l'animation de démarrage dans la console.






import os
import sys
import time
from gpiozero import LEDBoard, TonalBuzzer
from gpiozero.tones import Tone
import speech_recognition as sr

leds_portail = LEDBoard(17, 27, 22, 10, pwm=True)
buzzer = TonalBuzzer(18, octaves=2)

def son_ouverture():
    for freq in range(300, 1250, 60):
        buzzer.play(Tone(freq))
        time.sleep(0.02)
    buzzer.stop()

def son_fermeture():
    for freq in range(1000, 240, -60):
        buzzer.play(Tone(freq))
        time.sleep(0.025)
    buzzer.stop()

def son_bip():
    buzzer.play(Tone(523))
    time.sleep(0.07)
    buzzer.stop()
    time.sleep(0.04)
    buzzer.play(Tone(784))
    time.sleep(0.07)
    buzzer.stop()

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
        # Petit clic sonore à chaque ligne qui défile
        buzzer.play(Tone(800))
        time.sleep(0.02)
        buzzer.stop()
        time.sleep(0.2)

    time.sleep(0.5)
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
                texte_nettoye = (
                    texte.replace(",", "")
                    .replace(".", "")
                    .replace("méta", "meta")
                    .replace("désactive", "desactive")
                    .strip()
                )
                print(f"🗣️ Entendu : \"{texte}\"")

                if "salut meta tu es avec moi" in texte_nettoye:
                    son_bip()
                    print("\nToujours présent, je suis à votre écoute\n")

                elif "ok lance le programme" in texte_nettoye:
                    animation_chargement()

                elif "meta active le portail" in texte_nettoye:
                    print("\n🟢 [RICKLAB] : OUVERTURE DU PORTAIL EN COURS !")
                    son_ouverture()
                    leds_portail.pulse(fade_in_time=1.2, fade_out_time=1.2, background=True)
                    print("[Portail actif - En attente de l'ordre d'extinction...]")

                elif "meta desactive le portail" in texte_nettoye:
                    print("\n🔒 [RICKLAB] : FERMETURE DU PORTAIL...")
                    son_fermeture()
                    leds_portail.off()
                    print("Retour en veille.\n")
                    print("[À l'écoute...]")

                elif "meta fin de programme" in texte_nettoye:
                    print("\n[RICKLAB] : ARRÊT DU PROGRAMME")
                    son_fermeture()
                    leds_portail.off()
                    break

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"❌ Erreur réseau : {e}")
                break
            except KeyboardInterrupt:
                leds_portail.off()
                buzzer.stop()
                print("\nArrêt d'urgence du système.")
                break

if __name__ == "__main__":
    ecouter_labo()

"meta active le portail" : active la pulsation des LEDs et joue le son d'ouverture.

"meta desactive le portail" : éteint les LEDs et joue le son de fermeture.

"meta fin de programme" : coupe les sorties et quitte le script.
