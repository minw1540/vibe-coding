import { useMemo } from 'react';
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { useTodoStore } from '@/store/todo-store';
import { Trash2 } from 'lucide-react';
import { Todo } from '@/types/todo';

function TodoItem({ todo }: { todo: Todo }) {
  const { categories, toggleTodo, deleteTodo } = useTodoStore();
  const category = categories.find((c) => c.id === todo.categoryId);

  return (
    <Card className="p-4 mb-2">
      <div className="flex items-center gap-2">
        <Checkbox
          checked={todo.completed}
          onCheckedChange={() => toggleTodo(todo.id)}
        />
        <span
          className={`flex-1 ${
            todo.completed ? 'line-through text-muted-foreground' : ''
          }`}
        >
          {todo.content}
        </span>
        <span className="text-sm text-muted-foreground">{category?.name}</span>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => deleteTodo(todo.id)}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
}

export function TodoList() {
  const { todos, filter } = useTodoStore();

  const filteredTodos = useMemo(() => {
    return todos
      .filter((todo) => {
        if (filter.status === 'completed') return todo.completed;
        if (filter.status === 'active') return !todo.completed;
        return true;
      })
      .filter((todo) => {
        if (filter.categoryId) return todo.categoryId === filter.categoryId;
        return true;
      })
      .filter((todo) => {
        if (filter.search) {
          return todo.content
            .toLowerCase()
            .includes(filter.search.toLowerCase());
        }
        return true;
      })
      .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }, [todos, filter]);

  const stats = useMemo(() => {
    const total = todos.length;
    const completed = todos.filter((todo) => todo.completed).length;
    return { total, completed, remaining: total - completed };
  }, [todos]);

  return (
    <div>
      <div className="text-sm text-muted-foreground mb-4">
        전체: {stats.total}개 | 완료: {stats.completed}개 | 남은 할 일:{' '}
        {stats.remaining}개
      </div>
      <div>
        {filteredTodos.map((todo) => (
          <TodoItem key={todo.id} todo={todo} />
        ))}
        {filteredTodos.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            할 일이 없습니다.
          </div>
        )}
      </div>
    </div>
  );
} 