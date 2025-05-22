import { TodoInput } from '@/components/TodoInput';
import { TodoFilter } from '@/components/TodoFilter';
import { TodoList } from '@/components/TodoList';

function App() {
  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container max-w-2xl">
        <h1 className="text-4xl font-bold mb-8">SimpleTodo</h1>
        <TodoInput />
        <TodoFilter />
        <TodoList />
      </div>
    </div>
  );
}

export default App;
