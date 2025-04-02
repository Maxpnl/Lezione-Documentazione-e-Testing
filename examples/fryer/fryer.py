# Simulazione della funzione di comunicazione con la friggitrice
import time
from typing import Any, Dict, Optional, Union


def send_to_fryer(action: str, arguments: Dict[str, Any] = None) -> Optional[Union[float, None]]:
    """Invia un comando alla friggitrice."""
    if arguments is None:
        arguments = {}
        
    if action == "sleep":
        if "seconds" not in arguments:
            raise ValueError("L'azione 'sleep' richiede l'argomento 'seconds'")
        # Simula l'attesa per il numero di secondi specificato
        time.sleep(arguments["seconds"])
        return None
        
    elif action == "heat":
        if "action" not in arguments:
            raise ValueError("L'azione 'heat' richiede l'argomento 'action'")
        if arguments["action"] not in ["start", "stop"]:
            raise ValueError("L'argomento 'action' per 'heat' deve essere 'start' o 'stop'")
        # Qui si simulerebbe l'accensione o lo spegnimento del riscaldamento
        print(f"Riscaldamento {'avviato' if arguments['action'] == 'start' else 'spento'}")
        return None
        
    elif action == "read_temperature":
        # Simula la lettura della temperatura (valore casuale tra 20 e 200)
        import random
        temp = random.uniform(20, 200)
        print(f"Temperatura attuale: {temp:.1f}°C")
        return temp
        
    else:
        raise ValueError(f"Azione non supportata: {action}")
