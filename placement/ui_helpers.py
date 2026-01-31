def get_svg_sticker():
    return '''
    <div style="position: relative;">
      <div style="
          position: absolute;
          right: 18px;
          bottom: 18px;
          width: 110px;
          opacity: 0.95;
          transform: rotate(-6deg);
          pointer-events: none;
          ">
        <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
          <g fill="none" stroke="none">
            <rect x="14" y="18" width="36" height="30" rx="8" fill="#EFF6FF"/>
            <rect x="26" y="6" width="12" height="8" rx="3" fill="#BFDBFE"/>
            <circle cx="26" cy="33" r="3" fill="#60A5FA"/>
            <circle cx="38" cy="33" r="3" fill="#60A5FA"/>
            <path d="M22 44c4 2 16 2 20 0" stroke="#2563EB" stroke-width="1.5" stroke-linecap="round" fill="none"/>
          </g>
        </svg>
      </div>
    </div>
    '''
