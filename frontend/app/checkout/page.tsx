'use client';

import { useState } from 'react';
import { useCart } from '@/context/CartContext';
import { Truck, CreditCard } from 'lucide-react';

export default function CheckoutPage() {
  const { cart, totalAmount } = useCart();
  const [step, setStep] = useState(1);
  const [shippingMethod, setShippingMethod] = useState('standard');

  if (cart.length === 0) {
    return <div className="container mx-auto py-20 text-center">আপনার কার্ট খালি</div>;
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold font-bengali mb-8 text-center">চেকআউট</h1>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Forms */}
        <div className="lg:col-span-8 space-y-6">

          {/* Step 1: Address */}
          <div className={`bg-white p-6 rounded-xl border ${step === 1 ? 'border-primary ring-1 ring-primary/20' : 'border-gray-100'}`}>
            <h2 className="text-lg font-bold font-bengali mb-4 flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center text-sm">1</span>
              শিপিং তথ্য
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input type="text" placeholder="আপনার নাম" className="border p-3 rounded-lg w-full focus:outline-none focus:border-primary" />
              <input type="text" placeholder="মোবাইল নাম্বার" className="border p-3 rounded-lg w-full focus:outline-none focus:border-primary" />
              <textarea placeholder="সম্পূর্ণ ঠিকানা (বাসা নং, রোড নং...)" className="border p-3 rounded-lg w-full md:col-span-2 focus:outline-none focus:border-primary" rows={2}></textarea>

              <select className="border p-3 rounded-lg w-full bg-white">
                <option>বিভাগ নির্বাচন করুন</option>
                <option>ঢাকা</option>
                <option>চট্টগ্রাম</option>
              </select>
              <select className="border p-3 rounded-lg w-full bg-white">
                <option>জেলা নির্বাচন করুন</option>
              </select>
              <select className="border p-3 rounded-lg w-full bg-white">
                <option>থানা নির্বাচন করুন</option>
              </select>
            </div>
          </div>

          {/* Step 2: Payment */}
          <div className={`bg-white p-6 rounded-xl border ${step === 2 ? 'border-primary ring-1 ring-primary/20' : 'border-gray-100'}`}>
            <h2 className="text-lg font-bold font-bengali mb-4 flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center text-sm">2</span>
              পেমেন্ট মেথড
            </h2>

            <div className="space-y-3">
              <label className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input type="radio" name="payment" className="text-primary focus:ring-primary" defaultChecked />
                <div className="flex-1">
                  <span className="font-bold block">ক্যাশ অন ডেলিভারি</span>
                  <span className="text-xs text-gray-500">পণ্য হাতে পেয়ে মূল্য পরিশোধ</span>
                </div>
                <Truck className="text-gray-400" />
              </label>

              <label className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input type="radio" name="payment" className="text-primary focus:ring-primary" />
                <div className="flex-1">
                  <span className="font-bold block">বিকাশ / নগদ (Send Money)</span>
                  <span className="text-xs text-gray-500">ম্যানুয়াল ভেরিফিকেশন</span>
                </div>
                <CreditCard className="text-gray-400" />
              </label>
            </div>
          </div>

        </div>

        {/* Right Column: Order Summary */}
        <div className="lg:col-span-4">
          <div className="bg-white p-6 rounded-xl border border-gray-100 sticky top-24">
            <h3 className="font-bold text-lg mb-4 font-bengali">অর্ডার সামারি</h3>

            <div className="space-y-3 mb-6 max-h-60 overflow-y-auto">
              {cart.map(item => (
                <div key={item.id} className="flex justify-between text-sm">
                  <span>{item.title} <span className="text-gray-400">x {item.quantity}</span></span>
                  <span className="font-medium">৳{item.price * item.quantity}</span>
                </div>
              ))}
            </div>

            <div className="space-y-2 border-t pt-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">সাবটোটাল</span>
                <span>৳{totalAmount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">ডেলিভারি চার্জ</span>
                <span>৳{shippingMethod === 'standard' ? 60 : 100}</span>
              </div>
              <div className="flex justify-between text-lg font-bold pt-2 border-t text-primary">
                <span>সর্বমোট</span>
                <span>৳{totalAmount + (shippingMethod === 'standard' ? 60 : 100)}</span>
              </div>
            </div>

            <button className="w-full bg-primary text-white py-3 rounded-lg font-bold mt-6 hover:bg-primary/90 transition-colors">
              অর্ডার কনফার্ম করুন
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
