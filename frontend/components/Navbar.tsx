'use client';

import Link from 'next/link';
import { ShoppingCart, User, Search, Menu } from 'lucide-react';
import { useState } from 'react';

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl font-bold font-bengali text-primary">বুকশপ</span>
        </Link>

        {/* Desktop Search */}
        <div className="hidden md:flex flex-1 max-w-xl mx-8">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="বই, লেখক বা প্রকাশনী খুঁজুন..."
              className="w-full pl-4 pr-10 py-2 rounded-full border border-gray-200 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 bg-secondary/30 transition-all font-bengali"
            />
            <button className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary">
              <Search className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4 md:gap-6">
          <Link href="/cart" className="relative group">
            <div className="p-2 rounded-full hover:bg-secondary transition-colors">
              <ShoppingCart className="w-6 h-6 text-gray-700 group-hover:text-primary" />
              <span className="absolute -top-1 -right-1 bg-accent text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full border-2 border-white">
                0
              </span>
            </div>
          </Link>

          <Link href="/login" className="hidden md:flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-primary transition-colors">
            <User className="w-5 h-5" />
            <span>লগইন</span>
          </Link>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 text-gray-700"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>
      </div>

      {/* Mobile Search & Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t p-4 space-y-4 bg-white">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="বই খুঁজুন..."
              className="w-full pl-4 pr-10 py-2 rounded-lg border border-gray-200"
            />
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <div className="flex flex-col gap-2">
            <Link href="/login" className="py-2 text-gray-700 font-medium border-b">লগইন করুন</Link>
            <Link href="/order-track" className="py-2 text-gray-700 font-medium">অর্ডার ট্র্যাক</Link>
          </div>
        </div>
      )}
    </nav>
  );
}
