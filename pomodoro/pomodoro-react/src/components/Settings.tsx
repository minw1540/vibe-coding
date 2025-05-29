import { useState } from 'react';
import { X } from 'lucide-react';
import type { TimerSettings } from '../types/timer';
import '../styles/Settings.css';

interface SettingsProps {
  onClose: () => void;
  onSave: (settings: TimerSettings) => void;
  initialSettings: TimerSettings;
}

export const Settings = ({ onClose, onSave, initialSettings }: SettingsProps) => {
  const [settings, setSettings] = useState<TimerSettings>(initialSettings);

  const handleSave = () => {
    onSave(settings);
    onClose();
  };

  return (
    <div className="settings-overlay">
      <div className="settings-container">
        <div className="settings-header">
          <h2>설정</h2>
          <button onClick={onClose} className="close-button">
            <X size={24} />
          </button>
        </div>

        <div className="settings-content">
          <div className="setting-item">
            <label htmlFor="focusTime">집중 시간 (분)</label>
            <input
              type="range"
              id="focusTime"
              min="1"
              max="60"
              step="1"
              value={settings.focusTime}
              onChange={(e) => setSettings({ ...settings, focusTime: Number(e.target.value) })}
            />
            <span className="setting-value">{settings.focusTime}분</span>
          </div>

          <div className="setting-item">
            <label htmlFor="shortBreakTime">짧은 휴식 (분)</label>
            <input
              type="range"
              id="shortBreakTime"
              min="3"
              max="10"
              step="1"
              value={settings.shortBreakTime}
              onChange={(e) => setSettings({ ...settings, shortBreakTime: Number(e.target.value) })}
            />
            <span className="setting-value">{settings.shortBreakTime}분</span>
          </div>

          <div className="setting-item">
            <label htmlFor="longBreakTime">긴 휴식 (분)</label>
            <input
              type="range"
              id="longBreakTime"
              min="10"
              max="30"
              step="5"
              value={settings.longBreakTime}
              onChange={(e) => setSettings({ ...settings, longBreakTime: Number(e.target.value) })}
            />
            <span className="setting-value">{settings.longBreakTime}분</span>
          </div>

          <div className="setting-item">
            <label htmlFor="pomodoroCount">뽀모도로 사이클</label>
            <input
              type="range"
              id="pomodoroCount"
              min="2"
              max="6"
              step="1"
              value={settings.pomodoroCount}
              onChange={(e) => setSettings({ ...settings, pomodoroCount: Number(e.target.value) })}
            />
            <span className="setting-value">{settings.pomodoroCount}회</span>
          </div>
        </div>

        <div className="settings-footer">
          <button onClick={handleSave} className="save-button">
            저장
          </button>
          <button onClick={onClose} className="cancel-button">
            취소
          </button>
        </div>
      </div>
    </div>
  );
}; 