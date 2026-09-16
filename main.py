import speech_recognition as sr
import time

def ecouter_labo():
    # Initialisation de la reconnaissance vocale
    reconnaissance = sr.Recognizer()
    
    print("=============================================")
    print("    🧪 TEST LABORATOIRE RICKLAB™ - SUR PC    ")
    print("=============================================")
    print("🎙️ Le microphone est ouvert. Parlez maintenant...")
    print("💡 Dites une phrase contenant le mot 'PORTAIL' ou 'RICK'.")
    print("---------------------------------------------")

    with sr.Microphone() as source:
        # Ajustement automatique au bruit ambiant de la pièce
        reconnaissance.adjust_for_ambient_noise(source, duration=1)
        print("[À l'écoute...]")
        
        while True:
            try:
                # Capture de la voix
                audio = reconnaissance.listen(source, timeout=None, phrase_time_limit=5)
                
                # Traduction de l'audio en texte via l'API Google (Français)
                texte = reconnaissance.recognize_google(audio, language="fr-FR").lower()
                print(f"🗣️ Entendu : \"{texte}\"")

                # Détection des mots-clés de Rick
                if "portail" in texte or "rick" in texte:
                    print("\n🟢 [ALERTE RICKLAB] : OUVERTURE DU PORTAIL VERT DETECTÉE !")
                    print("⚡ (Ici, le Raspberry Pi allumera la LED et le Plexiglas) ⚡")
                    
                    time.sleep(3) # Simule le temps d'ouverture du portail
                    
                    print("\n🔒 Portail refermé. Retour en veille.\n")
                    print("[À l'écoute...]")

            except sr.UnknownValueError:
                # L'IA n'a pas compris le bruit ou la phrase, on continue d'écouter
                pass
            except sr.RequestError as e:
                print(f"❌ Erreur de connexion au service vocal : {e}")
                break
            except KeyboardInterrupt:
                print("\nArrêt du test du laboratoire.")
                break

if __name__ == "__main__":
    ecouter_labo()