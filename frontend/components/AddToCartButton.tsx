'use client';

import { ShoppingCart } from 'lucide-react';
import { useCart } from '@/context/CartContext';

interface Book {
  id: number;
  title: string;
  slug: string;
  price: number;
  cover_image: string;
}

export default function AddToCartButton({ book }: { book: Book }) {
  const { addToCart } = useCart();

  const handleAddToCart = () => {
    addToCart({
      id: book.id,
      title: book.title,
      slug: book.slug,
      price: book.price,
      cover_image: book.cover_image,
      quantity: 1
    });
    alert('বইটি কার্টে যুক্ত করা হয়েছে!');
  };

  return (
    <button
      onClick={handleAddToCart}
      className="flex-1 bg-primary text-white py-3 rounded-lg font-bold hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
    >
      <ShoppingCart className="w-5 h-5" />
      কার্টে যোগ করুন
    </button>
  );
}
