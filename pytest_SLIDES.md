---
marp: true
---

# Pytest: modern Python testing

### Un framework di testing potente e flessibile

- Framework di testing Python avanzato e di facile utilizzo
- Sintassi semplice rispetto a unittest (non richiede classi)
- Funzionalità avanzate per discovery e report dei test
- Ampia compatibilità con unittest e altri framework
- Estensibile tramite plugin

---

# Installazione e primo test

```python
# Installazione
pip install pytest

# Esempio di test semplice (test_sample.py)
def test_sum():
    assert sum([1, 2, 3]) == 6, "La somma dovrebbe essere 6"
```

Esecuzione:
```bash
$ pytest
===================== test session starts =====================
collected 1 item

test_sample.py .                                       [100%]

====================== 1 passed in 0.01s ======================
```

---

# Struttura dei test con pytest

- I file di test devono iniziare con `test_` o finire con `_test.py`
- Le funzioni di test devono iniziare con `test_`
- L'esito del test è determinato da semplici assert Python
- Non è necessario creare classi di test (ma è possibile)

```python
# test_fryer.py
def test_shutdown():
    fryer = FrenchFryFryer()
    fryer.is_heating = True
    fryer.shutdown()
    
    assert not fryer.is_heating, "is_heating dovrebbe essere False"
```

---

# Fixture: concetto chiave

- **Fixture**: meccanismo per preparare e ripulire dati/oggetti per i test
- Sostituiscono il pattern setUp/tearDown di unittest
- Più flessibili e componibili
- Permettono di riutilizzare risorse tra test
- Risolvono automaticamente le dipendenze

```python
import pytest

@pytest.fixture
def fryer():
    """Crea e restituisce un'istanza di FrenchFryFryer."""
    return FrenchFryFryer()
```

---

# Uso delle fixture 

```python
def test_shutdown(fryer):  # La fixture viene iniettata automaticamente
    fryer.is_heating = True
    fryer.shutdown()
    
    assert not fryer.is_heating

def test_load_potatoes(fryer):
    fryer.load_potatoes(1.0)
    
    assert fryer.potatoes_loaded

def test_multiple_fixtures(fryer, another_fixture):
    # È possibile utilizzare più fixture contemporaneamente
    pass
```

---

# Fixture con scope

- **scope**: determina la durata della fixture
  - `function`: creata per ogni funzione di test (default)
  - `class`: creata una volta per classe
  - `module`: creata una volta per modulo
  - `session`: creata una volta per sessione di test

```python
@pytest.fixture(scope="module")
def database_connection():
    """Crea una connessione al database per l'intero modulo."""
    conn = create_connection()
    yield conn  # Restituisce la connessione al test
    conn.close()  # Cleanup eseguito dopo tutti i test
```

---

# Fixture con yield (teardown)

- Utilizzando `yield` invece di `return` possiamo eseguire operazioni di cleanup
- Il codice dopo lo `yield` viene eseguito dopo il completamento del test

```python
@pytest.fixture
def fryer_with_oil():
    """Crea e restituisce un'istanza di FrenchFryFryer con l'olio riscaldato."""
    fryer = FrenchFryFryer()
    fryer.is_heating = True
    fryer.potatoes_loaded = False
    
    # Setup completato, restituiamo la risorsa
    yield fryer
    
    # Teardown (eseguito dopo il test)
    if fryer.is_heating:
        fryer.shutdown()
```

---

# Parametrizzazione dei test

- Permette di eseguire lo stesso test con input diversi
- Evita la duplicazione di codice
- Rende i test più leggibili e manutenibili
---

```python
@pytest.mark.parametrize("quantity,expected", [
    (0.5, True),    # Quantità valida
    (1.0, True),    # Quantità valida
    (2.0, True),    # Quantità limite
    (2.1, False),   # Quantità eccessiva
    (-0.1, False),  # Quantità negativa
])
def test_load_potatoes_validation(fryer, quantity, expected):
    """Verifica la validazione della quantità di patatine."""
    if expected:
        fryer.load_potatoes(quantity)
        assert fryer.potatoes_loaded
    else:
        with pytest.raises(ValueError):
            fryer.load_potatoes(quantity)
```

---

# Mocking con pytest e monkeypatch

- **monkeypatch**: fixture integrata per sostituire oggetti durante i test
- Alternativa a `unittest.mock.patch`
- Utile per simulare API, chiamate esterne, ecc.
---
```python
def test_heat_oil(fryer, monkeypatch):
    """Verifica che heat_oil riscaldi correttamente l'olio."""
    # Sostituisce send_to_fryer con una funzione mock
    def mock_send_to_fryer(action, args=None):
        if action == "read_temperature":
            return 190.0
        return None
    
    # Applica il mock alla funzione
    monkeypatch.setattr('main.send_to_fryer', mock_send_to_fryer)
    
    # Esegue il test
    result = fryer.heat_oil()
    assert result
    assert fryer.is_heating
```

---

# pytest-mock: fixture per il mocking

- Plugin che fornisce la fixture `mocker`
- Semplifica ulteriormente il mocking
- Compatibile con unittest.mock
---
```python
def test_fry_success(fryer, mocker):
    """Verifica che fry funzioni correttamente."""
    # Setup
    fryer.is_heating = True
    fryer.potatoes_loaded = True
    
    # Crea un mock per send_to_fryer
    mock_send = mocker.patch('main.send_to_fryer')
    mock_send.return_value = 180.0  # Temperatura OK
    
    # Esegue il test
    fryer.fry(frying_time=10.0)
    
    # Verifiche
    assert mock_send.call_count >= 1
    mock_send.assert_any_call("sleep", {"seconds": 10.0})
```

---

# Marker e salto dei test

- **Marker**: etichette che possono essere applicate ai test
- Permettono di selezionare o escludere test specifici
- Marker predefiniti: skip, skipif, xfail, parametrize, ...
---
```python
@pytest.mark.slow
def test_long_integration():
    """Test di integrazione lungo che può essere saltato."""
    # Logica del test complessa e lunga
    pass

@pytest.mark.skipif(sys.platform == "win32", 
                    reason="Non eseguire su Windows")
def test_unix_specific():
    """Test specifico per sistemi Unix."""
    # Test specifico per Unix
    pass
```

Esecuzione: `pytest -m "not slow"` (esclude i test marcati come "slow")

---

# Test di integrazione con pytest

```python
@pytest.mark.integration
def test_complete_frying_process(mocker):
    """Test di integrazione per l'intero processo di frittura."""
    # Mock per send_to_fryer con temperature crescenti
    temperatures = [25.0, 100.0, 150.0, 180.0]
    mock_send = mocker.patch('main.send_to_fryer')
    
    # Implementa una side_effect che restituisce temperature crescenti
    # ad ogni chiamata a read_temperature
    mock_send.side_effect = lambda action, args=None: (
        temperatures.pop(0) if action == "read_temperature" and temperatures else None
    )
    
    # Crea una friggitrice e esegue il processo completo
    fryer = FrenchFryFryer()
    result = fryer.cook_french_fries(quantity=1.0, cooking_time=5.0)
    
    # Verifica i risultati
    assert len(result) == 10
    assert "🍟" in result
```

---

# Reporting e analisi dei test

- Output dettagliato per i test falliti
- Opzioni per incrementare la verbosità
- Report in vari formati (JUnit XML, HTML, ecc.)
- Integrazione con strumenti di coverage

```bash
# Esecuzione con report dettagliato
pytest -v

# Generazione di report XML per l'integrazione con CI
pytest --junitxml=results.xml

# Coverage report
pytest --cov=myproject --cov-report=html
```

---

# Esecuzione selettiva dei test

- Eseguire test specifici in base al nome
- Eseguire test in base ai marker
- Eseguire test che corrispondono a un pattern

```bash
# Eseguire un file di test specifico
pytest test_fryer.py

# Eseguire una funzione specifica
pytest test_fryer.py::test_shutdown

# Eseguire test con un marker specifico
pytest -m integration

# Eseguire test che contengono una stringa nel nome
pytest -k "shutdown"
```

---

# Best practice con pytest

- **Organizzazione**: test indipendenti e isolati
- **Nomi descrittivi**: i nomi dei test devono descrivere cosa testano
- **Fixture modulari**: creare fixture riutilizzabili e componibili
- **Assertion chiare**: messaggi di errore esplicativi
- **Parametrizzazione**: per testare casi simili
- **Test di confine**: testare casi limite e valori di confine
- **Separazione**: test unitari separati dai test di integrazione


---


# Pytest vs unittest

| Caratteristica | pytest | unittest |
|----------------|--------|----------|
| Sintassi | Semplice, basata su funzioni | Basata su classi e metodi |
| Asserzioni | `assert` nativo | Metodi `self.assertXxx()` |
| Fixture | Potenti e componibili | setUp/tearDown per classe |
| Parametrizzazione | Incorporata | Richiede implementazione manuale |
| Plugin | Ampio ecosistema | Limitato |
| Compatibilità | Esegue test unittest | Non esegue test pytest |
