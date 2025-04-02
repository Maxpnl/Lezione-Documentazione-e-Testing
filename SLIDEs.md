---
marp: true
---

# Chi sono

### Mattia Furlani

- Solution architect @ Giunti
- Backend developer e Penetetration tester
- LinkedIn: https://www.linkedin.com/in/mattia-furlani/
- Email: mattia.furlani@protonmail.com

---

# Cosa è il Testing del software

### Perchè è importante

- Aumenta la sicurezza dello sviluppatore nei confronti di nuove implementazioni o modifiche al codice
- Permette di individuare bug in tempo
- Documenta le funzionalità del software
- Promuove la scrittura di validazioni all'interno del codice (numeri negativi, stringhe vuote, ecc.)

---

# Esempio friggitrice

- Immaginiamo una funzione `send_to_fryer(operazione, argomenti)` che invia comandi a una friggitrice
- Il comando `heat` accetta solo "start" o "stop" e fa partire il riscaldamento
- Il comando `read_temperature` restituisce la temperatura attuale
- Il comando `sleep` fa partire un timer di X secondi

---

# Classe FrenchFryFryer

- **Classe FrenchFryFryer**:
  - Gestisce tutte le operazioni della friggitrice
  - Mantiene lo stato della friggitrice (temperatura, riscaldamento, presenza di patatine)
  - Controlla l'intero processo di frittura
- **Metodo cook_french_fries**:
  - Coordina l'intero processo di frittura
  - Riscalda l'olio, carica le patatine, frigge e spegne la friggitrice
  - Restituisce le patatine fritte come risultato

---

```python
class FrenchFryFryer:
    """Classe che gestisce la frittura delle patatine."""

    def __init__(self, target_temp: float = 180.0):
        """Inizializza la friggitrice per patatine."""
        self.target_temp = target_temp  # Temperatura target in gradi Celsius
        self.is_heating = False         # Se sta scaldando l'olio o meno
        self.potatoes_loaded = False    # Se le patatine sono caricate o meno

    #......

    def cook_french_fries(self, quantity, cooking_time) -> List[str]:
        """Processo completo di frittura delle patatine."""
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
```

---

# Metodo heat_oil

- **Funzionalità**:
  - Avvia il riscaldamento dell'olio verso la temperatura target
  - Monitora la temperatura corrente attraverso controlli periodici
  - Ha un numero massimo di tentativi per raggiungere la temperatura
- **Comportamento**:
  - Invia il comando "heat" con azione "start" alla friggitrice
  - Attende e controlla periodicamente la temperatura
  - Solleva un'eccezione se non raggiunge la temperatura target
  - Restituisce True se il riscaldamento è avvenuto con successo

---

```python
def heat_oil(self, max_attempts: int = 6) -> bool:
    """Riscalda l'olio fino alla temperatura target."""
    # Avvia il riscaldamento
    fryer.send_to_fryer("heat", {"action": "start"})
    self.is_heating = True

    # Controlla la temperatura fino a raggiungere quella target
    attempts = 0
    current_temp = self.check_temperature()

    while current_temp < self.target_temp and attempts < max_attempts:
        print(f"Riscaldamento in corso... Temperatura attuale: {current_temp:.1f}°C")
        fryer.send_to_fryer("sleep", {"seconds": 5})
        current_temp = self.check_temperature()
        attempts += 1

    # Verifica se la temperatura target è stata raggiunta
    if current_temp >= self.target_temp:
        print(f"Temperatura target raggiunta: {current_temp:.1f}°C")
        return True
    else:
        fryer.send_to_fryer("heat", {"action": "stop"})
        self.is_heating = False
        raise TimeoutError(f"Impossibile raggiungere la temperatura target dopo {max_attempts} tentativi")
```

---

# Metodo load_potatoes

- **Funzionalità**:
  - Carica una quantità specificata di patatine nella friggitrice
  - Verifica che la quantità sia valida (maggiore di zero e non eccessiva)
- **Controlli**:
  - Verifica che la quantità sia maggiore di zero
  - Verifica che la quantità non superi il limite massimo di 2 kg
- **Comportamento**:
  - Aggiorna lo stato della friggitrice indicando la presenza di patatine
  - Solleva un'eccezione se i parametri non sono validi

---

```python
def load_potatoes(self, quantity: float) -> None:
    """Carica le patatine nella friggitrice."""
    if quantity <= 0:
        raise ValueError("La quantità di patatine deve essere maggiore di zero")

    if quantity > 2.0:
        raise ValueError("Quantità massima di patatine: 2 kg")

    print(f"Caricamento di {quantity} kg di patatine nella friggitrice")
    self.potatoes_loaded = True
```

---

# Metodo fry

- **Funzionalità**:
  - Gestisce il processo di frittura per un tempo specificato
  - Verifica le condizioni necessarie per una corretta frittura
- **Controlli**:
  - Verifica che il riscaldamento sia attivo
  - Verifica che le patatine siano state caricate
  - Controlla che la temperatura sia adeguata (almeno 90% di quella target)
- **Comportamento**:
  - Avvia il timer per la frittura
  - Solleva eccezioni se le condizioni non sono adatte alla frittura

---

```python
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

    fryer.send_to_fryer("sleep", {"seconds": frying_time})

    print("Frittura completata!")
```

---

# Metodi remove_fries e shutdown

- **Metodo remove_fries**:
  - Rimuove le patatine fritte dalla friggitrice
  - Verifica che ci siano patatine da rimuovere
  - Restituisce le patatine fritte come risultato
- **Metodo shutdown**:
  - Verifica lo stato attuale del riscaldamento
  - Invia il comando di spegnimento alla friggitrice se necessario

---

```python
def remove_fries(self) -> List[str]:
    """Rimuove le patatine dalla friggitrice."""
    if not self.potatoes_loaded:
        raise RuntimeError("Nessuna patata da rimuovere")

    print("Rimozione delle patatine dalla friggitrice")

    self.potatoes_loaded = False
    return ["🍟"] * 10

def shutdown(self) -> None:
    """Spegne la friggitrice."""
    if self.is_heating:
        fryer.send_to_fryer("heat", {"action": "stop"})
        self.is_heating = False
    print("Friggitrice spenta")
```

---

# Cosa possiamo testare?

- *Side effect* e valori di ritorno
- Validazione dei parametri e casi limite
- Quali funzioni vengono chiamate
- Integrazione con altre parti del sistema

---

# Di che cosa?

- **Unit test**: testano una singola unità di codice (funzione o metodo)
- **Integration test**: testano l'integrazione tra più unità di codice
- **End to end test**: testano il sistema completo, dall'inizio alla fine
- **Regression test**: testano che bug precedentemente risolti non si ripresentino
- _System test_: testano il sistema in un ambiente di produzione
- _Acceptance test_: testano che il sistema soddisfi i requisiti del cliente

---

# Unit test per shutdown

```python
def shutdown(self) -> None:
    """Spegne la friggitrice."""
    if self.is_heating:
        fryer.send_to_fryer("heat", {"action": "stop"})
        self.is_heating = False
    print("Friggitrice spenta")
```

- Chiamare `shutdown` quando _is_heating_ è True
  - Controllare che _is_heating_ venga impostato su False
  - Assicurarsi che il comando di spegnimento venga inviato
- Chiamare `shutdown` quando _is_heating_ è False
  - Controllare che _is_heating_ rimanga False
  - Assicurarsi che il comando di spegnimento NON venga inviato
---
```python
import unittest
from main import FrenchFryFryer

class TestFrenchFryFryer(unittest.TestCase):
    """Test per la classe FrenchFryFryer."""
    
    def setUp(self):
        """Inizializza una nuova istanza di FrenchFryFryer prima di ogni test."""
        self.fryer = FrenchFryFryer()

    def test_shutdown(self):
        """Verifica che shutdown spenga il riscaldamento se è attivo."""
        self.fryer.is_heating = True
        self.fryer.shutdown()
        
        # Verifiche
        self.assertFalse(self.fryer.is_heating)
    
    def test_shutdown_already_off(self):
        """Verifica che shutdown non faccia nulla se il riscaldamento è già spento."""
        self.fryer.is_heating = False
        self.fryer.shutdown()
        
        # Verifiche
        self.assertFalse(self.fryer.is_heating)
```
---
```python
import unittest
from unittest.mock import patch
from main import FrenchFryFryer

class TestFrenchFryFryer(unittest.TestCase):
    """Test per la classe FrenchFryFryer."""
    
    def setUp(self):
        """Inizializza una nuova istanza di FrenchFryFryer prima di ogni test."""
        self.fryer = FrenchFryFryer()

    @patch('main.send_to_fryer') # Rimpiazza la funzione send_to_fryer con un mock
    def test_shutdown(self, mock_send):
        """Verifica che shutdown spenga il riscaldamento se è attivo."""
        self.fryer.is_heating = True
        self.fryer.shutdown()
        
        # Verifiche
        mock_send.assert_called_once_with("heat", {"action": "stop"})
        self.assertFalse(self.fryer.is_heating)
    
    @patch('main.send_to_fryer') # Rimpiazza la funzione send_to_fryer con un mock
    def test_shutdown_already_off(self, mock_send):
        """Verifica che shutdown non faccia nulla se il riscaldamento è già spento."""
        self.fryer.is_heating = False
        self.fryer.shutdown()
        mock_send.assert_not_called()
```
