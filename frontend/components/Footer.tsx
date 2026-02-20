import Link from 'next/link';
import { Facebook, Instagram, Twitter } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-100 pt-16 pb-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          {/* Brand */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold font-bengali text-primary">বুকশপ</h3>
            <p className="text-gray-500 text-sm leading-relaxed">
              বাংলাদেশের অন্যতম নির্ভরযোগ্য অনলাইন বুকশপ। আমরা পৌঁছে দিচ্ছি জ্ঞান ও প্রজ্ঞা আপনার দোরগোড়ায়।
            </p>
            <div className="flex gap-4">
              <Link href="#" className="text-gray-400 hover:text-primary transition-colors"><Facebook className="w-5 h-5" /></Link>
              <Link href="#" className="text-gray-400 hover:text-primary transition-colors"><Instagram className="w-5 h-5" /></Link>
              <Link href="#" className="text-gray-400 hover:text-primary transition-colors"><Twitter className="w-5 h-5" /></Link>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold text-gray-900 mb-6 font-bengali">শর্টকাট লিংক</h4>
            <ul className="space-y-3 text-sm text-gray-500 font-bengali">
              <li><Link href="/books" className="hover:text-primary">সকল বই</Link></li>
              <li><Link href="/authors" className="hover:text-primary">লেখকবৃন্দ</Link></li>
              <li><Link href="/publishers" className="hover:text-primary">প্রকাশনী</Link></li>
              <li><Link href="/pre-order" className="hover:text-primary">প্রি-অর্ডার</Link></li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="font-bold text-gray-900 mb-6 font-bengali">কাস্টমার সেবা</h4>
            <ul className="space-y-3 text-sm text-gray-500 font-bengali">
              <li><Link href="/contact" className="hover:text-primary">যোগাযোগ করুন</Link></li>
              <li><Link href="/shipping-policy" className="hover:text-primary">ডেলিভারি পলিসি</Link></li>
              <li><Link href="/return-policy" className="hover:text-primary">রিটার্ন পলিসি</Link></li>
              <li><Link href="/faq" className="hover:text-primary">প্রশ্নোত্তর</Link></li>
            </ul>
          </div>

          {/* Newsletter (Optional) */}
          <div>
            <h4 className="font-bold text-gray-900 mb-6 font-bengali">পেমেন্ট মেথড</h4>
            <div className="flex flex-wrap gap-2">
               {/* Placeholders for logos */}
               <div className="w-12 h-8 bg-gray-100 rounded border"></div>
               <div className="w-12 h-8 bg-gray-100 rounded border"></div>
               <div className="w-12 h-8 bg-gray-100 rounded border"></div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-100 pt-8 text-center text-sm text-gray-400 font-bengali">
          <p>&copy; {new Date().getFullYear()} বুকশপ ডট কম। সর্বস্বত্ব সংরক্ষিত।</p>
        </div>
      </div>
    </footer>
  );
}
