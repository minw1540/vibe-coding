import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoFilter } from '../TodoFilter';
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

vi.mock('@/store/todo-store', () => ({
  useTodoStore: vi.fn(() => ({
    categories: [
      { id: 'work', name: '업무' },
      { id: 'personal', name: '개인' },
    ],
    filter: {
      status: 'all',
      categoryId: null,
      search: '',
    },
    setFilter: vi.fn(),
  })),
}));

describe('TodoFilter', () => {
  it('renders filter buttons and search input', () => {
    render(<TodoFilter />);
    
    expect(screen.getByText('전체')).toBeInTheDocument();
    expect(screen.getByText('미완료')).toBeInTheDocument();
    expect(screen.getByText('완료')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('검색...')).toBeInTheDocument();
    expect(screen.getByText('모든 카테고리')).toBeInTheDocument();
  });

  it('calls setFilter with correct status when filter buttons are clicked', () => {
    const setFilter = vi.fn();
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      categories: [{ id: 'work', name: '업무' }],
      filter: { status: 'all', categoryId: null, search: '' },
      setFilter,
    }));

    render(<TodoFilter />);
    
    fireEvent.click(screen.getByText('미완료'));
    expect(setFilter).toHaveBeenCalledWith({ status: 'active' });
    
    fireEvent.click(screen.getByText('완료'));
    expect(setFilter).toHaveBeenCalledWith({ status: 'completed' });
  });

  it('calls setFilter with search text when search input changes', () => {
    const setFilter = vi.fn();
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      categories: [{ id: 'work', name: '업무' }],
      filter: { status: 'all', categoryId: null, search: '' },
      setFilter,
    }));

    render(<TodoFilter />);
    
    const searchInput = screen.getByPlaceholderText('검색...');
    fireEvent.change(searchInput, { target: { value: '테스트' } });
    
    expect(setFilter).toHaveBeenCalledWith({ search: '테스트' });
  });

  it('calls setFilter with category when category is selected', () => {
    const setFilter = vi.fn();
    const mockStore = useTodoStore as unknown as ReturnType<typeof vi.fn>;
    mockStore.mockImplementation(() => ({
      categories: [{ id: 'work', name: '업무' }],
      filter: { status: 'all', categoryId: null, search: '' },
      setFilter,
    }));

    render(<TodoFilter />);
    
    // Select 컴포넌트를 클릭하면 mocked onValueChange가 호출됨
    const selectComponent = screen.getByText('모든 카테고리').parentElement;
    fireEvent.click(selectComponent!);
    
    expect(setFilter).toHaveBeenCalledWith({ categoryId: 'work' });
  });
}); 