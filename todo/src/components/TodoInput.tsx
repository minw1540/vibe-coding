import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useTodoStore } from '@/store/todo-store';

export function TodoInput() {
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const { categories, addTodo } = useTodoStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !categoryId) return;
    
    addTodo(content.trim(), categoryId);
    setContent('');
    setCategoryId('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
      <Input
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="새로운 할 일을 입력하세요..."
        className="flex-1"
      />
      <Select value={categoryId} onValueChange={setCategoryId}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="카테고리 선택" />
        </SelectTrigger>
        <SelectContent>
          {categories.map((category) => (
            <SelectItem key={category.id} value={category.id}>
              {category.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Button type="submit" disabled={!content.trim() || !categoryId}>
        추가
      </Button>
    </form>
  );
} 