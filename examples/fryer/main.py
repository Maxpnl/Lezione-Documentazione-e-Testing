"""Modulo friggitrice"""

import time
from typing import Dict, Any, Optional, Union, List

from fryer import send_to_fryer


class FrenchFryFryer:
    """Classe che gestisce la frittura delle patatine."""
    
    def __init__(self, target_temp: float = 180.0):
        """Inizializza la friggitrice per patatine."""
        self.target_temp = target_temp  # Temperatura target in gradi Celsius
        self.is_heating = False         # Se sta scaldando l'olio o meno
        self.potatoes_loaded = False    # Se le patatine sono caricate o meno
        
    def check_temperature(self) -> float:
        """Controlla la temperatura attuale della friggitrice."""
        return send_to_fryer("read_temperature")
    
    def heat_oil(self, max_attempts: int = 6) -> bool:
        """Riscalda l'olio fino alla temperatura target."""
        # Avvia il riscaldamento
        send_to_fryer("heat", {"action": "start"})
        self.is_heating = True
        
        # Controlla la temperatura fino a raggiungere quella target
        attempts = 0
        current_temp = self.check_temperature()
        
        while current_temp < self.target_temp and attempts < max_attempts:
            print(f"Riscaldamento in corso... Temperatura attuale: {current_temp:.1f}°C")
            send_to_fryer("sleep", {"seconds": 5})
            current_temp = self.check_temperature()
            attempts += 1
            
        # Verifica se la temperatura target è stata raggiunta
        if current_temp >= self.target_temp:
            print(f"Temperatura target raggiunta: {current_temp:.1f}°C")
            return True
        else:
            send_to_fryer("heat", {"action": "stop"})
            self.is_heating = False
            raise TimeoutError(f"Impossibile raggiungere la temperatura target dopo {max_attempts} tentativi")
    
    def load_potatoes(self, quantity: float) -> None:
        """Carica le patatine nella friggitrice."""
        if quantity <= 0:
            raise ValueError("La quantità di patatine deve essere maggiore di zero")
        
        if quantity > 2.0:
            raise ValueError("Quantità massima di patatine: 2 kg")
            
        print(f"Caricamento di {quantity} kg di patatine nella friggitrice")
        self.potatoes_loaded = True
    
    def fry(self, frying_time: float = 180.0) -> None:
        """Frigge le patatine per il tempo specificato."""
        if not self.is_heating:
            raise RuntimeError("Il riscaldamento non è attivo")
            
        if not self.potatoes_loaded:
            raise RuntimeError("Nessuna patata caricata nella friggitrice")
        
        # Controlla che la temperatura sia vicina a quella target
        current_temp = self.check_temperature()
        if current_temp < self.target_temp * 0.9:  # 90% della temperatura target
            raise RuntimeError(f"Temperatura troppo bassa: {current_temp:.1f}°C")
        
        print(f"Inizio frittura delle patatine per {frying_time} secondi")
        send_to_fryer("sleep", {"seconds": frying_time})
        print("Frittura completata!")
    
    def remove_fries(self) -> List[str]:
        """Rimuove le patatine dalla friggitrice."""
        if not self.potatoes_loaded:
            raise RuntimeError("Nessuna patata da rimuovere")
            
        print("Rimozione delle patatine dalla friggitrice")
        self.potatoes_loaded = False
        return ["🍟"] * 10  # Simulate french fries
    
    def shutdown(self) -> None:
        """Spegne la friggitrice."""
        if self.is_heating:
            send_to_fryer("heat", {"action": "stop"})
            self.is_heating = False
        print("Friggitrice spenta")
    
    def cook_french_fries(self, quantity, cooking_time) -> List[str]:
        """Processo completo di frittura delle patatine."""
        try:
            # Riscalda l'olio
            self.heat_oil()
            
            # Carica le patatine
            self.load_potatoes(quantity)
            
            # Friggi
            self.fry(cooking_time)
            
            # Spegni la friggitrice
            self.shutdown()
            # Rimuovi e restituisci le patatine
            return self.remove_fries()
        except Exception as e:
            print(f"Errore durante la frittura: {e}")
            # Spegni la friggitrice in caso di errore
            self.shutdown()
            raise
        finally:
            # Assicurati che la friggitrice venga spenta in caso di errore
            if self.is_heating:
                self.shutdown()
            