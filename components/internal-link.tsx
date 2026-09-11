import type { AnchorHTMLAttributes } from 'react';

type InternalLinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  href: string;
};

/**
 * Use a document navigation for public routes.
 *
 * The current Vinext client router throws while installing RSC prefetch
 * handlers in production. A native anchor keeps every public route usable
 * while preserving normal browser history, accessibility, and link behavior.
 */
export default function InternalLink({ href, ...props }: InternalLinkProps) {
  return <a href={href} {...props} />;
}
