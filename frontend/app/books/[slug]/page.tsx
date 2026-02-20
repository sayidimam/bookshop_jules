import { getBookDetail } from '@/lib/api';
import Image from 'next/image';
import { ShoppingCart, Heart, Share2 } from 'lucide-react';
import { BookCard } from '@/components/BookCard';
import AddToCartButton from '@/components/AddToCartButton';

export default async function BookDetail({ params }: { params: { slug: string } }) {
  let book = null;
  try {
    book = await getBookDetail(params.slug);
  } catch (error) {
    return <div className="container mx-auto py-20 text-center">Book Not Found</div>;
  }

  const price = book.sale_price || book.regular_price;
  const discount = book.sale_price
    ? Math.round(((book.regular_price - book.sale_price) / book.regular_price) * 100)
    : 0;

  return (
    <main className="container mx-auto px-4 py-8">
      {/* Product Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 p-6 md:p-8">

          {/* Image Gallery */}
          <div className="md:col-span-4 relative aspect-[2/3] md:aspect-auto">
            <div className="relative w-full h-full min-h-[400px] rounded-lg overflow-hidden border bg-gray-50 group">
              {book.cover_image ? (
                <Image
                  src={book.cover_image}
                  alt={book.title}
                  fill
                  className="object-contain group-hover:scale-110 transition-transform duration-500"
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-400">No Image</div>
              )}
            </div>
          </div>

          {/* Product Info */}
          <div className="md:col-span-5 space-y-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold font-bengali text-gray-900 leading-tight mb-2">
                {book.title}
              </h1>
              <p className="text-gray-500 font-bengali">
                লেখক: <span className="text-primary font-medium cursor-pointer hover:underline">{book.authors.map((a:any) => a.name).join(', ')}</span>
              </p>
              <p className="text-gray-500 font-bengali">
                প্রকাশনী: <span className="text-primary font-medium cursor-pointer hover:underline">{book.publisher?.name}</span>
              </p>
            </div>

            <div className="flex items-end gap-3 pb-4 border-b border-gray-100">
              <span className="text-4xl font-bold text-primary font-sans">৳{price}</span>
              {book.sale_price && (
                <>
                  <span className="text-xl text-gray-400 line-through font-sans">৳{book.regular_price}</span>
                  <span className="bg-accent/10 text-accent px-2 py-1 rounded text-sm font-bold">
                    {discount}% ছাড়
                  </span>
                </>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 bg-gray-50 p-4 rounded-lg font-bengali">
              <div>
                <span className="block text-gray-400 text-xs mb-1">ক্যাটাগরি</span>
                <span className="font-medium">{book.categories.map((c:any) => c.name).join(', ')}</span>
              </div>
              <div>
                <span className="block text-gray-400 text-xs mb-1">এডিশন</span>
                <span className="font-medium">{book.edition || 'N/A'}</span>
              </div>
              <div>
                <span className="block text-gray-400 text-xs mb-1">পৃষ্ঠা</span>
                <span className="font-medium font-sans">{book.page_count || 'N/A'}</span>
              </div>
              <div>
                <span className="block text-gray-400 text-xs mb-1">ভাষা</span>
                <span className="font-medium">{book.language}</span>
              </div>
            </div>

            <p className="text-gray-600 leading-relaxed font-bengali text-sm md:text-base">
              {book.description?.substring(0, 300)}...
            </p>

            <div className="flex gap-4 pt-4">
              <AddToCartButton
                book={{
                  id: book.id,
                  title: book.title,
                  slug: book.slug,
                  price: price,
                  cover_image: book.cover_image
                }}
              />
              <button className="p-3 border border-gray-200 rounded-lg hover:border-primary hover:text-primary transition-colors">
                <Heart className="w-5 h-5" />
              </button>
              <button className="p-3 border border-gray-200 rounded-lg hover:border-primary hover:text-primary transition-colors">
                <Share2 className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Delivery & Assurance */}
          <div className="md:col-span-3 space-y-4">
            <div className="border border-gray-100 rounded-lg p-4 bg-gray-50/50 space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm text-primary">🚚</div>
                <div>
                  <h4 className="font-bold text-sm text-gray-900">দ্রুত ডেলিভারি</h4>
                  <p className="text-xs text-gray-500">সমগ্র বাংলাদেশে হোম ডেলিভারি</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm text-primary">💰</div>
                <div>
                  <h4 className="font-bold text-sm text-gray-900">ক্যাশ অন ডেলিভারি</h4>
                  <p className="text-xs text-gray-500">পণ্য হাতে পেয়ে মূল্য পরিশোধ</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm text-primary">🔄</div>
                <div>
                  <h4 className="font-bold text-sm text-gray-900">হ্যাপি রিটার্ন</h4>
                  <p className="text-xs text-gray-500">৭ দিনের মধ্যে ফেরত দেওয়ার সুবিধা</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Related Books */}
      {book.related_books && book.related_books.length > 0 && (
        <section className="mt-12">
          <h2 className="text-2xl font-bold font-bengali mb-6 border-l-4 border-primary pl-3">
            রিলেটেড বই
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
            {book.related_books.map((related: any) => (
              <BookCard key={related.id} book={related} />
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
