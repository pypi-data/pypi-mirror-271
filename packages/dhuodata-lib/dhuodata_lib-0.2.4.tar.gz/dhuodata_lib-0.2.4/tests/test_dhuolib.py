import json
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append("src")
from dhuolib.clients import DhuolibClient


class TestDhuolibUtils(unittest.TestCase):
    def setUp(self):
        self.end_point = "http://localhost:8000"
        self.dhuolib = DhuolibClient(service_endpoint=self.end_point)
        self.file_path = "tests/files/LogisticRegression_best.pickle"
        
    # def test_integracao(self):
    #     experiment_params = {
    #         "experiment_name": "test_experiment_nlp",
    #         "experiment_tags": {"version": "v1", "priority": "P1"},
    #         "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
    #         "requirements_file": "tests/files/requirements.txt"
    #     }

    #     response = self.dhuolib.create_experiment(experiment_params)

        
    def test_deve_lancar_excecao_com_valores_run_params_incorretos(self):
        experiment_params = {
            "experiment_name": "test_experiment",
            "experiment_tags": {"version": "v1", "priority": "P1"}
        }
        response = self.dhuolib.create_experiment(experiment_params)
        self.assertEqual(list(response.keys()), ["error"])

    @patch("requests.post")
    def test_deve_criar_o_experimento_com_run_params_corretos(
        self, mock_post
    ):
        client = DhuolibClient(service_endpoint=self.end_point)

        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"experiment_id": "1"}

        experiment_params = {
            "experiment_name": "test_experiment",
            "experiment_tags": {"version": "v1", "priority": "P1"},
            "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
            "requirements_file": "tests/files/requirements.txt"
        }
        
        response = client.create_experiment(experiment_params)
        self.assertEqual(response, mock_response.json.return_value)
        
    @patch("requests.post")
    def test_deve_executar_o_experimento_com_run_params_corretos(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "current_stage": "Production",
            "last_updated_timestamp": 1713582060414,
            "model_version": "1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "status": "READY",
        }

        run_params = {
            "experiment_id": '2',
            "stage": "Production",
            "modelname": "nlp_framework",
            "modeltag": "v1",
            "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
            "requirements_file": "tests/files/requirements.txt"
        }
        response = self.dhuolib.run_experiment(run_params)

        self.assertEqual(response, mock_response.json.return_value)