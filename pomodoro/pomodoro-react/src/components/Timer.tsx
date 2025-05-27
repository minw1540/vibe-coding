import { useState, useEffect } from 'react';
import { Play, Pause, RefreshCw, Settings } from 'lucide-react';
import '../styles/Timer.css';

type TimerPhase = 'focus' | 'shortBreak' | 'longBreak';

interface TimerProps {
  onSettingsClick: () => void;
}

export const Timer = ({ onSettingsClick }: TimerProps) => {
  const [phase, setPhase] = useState<TimerPhase>('focus');
  const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minutes in seconds
  const [isRunning, setIsRunning] = useState(false);
  const [pomodorosCompleted, setPomodorosCompleted] = useState(0);
  const [currentCycle, setCurrentCycle] = useState(1);

  useEffect(() => {
    let interval: number | undefined;

    if (isRunning && timeLeft > 0) {
      interval = window.setInterval(() => {
        setTimeLeft((time) => time - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      handlePhaseComplete();
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning, timeLeft]);

  const handlePhaseComplete = () => {
    const audio = new Audio('/notification.mp3');
    audio.play();

    if (phase === 'focus') {
      setPomodorosCompleted((prev) => prev + 1);
      if (currentCycle === 4) {
        setPhase('longBreak');
        setTimeLeft(15 * 60); // 15 minutes
        setCurrentCycle(1);
      } else {
        setPhase('shortBreak');
        setTimeLeft(5 * 60); // 5 minutes
        setCurrentCycle((prev) => prev + 1);
      }
    } else {
      setPhase('focus');
      setTimeLeft(25 * 60); // 25 minutes
    }
    setIsRunning(false);
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    if (phase === 'focus') {
      setTimeLeft(25 * 60);
    } else if (phase === 'shortBreak') {
      setTimeLeft(5 * 60);
    } else {
      setTimeLeft(15 * 60);
    }
  };

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const calculateProgress = (): number => {
    const totalTime = phase === 'focus' ? 25 * 60 : phase === 'shortBreak' ? 5 * 60 : 15 * 60;
    return ((totalTime - timeLeft) / totalTime) * 100;
  };

  return (
    <div className="timer-container">
      <div className="timer-header">
        <span className="phase-label">{phase === 'focus' ? '집중 시간' : phase === 'shortBreak' ? '짧은 휴식' : '긴 휴식'}</span>
        <span className="cycle-label">#{currentCycle}/4</span>
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