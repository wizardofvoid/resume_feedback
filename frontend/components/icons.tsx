type IconProps = React.SVGProps<SVGSVGElement>;

export function UploadIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4.5A1.5 1.5 0 006.5 20h11a1.5 1.5 0 001.5-1.5V14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function FileIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M7 3.75h6.5L18 8.25v12H7v-16.5z" stroke="currentColor" strokeWidth="1.5" />
      <path d="M13.5 3.75v4.5H18M9.5 12h6M9.5 15h6" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

export function ArrowIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M5 12h13M13 7l5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function CloseIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export function MoonIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M20 15.1A8.5 8.5 0 018.9 4a8.5 8.5 0 1011.1 11.1z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
    </svg>
  );
}

export function SunIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <circle cx="12" cy="12" r="3.5" stroke="currentColor" strokeWidth="1.5" />
      <path d="M12 2v2.2M12 19.8V22M4.93 4.93l1.56 1.56m11.02 11.02l1.56 1.56M2 12h2.2M19.8 12H22M4.93 19.07l1.56-1.56M17.51 6.49l1.56-1.56" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export function CheckIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M5 12.5l4.25 4.25L19 7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function ShieldIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M12 3l7 3v5.4c0 4.5-2.8 7.7-7 9.6-4.2-1.9-7-5.1-7-9.6V6l7-3z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
      <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function EyeIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path d="M3 12s3.2-5 9-5 9 5 9 5-3.2 5-9 5-9-5-9-5z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
      <circle cx="12" cy="12" r="2.5" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}
