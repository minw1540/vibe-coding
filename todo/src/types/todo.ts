export type Category = {
  id: string;
  name: string;
};

export type Todo = {
  id: string;
  content: string;
  completed: boolean;
  categoryId: string;
  createdAt: Date;
}; 