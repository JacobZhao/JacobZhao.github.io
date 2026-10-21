document.documentElement.classList.add('js');
const search = document.querySelector('#publication-search');
if (search) {
  const entries = [...document.querySelectorAll('.publication')];
  const groups = [...document.querySelectorAll('.year-group')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const year = document.querySelector('#publication-year');
  const status = document.querySelector('#results-status');
  const empty = document.querySelector('#empty-state');
  let selectedType = 'all';
  const apply = () => {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach(entry => {
      const text = entry.textContent.toLocaleLowerCase();
      const visible = (selectedType === 'all' || entry.dataset.type === selectedType)
        && (year.value === 'all' || entry.dataset.year === year.value)
        && terms.every(term => text.includes(term));
      entry.hidden = !visible;
      if (visible) count++;
    });
    groups.forEach(group => { group.hidden = !group.querySelector('.publication:not([hidden])'); });
    status.textContent = `Showing ${count} of ${entries.length} entries`;
    empty.hidden = count !== 0;
  };
  filters.forEach(button => button.addEventListener('click', () => {
    selectedType = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    apply();
  }));
  search.addEventListener('input', apply);
  year.addEventListener('change', apply);
  document.querySelector('#reset-filters').addEventListener('click', () => {
    search.value = ''; year.value = 'all'; selectedType = 'all';
    filters.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.filter === 'all')));
    apply(); search.focus();
  });
  apply();
}
