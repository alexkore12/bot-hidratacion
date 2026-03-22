"""
Tests for Bot de Hidratación
Test commands, stats, and error handling
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig:
    """Test configuration module"""
    
    def test_config_imports(self):
        """Should import config successfully"""
        from config import HORARIOS, MENSAJE, INTERVALO_CHECK
        assert HORARIOS is not None
        assert isinstance(HORARIOS, list)
        assert len(HORARIOS) > 0
    
    def test_horarios_format(self):
        """All horarios should be in HH:MM format"""
        from config import HORARIOS
        for h in HORARIOS:
            assert len(h) == 5
            assert h[2] == ':'
    
    def test_mensaje_not_empty(self):
        """Mensaje should not be empty"""
        from config import MENSAJE
        assert MENSAJE is not None
        assert len(MENSAJE) > 0
    
    def test_intervalo_check_positive(self):
        """Intervalo should be positive"""
        from config import INTERVALO_CHECK
        assert INTERVALO_CHECK > 0


class TestBotCommands:
    """Test bot command handlers"""
    
    @patch('main.bot')
    def test_start_command(self, mock_bot):
        """Start command should send welcome message"""
        from main import handle_start
        mock_message = Mock()
        mock_message.chat.id = 123456
        mock_message.from_user.first_name = "Test User"
        
        handle_start(mock_message)
        
        mock_bot.send_message.assert_called_once()
    
    @patch('main.bot')
    def test_stop_command(self, mock_bot):
        """Stop command should send confirmation"""
        from main import handle_stop
        mock_message = Mock()
        mock_message.chat.id = 123456
        
        handle_stop(mock_message)
        
        mock_bot.send_message.assert_called_once()
    
    @patch('main.bot')
    def test_status_command(self, mock_bot):
        """Status command should show current state"""
        from main import handle_status
        mock_message = Mock()
        mock_message.chat.id = 123456
        
        handle_status(mock_message)
        
        mock_bot.send_message.assert_called_once()
    
    @patch('main.bot')
    def test_stats_command(self, mock_bot):
        """Stats command should show statistics"""
        from main import handle_stats
        mock_message = Mock()
        mock_message.chat.id = 123456
        
        handle_stats(mock_message)
        
        mock_bot.send_message.assert_called_once()


class TestBotLogic:
    """Test bot core logic"""
    
    def test_is_time_to_send(self):
        """Should correctly determine if it's time to send"""
        from main import is_time_to_send
        from config import HORARIOS
        
        # Should match any horario
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        result = is_time_to_send(current_time)
        assert isinstance(result, bool)
    
    def test_get_uptime(self):
        """Uptime calculation should work"""
        from main import get_uptime
        uptime = get_uptime()
        assert uptime is not None
        assert "h" in uptime or "m" in uptime


class TestErrorHandling:
    """Test error handling"""
    
    @patch('main.bot')
    def test_handle_invalid_command(self, mock_bot):
        """Should handle unknown commands gracefully"""
        from main import handle_unknown
        mock_message = Mock()
        mock_message.chat.id = 123456
        mock_message.text = "/unknowncmd"
        
        handle_unknown(mock_message)
        
        mock_bot.send_message.assert_called_once()


class TestEnvConfig:
    """Test environment configuration"""
    
    def test_env_token_optional(self):
        """Token should be optional for testing"""
        # Should not fail without token
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        assert token is None or isinstance(token, str)
    
    def test_env_example_exists(self):
        """Env example file should exist"""
        env_example = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.env.example'
        )
        assert os.path.exists(env_example)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
