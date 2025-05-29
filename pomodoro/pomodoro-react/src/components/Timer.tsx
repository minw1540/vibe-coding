import { useState, useEffect, useCallback } from 'react';
import { Play, Pause, RefreshCw, Settings } from 'lucide-react';
import type { TimerSettings } from '../types/timer';
import '../styles/Timer.css';

type TimerPhase = 'focus' | 'shortBreak' | 'longBreak';

interface TimerProps {
  onSettingsClick: () => void;
  settings: TimerSettings;
}

declare global {
  interface Window {
    webkitAudioContext: typeof AudioContext;
  }
}

export const Timer = ({ onSettingsClick, settings }: TimerProps) => {
  const [phase, setPhase] = useState<TimerPhase>('focus');
  const [timeLeft, setTimeLeft] = useState(settings.focusTime * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [pomodorosCompleted, setPomodorosCompleted] = useState(0);
  const [currentCycle, setCurrentCycle] = useState(1);

  // 알림음 재생 함수
  const playNotification = useCallback(() => {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    const audioContext = new AudioContextClass();
    
    // 알림음 생성
    const createBeep = (frequency: number, duration: number) => {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.type = 'sine';
      oscillator.frequency.value = frequency;
      
      gainNode.gain.setValueAtTime(0, audioContext.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.5, audioContext.currentTime + 0.01);
      gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + duration);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + duration);
    };

    // 두 번의 비프음 재생 (높은음 -> 낮은음)
    createBeep(880, 0.15); // A5 음
    setTimeout(() => createBeep(587.33, 0.15), 200); // D5 음
  }, []);

  // 설정이 변경될 때마다 타이머 시간 업데이트
  useEffect(() => {
    setIsRunning(false);
    if (phase === 'focus') {
      setTimeLeft(settings.focusTime * 60);
    } else if (phase === 'shortBreak') {
      setTimeLeft(settings.shortBreakTime * 60);
    } else {
      setTimeLeft(settings.longBreakTime * 60);
    }
  }, [settings, phase]);

  useEffect(() => {
    let interval: number | undefined;

    if (isRunning && timeLeft > 0) {
      interval = window.setInterval(() => {
        setTimeLeft((time) => time - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      playNotification();
      handlePhaseComplete();
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning, timeLeft, playNotification]);

  const handlePhaseComplete = () => {
    if (phase === 'focus') {
      setPomodorosCompleted((prev) => prev + 1);
      if (currentCycle === settings.pomodoroCount) {
        setPhase('longBreak');
        setTimeLeft(settings.longBreakTime * 60);
        setCurrentCycle(1);
      } else {
        setPhase('shortBreak');
        setTimeLeft(settings.shortBreakTime * 60);
        setCurrentCycle((prev) => prev + 1);
      }
    } else {
      setPhase('focus');
      setTimeLeft(settings.focusTime * 60);
    }
    setIsRunning(false);
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    if (phase === 'focus') {
      setTimeLeft(settings.focusTime * 60);
    } else if (phase === 'shortBreak') {
      setTimeLeft(settings.shortBreakTime * 60);
    } else {
      setTimeLeft(settings.longBreakTime * 60);
    }
  };

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const calculateProgress = (): number => {
    const totalTime = phase === 'focus' 
      ? settings.focusTime * 60 
      : phase === 'shortBreak' 
        ? settings.shortBreakTime * 60 
        : settings.longBreakTime * 60;
    return ((totalTime - timeLeft) / totalTime) * 100;
  };

  return (
    <div className="timer-container" data-phase={phase}>
      <div className="timer-header">
        <span className="phase-label">{phase === 'focus' ? '집중 시간' : phase === 'shortBreak' ? '짧은 휴식' : '긴 휴식'}</span>
        <span className="cycle-label">#{currentCycle}/{settings.pomodoroCount}</span>
      </div>

      <div className="timer-display">
        <div className="progress-ring" style={{ '--progress': `${calculateProgress()}%` } as React.CSSProperties}>
          <div className="time-text">{formatTime(timeLeft)}</div>
        </div>
      </div>

      <div className="timer-controls">
        <button onClick={toggleTimer} className="control-button">
          {isRunning ? <Pause size={24} /> : <Play size={24} />}
        </button>
        <button onClick={resetTimer} className="control-button">
          <RefreshCw size={24} />
        </button>
        <button onClick={onSettingsClick} className="control-button">
          <Settings size={24} />
        </button>
      </div>

      <div className="timer-stats">
        <span>오늘 완료: {pomodorosCompleted}개</span>
      </div>
    </div>
  );
}; 