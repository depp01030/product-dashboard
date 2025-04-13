// 📁 static/js/utils/resizable-layout.js

export function initResizable(container) {
  const left = container.querySelector('.resizable-left');
  const right = container.querySelector('.resizable-right');
  const splitter = container.querySelector('.resizable-splitter');
  
  if (!left || !right || !splitter) return;

  let isResizing = false;
  let startX, startWidth;

  splitter.addEventListener('mousedown', e => {
    isResizing = true;
    startX = e.pageX;
    startWidth = left.offsetWidth;
    
    // 防止拖曳時選取文字
    document.body.classList.add('user-select-none');
    splitter.classList.add('dragging');
  });

  document.addEventListener('mousemove', e => {
    if (!isResizing) return;

    const width = startWidth + (e.pageX - startX);
    const containerWidth = container.offsetWidth;
    
    // 計算百分比並應用限制
    const percentage = Math.min(Math.max(
      (width / containerWidth) * 100,
      30  // 最小 30%
    ), 85); // 最大 85%
    
    left.style.flexBasis = `${percentage}%`;
    
    // 儲存當前寬度到 localStorage
    localStorage.setItem('productCardLeftWidth', percentage);
  });

  document.addEventListener('mouseup', () => {
    if (!isResizing) return;
    
    isResizing = false;
    document.body.classList.remove('user-select-none');
    splitter.classList.remove('dragging');
  });

  // 載入上次儲存的寬度
  const savedWidth = localStorage.getItem('productCardLeftWidth');
  if (savedWidth) {
    left.style.flexBasis = `${savedWidth}%`;
  }
}