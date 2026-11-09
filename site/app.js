'use strict';

const toggle = document.querySelector('#demo-toggle');
const note = document.querySelector('#demo-note');

if (toggle && note) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    note.hidden = open;
  });
}
