/**
 * Next.js App Component - Global App Configuration
 * 
 * Educational Note:
 * The _app.tsx file is the entry point for all pages in Next.js.
 * It's where we can add global styles, providers, and layout components.
 */

import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
