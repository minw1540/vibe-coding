import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoInput } from '../TodoInput';
import { useTodoStore } from '@/store/todo-store';

// Mock the Radix UI Select component
vi.mock('@/components/ui/select', () => ({
  Select: ({ children, onValueChange }: { children: React.ReactNode; onValueChange: (value: string) => void }) => (
    <div onClick={() => onValueChange('work')}>{children}</div>
  ),
  SelectTrigger: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  SelectContent: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  SelectItem: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  SelectValue: ({ placeholder }: { placeholder: string }) => <div>{placeholder}</div>,
}));

// Mock the store
vi.mock('@/store/todo-store', () => ({
  useTodoStore: vi.fn(() => ({
    categories: [
      { id: 'work', name: '업무' },
      { id: 'personal', name: '개인' },
    ],
    addTodo: vi.fn(),
  })),
}));

describe('TodoInput', () => {
  it('renders input field and category select', () => {
    render(<TodoInput />);
    
    expect(screen.getByPlaceholderText('새로운 할 일을 입력하세요...')).toBeInTheDocument();
    expect(screen.getByText('카테고리 선택')).toBeInTheDocument();
  });

  it('disables submit button when input is empty or category is not selected', () => {
    render(<TodoInput />);
    
    const submitButton = screen.getByText('추가');
    expect(submitButton).toBeDisabled();
  });

  it('calls addTodo when form is submitted with valid input', async () => {
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    const addTodo = vi.fn();
    mockStore.mockImplementation(() => ({
      categories: [{ id: 'work', name: '업무' }],
      addTodo,
    }));

    render(<TodoInput />);
    
    const input = screen.getByPlaceholderText('새로운 할 일을 입력하세요...');
    fireEvent.change(input, { target: { value: '새로운 할 일' } });
    
    // Select 컴포넌트를 클릭하면 mocked onValueChange가 호출됨
    const selectComponent = screen.getByText('카테고리 선택').parentElement;
    fireEvent.click(selectComponent!);
    
    const submitButton = screen.getByText('추가');
    fireEvent.click(submitButton);
    
    expect(addTodo).toHaveBeenCalledWith('새로운 할 일', 'work');
  });
}); 