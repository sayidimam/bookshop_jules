import Image from 'next/image';
import Link from 'next/link';

interface BookCardProps {
  book: {
    title: string;
    slug: string;
    authors: { name: string }[];
    cover_image: string | null;
    sale_price: number | null;
    regular_price: number;
  };
}

export function BookCard({ book }: BookCardProps) {
  const price = book.sale_price || book.regular_price;
  const discount = book.sale_price
    ? Math.round(((book.regular_price - book.sale_price) / book.regular_price) * 100)
    : 0;

  return (
    <Link href={`/books/${book.slug}`} className="group block bg-white rounded-lg border border-gray-100 hover:shadow-lg transition-all duration-300">
      <div className="relative aspect-[2/3] overflow-hidden rounded-t-lg bg-gray-50">
        {book.cover_image ? (
          <Image
            src={book.cover_image}
            alt={book.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">No Image</div>
        )}
        {discount > 0 && (
          <span className="absolute top-2 left-2 bg-accent text-white text-xs font-bold px-2 py-1 rounded">
            {discount}% OFF
          </span>
        )}
      </div>
      <div className="p-3">
        <h3 className="font-bengali font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors">
          {book.title}
        </h3>
        <p className="text-gray-500 text-sm mt-1 line-clamp-1">
          {book.authors.map(a => a.name).join(', ')}
        </p>
        <div className="mt-3 flex items-baseline gap-2">
          <span className="text-primary font-bold text-lg">৳{price}</span>
          {book.sale_price && (
            <span className="text-gray-400 text-sm line-through">৳{book.regular_price}</span>
          )}
        </div>
      </div>
    </Link>
  );
}
