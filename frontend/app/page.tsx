import { getBooks } from '@/lib/api';
import { BookCard } from '@/components/BookCard';

export default async function Home() {
  let books = [];
  try {
    const data = await getBooks();
    books = data.results || [];
  } catch (e) {
    console.error("Failed to fetch books:", e);
  }

  return (
    <main className="min-h-screen">
      {/* Header Placeholder */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-primary">বুকশপ</h1>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="বই খুঁজুন..."
              className="border rounded-full px-4 py-2 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-primary/5 py-12">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold font-bengali text-primary mb-4">জ্ঞানই শক্তি, বইই আলো</h2>
          <p className="text-gray-600 mb-8">আপনার পছন্দের ইসলামিক এবং একাডেমিক বইয়ের বিশাল সমাহার</p>
        </div>
      </section>

      {/* Book Grid */}
      <section className="container mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold font-bengali mb-6 border-l-4 border-primary pl-3">
          নতুন কালেকশন
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {books.map((book: any) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      </section>
    </main>
  );
}
