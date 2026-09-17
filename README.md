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
