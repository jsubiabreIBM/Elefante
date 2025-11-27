import pytest
from unittest.mock import MagicMock, patch
from src.core.orchestrator import MemoryOrchestrator
from src.utils.config import Config, ElefanteConfig, UserProfileConfig

class TestUserProfileLogic:
    @pytest.fixture
    def orchestrator(self):
        # Mock dependencies to avoid DB connections
        with patch('src.core.orchestrator.get_config') as mock_get_config:
            # Setup config
            config = MagicMock(spec=Config)
            elefante_config = MagicMock(spec=ElefanteConfig)
            user_profile_config = UserProfileConfig(
                user_name="TestUser",
                auto_link_first_person=True,
                detect_code_blocks=True
            )
            elefante_config.user_profile = user_profile_config
            config.elefante = elefante_config
            mock_get_config.return_value = config
            
            # Create orchestrator with mocked DBs
            with patch('src.core.orchestrator.VectorStore'), \
                 patch('src.core.orchestrator.GraphStore'), \
                 patch('src.core.orchestrator.EmbeddingService'):
                orch = MemoryOrchestrator()
                orch.config = config # Inject config directly
                return orch

    def test_positive_matches(self, orchestrator):
        """Test valid first-person statements"""
        valid_sentences = [
            "I live in Canada",
            "My favorite color is blue",
            "We should deploy this",
            "This is mine",
            "Please call me later",
            "our project is going well"
        ]
        for sentence in valid_sentences:
            assert orchestrator._is_first_person_statement(sentence), f"Failed to match: {sentence}"

    def test_negative_matches_code(self, orchestrator):
        """Test code patterns that should be ignored"""
        code_samples = [
            "for i in range(10):",
            "if my_var == 1:",
            "def my_function():",
            "import os",
            "class MyClass:",
            "return i",
            "print(i)",
            "user_id = 123"
        ]
        for code in code_samples:
            assert not orchestrator._is_first_person_statement(code), f"Incorrectly matched code: {code}"

    def test_negative_matches_variables(self, orchestrator):
        """Test variable names that contain pronouns"""
        variables = [
            "my_variable",
            "dummy_variable",
            "time_index",
            "our_function",
            "mine_craft"
        ]
        for var in variables:
            assert not orchestrator._is_first_person_statement(var), f"Incorrectly matched variable: {var}"

    def test_config_disable(self, orchestrator):
        """Test disabling the feature"""
        orchestrator.config.elefante.user_profile.auto_link_first_person = False
        assert not orchestrator._is_first_person_statement("I live in Canada")
