"""Test di integrazione."""

import unittest
from unittest.mock import patch
import time
from fryer import send_to_fryer
from main import FrenchFryFryer


class TestFryerIntegration(unittest.TestCase):
    """Test di integrazione per verificare l'interazione tra i componenti."""
    
    @patch('main.send_to_fryer')
    def test_complete_frying_process(self, mock_send):
        """
        Test di integrazione che verifica l'intero processo di frittura
        con una simulazione realistica delle risposte della friggitrice.
        """
        # Simula risposte realistiche della friggitrice
        temperature_sequence = [25.0, 100.0, 150.0, 179.0, 182.0, 181.0]
        current_temp_index = 0
        
        def mock_send_to_fryer(action, args=None):
            nonlocal current_temp_index
            
            if action == "read_temperature":
                temp = temperature_sequence[min(current_temp_index, len(temperature_sequence) - 1)]
                current_temp_index += 1
                return temp
            elif action == "sleep":
                # Non attendere realmente durante i test
                return None
            elif action == "heat":
                return None
        
        mock_send.side_effect = mock_send_to_fryer
        
        # Crea l'istanza della friggitrice
        fryer = FrenchFryFryer(target_temp=180.0)
        
        # Esegui il processo completo
        fries = fryer.cook_french_fries(quantity=1.0, cooking_time=3.0)
        
        # Verifica i risultati
        self.assertEqual(len(fries), 10)
        self.assertEqual(fries[0], "🍟")
        
        # Verifica la sequenza di chiamate alla friggitrice
        call_actions = [call[0][0] for call in mock_send.call_args_list]
        
        # Verifica che le azioni principali siano state chiamate nell'ordine corretto
        self.assertEqual(call_actions[0], "heat")  # Avvio riscaldamento
        self.assertIn("read_temperature", call_actions)  # Controllo temperatura
        self.assertIn("sleep", call_actions)  # Attesa durante la frittura
        self.assertEqual(call_actions[-1], "heat")  # Spegnimento finale
    
    @patch('main.send_to_fryer')
    def test_temperature_never_reaches_target(self, mock_send):
        """
        Test di integrazione che verifica il comportamento quando 
        la temperatura non raggiunge mai il target.
        """
        # Simula una temperatura che non raggiunge mai il target
        mock_send.side_effect = lambda action, args=None: 120.0 if action == "read_temperature" else None
        
        # Crea l'istanza della friggitrice
        fryer = FrenchFryFryer(target_temp=180.0)
        
        # Esegui il processo e verifica che sollevi l'eccezione attesa
        with self.assertRaises(Exception) as context:
            fryer.cook_french_fries(quantity=1.0, cooking_time=3.0)
        
        # Verifica che sia stato effettivamente un timeout di temperatura
        self.assertIn("Impossibile raggiungere la temperatura target", str(context.exception))
        
        # Verifica che la friggitrice sia stata spenta
        heat_calls = [call for call in mock_send.call_args_list if call[0][0] == "heat"]
        self.assertEqual(len(heat_calls), 2)  # start e stop
        self.assertEqual(heat_calls[0][0][1], {"action": "start"})
        self.assertEqual(heat_calls[1][0][1], {"action": "stop"})


class TestEndToEndFrying(unittest.TestCase):
    """
    Test end-to-end che simulano l'intero processo di frittura
    con diversi scenari e parametri.
    """
    
    @patch('random.uniform')
    @patch('time.sleep')
    def test_successful_frying_minimal_time(self, mock_sleep, mock_uniform):
        """
        Test E2E che simula un processo di frittura di successo
        con tempi minimi per velocizzare il test.
        """
        # Bypass sleep per accelerare i test
        mock_sleep.return_value = None
        
        # Simula temperature in aumento per superare il target
        temperature_values = [25.0, 100.0, 170.0, 185.0, 182.0, 183.0]
        mock_uniform.side_effect = temperature_values
        
        # Esegui il processo completo con parametri minimi
        fryer = FrenchFryFryer(target_temp=180.0)
        result = fryer.cook_french_fries(quantity=0.5, cooking_time=1.0)
        
        # Verifica il risultato
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], "🍟")
    
    @patch('main.send_to_fryer', wraps=send_to_fryer)
    @patch('random.uniform')
    @patch('time.sleep')
    def test_error_handling_with_invalid_input(self, mock_sleep, mock_uniform, mock_send):
        """
        Test E2E che verifica la gestione degli errori con input non validi.
        """
        # Bypass sleep per accelerare i test
        mock_sleep.return_value = None
        
        # Simula temperature in aumento
        temperature_values = [25.0, 100.0, 170.0, 185.0, 182.0, 183.0]
        mock_uniform.side_effect = temperature_values
        
        # Crea l'istanza della friggitrice
        fryer = FrenchFryFryer(target_temp=180.0)
        
        # Verifica che quantità di patatine non valide vengano gestite correttamente
        with self.assertRaises(ValueError):
            fryer.cook_french_fries(quantity=0, cooking_time=1.0)
        
        with self.assertRaises(ValueError):
            fryer.cook_french_fries(quantity=-1.0, cooking_time=1.0)
        
        with self.assertRaises(ValueError):
            fryer.cook_french_fries(quantity=3.0, cooking_time=1.0)
        
        # Verifica che la friggitrice venga spenta dopo ogni errore
        print(mock_send.call_args_list)
        self.assertEqual(mock_send.call_args[0][0], "heat")
        self.assertEqual(mock_send.call_args[0][1], {"action": "stop"})


if __name__ == '__main__':
    unittest.main()