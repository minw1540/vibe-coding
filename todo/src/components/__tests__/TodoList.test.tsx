import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoList } from '../TodoList';
import { useTodoStore } from '@/store/todo-store';

vi.mock('@/store/todo-store', () => ({
  useTodoStore: vi.fn(),
}));

describe('TodoList', () => {
  const mockTodos = [
    {
      id: '1',
      content: '할 일 1',
      completed: false,
      categoryId: 'work',
      createdAt: new Date(),
    },
    {
      id: '2',
      content: '할 일 2',
      completed: true,
      categoryId: 'personal',
      createdAt: new Date(),
    },
  ];

  const mockCategories = [
    { id: 'work', name: '업무' },
    { id: 'personal', name: '개인' },
  ];

  beforeEach(() => {
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      todos: mockTodos,
      categories: mockCategories,
      filter: { status: 'all', categoryId: null, search: '' },
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
    }));
  });

  it('renders todo list with stats', () => {
    render(<TodoList />);
    
    expect(screen.getByText(/전체: 2개/)).toBeInTheDocument();
    expect(screen.getByText(/완료: 1개/)).toBeInTheDocument();
    expect(screen.getByText(/남은 할 일: 1개/)).toBeInTheDocument();
  });

  it('renders all todos', () => {
    render(<TodoList />);
    
    expect(screen.getByText('할 일 1')).toBeInTheDocument();
    expect(screen.getByText('할 일 2')).toBeInTheDocument();
  });

  it('calls toggleTodo when checkbox is clicked', () => {
    const toggleTodo = vi.fn();
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      todos: mockTodos,
      categories: mockCategories,
      filter: { status: 'all', categoryId: null, search: '' },
      toggleTodo,
      deleteTodo: vi.fn(),
    }));

    render(<TodoList />);
    
    const checkboxes = screen.getAllByRole('checkbox');
    fireEvent.click(checkboxes[0]);
    
    expect(toggleTodo).toHaveBeenCalledWith('1');
  });

  it('calls deleteTodo when delete button is clicked', () => {
    const deleteTodo = vi.fn();
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      todos: mockTodos,
      categories: mockCategories,
      filter: { status: 'all', categoryId: null, search: '' },
      toggleTodo: vi.fn(),
      deleteTodo,
    }));

    render(<TodoList />);
    
    const deleteButtons = screen.getAllByRole('button');
    fireEvent.click(deleteButtons[0]);
    
    expect(deleteTodo).toHaveBeenCalledWith('1');
  });
}); 