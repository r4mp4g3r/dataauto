# tests/test_scheduler.py

import pytest
from unittest.mock import patch
from dataauto.scheduler import schedule_command

def test_schedule_command(mocker):
    with patch('dataauto.scheduler.schedule') as mock_schedule:
        with patch('dataauto.scheduler.threading.Thread') as mock_thread:
            # Mock the 'do' method
            mock_job = mocker.Mock()
            mock_schedule.every.return_value.at.return_value.do.return_value = mock_job
            
            schedule_command('load', '/path/to/file.csv', '14:30')
            
            # Assert that 'schedule.every().day.at().do(job)' was called
            mock_schedule.every.assert_called_once()
            mock_schedule.every.return_value.day.at.assert_called_once_with('14:30')
            mock_schedule.every.return_value.day.at.return_value.do.assert_called_once()
    
            # Assert that the scheduler thread was started
            mock_thread.assert_called_once()
            mock_thread.return_value.start.assert_called_once()