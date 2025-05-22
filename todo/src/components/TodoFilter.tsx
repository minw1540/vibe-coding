import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useTodoStore } from '@/store/todo-store';

export function TodoFilter() {
  const { categories, filter, setFilter } = useTodoStore();

  return (
    <div className="flex gap-2 mb-4">
      <div className="flex gap-2">
        <Button
          variant={filter.status === 'all' ? 'default' : 'outline'}
          onClick={() => setFilter({ status: 'all' })}
        >
          전체
        </Button>
        <Button
          variant={filter.status === 'active' ? 'default' : 'outline'}
          onClick={() => setFilter({ status: 'active' })}
        >
          미완료
        </Button>
        <Button
          variant={filter.status === 'completed' ? 'default' : 'outline'}
          onClick={() => setFilter({ status: 'completed' })}
        >
          완료
        </Button>
      </div>

      <Select
        value={filter.categoryId ?? 'all'}
        onValueChange={(value) => setFilter({ categoryId: value === 'all' ? null : value })}
      >
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="모든 카테고리" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">모든 카테고리</SelectItem>
          {categories.map((category) => (
            <SelectItem key={category.id} value={category.id}>
              {category.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Input
        value={filter.search}
        onChange={(e) => setFilter({ search: e.target.value })}
        placeholder="검색..."
        className="flex-1"
      />
    </div>
  );
} 