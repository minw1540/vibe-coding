import { useState } from 'react'
import { Timer } from './components/Timer'
import { Settings } from './components/Settings'
import type { TimerSettings } from './types/timer'
import './App.css'

const defaultSettings: TimerSettings = {
  focusTime: 25,
  shortBreakTime: 5,
  longBreakTime: 15,
  pomodoroCount: 4,
}

function App() {
  const [showSettings, setShowSettings] = useState(false)
  const [settings, setSettings] = useState<TimerSettings>(defaultSettings)

  const handleSettingsSave = (newSettings: TimerSettings) => {
    setSettings(newSettings)
    setShowSettings(false)
  }

  return (
    <div className="app">
      <Timer 
        onSettingsClick={() => setShowSettings(true)} 
        settings={settings}
      />
      {showSettings && (
        <Settings
          onClose={() => setShowSettings(false)}
          onSave={handleSettingsSave}
          initialSettings={settings}
        />
      )}
    </div>
  )
}

export default App
