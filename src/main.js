import './style.css';
import { categories } from './menu.js';

const app = document.querySelector('#app');

app.innerHTML = `
  <div class="shell">
    <aside class="brand" aria-label="Chicken Boom">
      <p class="brand__menu" dir="ltr">menu</p>
      <p class="brand__sub">Restaurant &amp; Cafe</p>
      <img class="brand__logo" src="/logo.png" alt="Chicken Boom" width="220" height="220" />
      <p class="brand__tag">دجاج بنكهة قوية</p>
    </aside>

    <div class="content">
      <header class="mobile-top">
        <img src="/logo.png" alt="Chicken Boom" class="mobile-top__logo" width="128" height="128" />
        <p class="mobile-top__tag">دجاج بنكهة قوية</p>
      </header>

      <nav class="cats" id="cats" aria-label="تصنيفات المنيو">
        <div class="cats__track" role="tablist">
          ${categories
            .map(
              (cat, i) => `
            <button
              type="button"
              class="cats__btn${i === 0 ? ' is-active' : ''}"
              data-target="${cat.id}"
              role="tab"
              aria-selected="${i === 0}"
            >
              <span class="cats__icon" aria-hidden="true">${cat.icon}</span>
              <span>${cat.title}</span>
            </button>
          `,
            )
            .join('')}
        </div>
      </nav>

      <main class="menu">
        ${categories
          .map(
            (cat) => `
          <section class="section section--${cat.tone}" id="${cat.id}" data-section>
            <div class="section__inner">
              <div class="section__visual">
                <img class="section__photo" src="${cat.image}" alt="" width="220" height="220" loading="lazy" />
              </div>
              <div class="section__body">
                <header class="section__head">
                  <h2 class="section__title">
                    <span class="section__icon" aria-hidden="true">${cat.icon}</span>
                    ${cat.title}
                  </h2>
                  <span class="section__count">${cat.items.length} أصناف</span>
                </header>
                <ul class="list">
                  ${cat.items
                    .map(
                      (item) => `
                    <li class="item">
                      <div class="item__text">
                        <h3 class="item__name">${item.name}</h3>
                        ${item.desc ? `<p class="item__desc">${item.desc}</p>` : ''}
                      </div>
                      <div class="item__price" aria-label="السعر">
                        <span class="item__amount">${item.price}</span>
                        <span class="item__currency">ل.س</span>
                      </div>
                    </li>
                  `,
                    )
                    .join('')}
                </ul>
              </div>
            </div>
          </section>
        `,
          )
          .join('')}
      </main>

      <footer class="footer">
        <img class="footer__logo" src="/logo.png" alt="" width="88" height="88" />
        <p class="footer__brand">Chicken Boom</p>
        <p class="footer__tag">دجاج بنكهة قوية</p>
        <p class="footer__note" dir="ltr">More than chicken — it's a BOOM!</p>
        <div class="footer__meta">
          <span>منيو إلكتروني</span>
          <span class="footer__dot" aria-hidden="true">•</span>
          <span>2026</span>
        </div>
      </footer>
    </div>

    <button type="button" class="to-top" id="toTop" aria-label="العودة للأعلى" hidden>↑</button>
  </div>
`;

const catsNav = document.getElementById('cats');
const catButtons = [...document.querySelectorAll('.cats__btn')];
const sections = [...document.querySelectorAll('[data-section]')];
const toTop = document.getElementById('toTop');

function setActive(id) {
  catButtons.forEach((btn) => {
    const active = btn.dataset.target === id;
    btn.classList.toggle('is-active', active);
    btn.setAttribute('aria-selected', String(active));
    if (active) {
      btn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  });
}

function scrollToSection(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const navH = catsNav.getBoundingClientRect().height;
  const top = el.getBoundingClientRect().top + window.scrollY - navH - 8;
  window.scrollTo({ top, behavior: 'smooth' });
}

catButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    setActive(btn.dataset.target);
    scrollToSection(btn.dataset.target);
  });
});

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((e) => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
    if (visible[0]) setActive(visible[0].target.id);
  },
  { rootMargin: '-25% 0px -50% 0px', threshold: [0.12, 0.4] },
);

sections.forEach((section) => observer.observe(section));

toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

window.addEventListener(
  'scroll',
  () => {
    toTop.hidden = window.scrollY < 400;
  },
  { passive: true },
);
