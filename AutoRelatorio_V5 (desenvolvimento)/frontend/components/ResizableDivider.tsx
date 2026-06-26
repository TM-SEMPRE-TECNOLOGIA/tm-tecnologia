'use client';

import { useEffect, useRef } from 'react';

interface ResizableDividerProps {
  onResize?: (width: number) => void;
}

export function ResizableDivider({ onResize }: ResizableDividerProps) {
  const dividerRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<HTMLElement | null>(null);
  const appRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const divider = dividerRef.current;
    if (!divider) return;

    editorRef.current = document.querySelector('.editor');
    appRef.current = document.querySelector('.app-layout');

    let isResizing = false;
    let startX = 0;
    let startWidth = 380;

    const handleMouseDown = (e: MouseEvent) => {
      isResizing = true;
      startX = e.clientX;
      startWidth = editorRef.current?.offsetWidth || 380;
      divider.classList.add('active');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    };

    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing || !editorRef.current || !appRef.current) return;
      const delta = e.clientX - startX;
      const newWidth = Math.max(300, Math.min(startWidth + delta, appRef.current.offsetWidth - 300));
      editorRef.current.style.width = newWidth + 'px';
      onResize?.(newWidth);
    };

    const handleMouseUp = () => {
      isResizing = false;
      divider.classList.remove('active');
      document.body.style.cursor = 'default';
      document.body.style.userSelect = 'auto';
    };

    divider.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      divider.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [onResize]);

  return <div className="resizable-divider" ref={dividerRef}></div>;
}
