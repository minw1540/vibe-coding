import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Todo, Category } from '@/types/todo';

interface TodoState {
  todos: Todo[];
  categories: Category[];
  filter: {
    status: 'all' | 'completed' | 'active';
    categoryId: string | null;
    search: string;
  };
  addTodo: (content: string, categoryId: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
  editTodo: (id: string, content: string) => void;
  addCategory: (name: string) => void;
  deleteCategory: (id: string) => void;
  setFilter: (filter: Partial<TodoState['filter']>) => void;
}

const defaultCategories: Category[] = [
  { id: 'work', name: '업무' },
  { id: 'personal', name: '개인' },
  { id: 'shopping', name: '쇼핑' },
  { id: 'etc', name: '기타' },
];

export const useTodoStore = create<TodoState>()(
  persist(
    (set) => ({
      todos: [],
      categories: defaultCategories,
      filter: {
        status: 'all',
        categoryId: null,
        search: '',
      },
      addTodo: (content, categoryId) =>
        set((state) => ({
          todos: [
            ...state.todos,
            {
              id: crypto.randomUUID(),
              content,
              completed: false,
              categoryId,
              createdAt: new Date(),
            },
          ],
        })),
      toggleTodo: (id) =>
        set((state) => ({
          todos: state.todos.map((todo) =>
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
          ),
        })),
      deleteTodo: (id) =>
        set((state) => ({
          todos: state.todos.filter((todo) => todo.id !== id),
        })),
      editTodo: (id, content) =>
        set((state) => ({
          todos: state.todos.map((todo) =>
            todo.id === id ? { ...todo, content } : todo
          ),
        })),
      addCategory: (name) =>
        set((state) => ({
          categories: [
            ...state.categories,
            { id: crypto.randomUUID(), name },
          ],
        })),
      deleteCategory: (id) =>
        set((state) => ({
          categories: state.categories.filter((category) => category.id !== id),
          todos: state.todos.filter((todo) => todo.categoryId !== id),
        })),
      setFilter: (filter) =>
        set((state) => ({
          filter: { ...state.filter, ...filter },
        })),
    }),
    {
      name: 'todo-storage',
    }
  )
); 